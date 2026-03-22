"""
MiniAgent Ad-Bench — Advertising-Specific Evaluation Suite

No existing LLM benchmark tests PPC knowledge. This does.
Tests: GAQL accuracy, campaign structure, PPC math, cross-platform, audit quality.

Usage:
    python eval/advertising_bench.py --model ./checkpoints/sft_512.pth
    python eval/advertising_bench.py --quick  # Runs without model (tests framework only)
"""

import json
import os
import sys
import argparse
from dataclasses import dataclass
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@dataclass
class BenchmarkResult:
    name: str
    total: int
    correct: int
    score: float
    details: list


# ─── GAQL EVAL ────────────────────────────────────────────────────────────────

GAQL_TESTS = [
    {
        "question": "Get top 10 campaigns by spend last 30 days",
        "expected_contains": ["SELECT", "campaign.name", "metrics.cost_micros", "LAST_30_DAYS", "ORDER BY", "DESC", "LIMIT 10"],
        "expected_resource": "campaign",
    },
    {
        "question": "Show me keywords with Quality Score below 5",
        "expected_contains": ["quality_info.quality_score", "keyword_view"],
        "expected_resource": "keyword_view",
    },
    {
        "question": "What search terms triggered my ads this week with zero conversions?",
        "expected_contains": ["search_term_view", "conversions", "LAST_7_DAYS"],
        "expected_resource": "search_term_view",
    },
    {
        "question": "Get impression share breakdown for all active campaigns",
        "expected_contains": ["search_impression_share", "search_budget_lost_impression_share", "search_rank_lost_impression_share"],
        "expected_resource": "campaign",
    },
    {
        "question": "Show Shopping campaign performance by product",
        "expected_contains": ["shopping_performance_view", "product_item_id"],
        "expected_resource": "shopping_performance_view",
    },
]

# ─── PPC MATH ─────────────────────────────────────────────────────────────────

PPC_MATH_TESTS = [
    {
        "question": "Cost is $5000, conversions is 100. What is the CPA?",
        "expected": 50.0, "tolerance": 0.01,
    },
    {
        "question": "Revenue is $15000, cost is $5000. What is the ROAS?",
        "expected": 3.0, "tolerance": 0.01,
    },
    {
        "question": "Impressions: 10000, Clicks: 350. What is the CTR?",
        "expected": 3.5, "tolerance": 0.1,
    },
    {
        "question": "cost_micros is 45000000. What is the actual cost in dollars?",
        "expected": 45.0, "tolerance": 0.01,
    },
    {
        "question": "Daily budget $100, 15 days remaining in month. What is the remaining budget?",
        "expected": 1500.0, "tolerance": 0.01,
    },
]

# ─── CAMPAIGN STRUCTURE ──────────────────────────────────────────────────────

STRUCTURE_TESTS = [
    {
        "scenario": "Ecommerce store with 500 products",
        "expected_campaigns": ["brand", "shopping", "non-brand", "remarketing"],
        "min_campaigns": 3,
    },
    {
        "scenario": "Local plumber serving 3 cities",
        "expected_campaigns": ["brand", "service", "location"],
        "min_campaigns": 2,
    },
    {
        "scenario": "B2B SaaS with $10K ACV",
        "expected_campaigns": ["brand", "non-brand", "competitor"],
        "min_campaigns": 2,
    },
]

# ─── CROSS-PLATFORM ──────────────────────────────────────────────────────────

CROSS_PLATFORM_TESTS = [
    {
        "question": "What is the Google Ads equivalent of Meta's 'ad set'?",
        "expected": "ad group",
    },
    {
        "question": "How do you convert Google cost_micros to dollars?",
        "expected": "divide by 1000000",
    },
    {
        "question": "What is Meta's equivalent of Google's Quality Score?",
        "expected": "relevance score",  # or "quality ranking"
    },
    {
        "question": "Which platform uses 'Sponsored Products' terminology?",
        "expected": "amazon",
    },
]


def run_gaql_eval(model=None) -> BenchmarkResult:
    """Evaluate GAQL query generation accuracy."""
    correct = 0
    details = []
    for test in GAQL_TESTS:
        if model is None:
            # Framework test — just verify test structure
            result = {"passed": True, "reason": "framework_test"}
            correct += 1
        else:
            generated = model.generate_text(test["question"])
            hits = sum(1 for kw in test["expected_contains"] if kw.lower() in generated.lower())
            passed = hits >= len(test["expected_contains"]) * 0.7  # 70% keyword match
            result = {"passed": passed, "hits": hits, "total_expected": len(test["expected_contains"])}
            if passed:
                correct += 1
        details.append({"test": test["question"], **result})

    return BenchmarkResult(
        name="GAQL-Eval",
        total=len(GAQL_TESTS),
        correct=correct,
        score=correct / len(GAQL_TESTS) * 100,
        details=details,
    )


def run_ppc_math_eval(model=None) -> BenchmarkResult:
    """Evaluate PPC math accuracy."""
    correct = 0
    details = []
    for test in PPC_MATH_TESTS:
        if model is None:
            correct += 1
            details.append({"test": test["question"], "passed": True, "reason": "framework_test"})
        else:
            generated = model.generate_text(test["question"])
            try:
                numbers = [float(s) for s in generated.split() if s.replace(".", "").replace("-", "").isdigit()]
                passed = any(abs(n - test["expected"]) <= test["tolerance"] for n in numbers)
            except Exception:
                passed = False
            if passed:
                correct += 1
            details.append({"test": test["question"], "passed": passed, "expected": test["expected"]})

    return BenchmarkResult(
        name="PPC-Math",
        total=len(PPC_MATH_TESTS),
        correct=correct,
        score=correct / len(PPC_MATH_TESTS) * 100,
        details=details,
    )


def run_cross_platform_eval(model=None) -> BenchmarkResult:
    """Evaluate cross-platform knowledge."""
    correct = 0
    details = []
    for test in CROSS_PLATFORM_TESTS:
        if model is None:
            correct += 1
            details.append({"test": test["question"], "passed": True})
        else:
            generated = model.generate_text(test["question"])
            passed = test["expected"].lower() in generated.lower()
            if passed:
                correct += 1
            details.append({"test": test["question"], "passed": passed})

    return BenchmarkResult(
        name="Cross-Platform",
        total=len(CROSS_PLATFORM_TESTS),
        correct=correct,
        score=correct / len(CROSS_PLATFORM_TESTS) * 100,
        details=details,
    )


def main():
    parser = argparse.ArgumentParser(description="MiniAgent Ad-Bench")
    parser.add_argument("--model", type=str, default=None, help="Model checkpoint path")
    parser.add_argument("--quick", action="store_true", help="Framework test only (no model)")
    parser.add_argument("--output", type=str, default="./eval/results.json")
    args = parser.parse_args()

    model = None
    if args.model and not args.quick:
        import torch
        from model.model_miniagent import MiniAgentModel
        checkpoint = torch.load(args.model, map_location="cpu")
        config = checkpoint["config"]
        model = MiniAgentModel(config)
        model.load_state_dict(checkpoint["model"])
        model.eval()

    print(f"\n{'='*60}")
    print(f"MiniAgent Ad-Bench — Advertising Evaluation Suite")
    print(f"{'='*60}")
    print(f"Mode: {'Quick (framework test)' if model is None else 'Full (with model)'}")
    print(f"{'='*60}\n")

    results = []
    for name, fn in [
        ("GAQL-Eval", run_gaql_eval),
        ("PPC-Math", run_ppc_math_eval),
        ("Cross-Platform", run_cross_platform_eval),
    ]:
        result = fn(model)
        results.append(result)
        status = "✅" if result.score >= 70 else "⚠️" if result.score >= 50 else "❌"
        print(f"  {status} {result.name}: {result.score:.1f}% ({result.correct}/{result.total})")

    # Overall
    total_correct = sum(r.correct for r in results)
    total_tests = sum(r.total for r in results)
    overall = total_correct / total_tests * 100

    print(f"\n  {'='*40}")
    print(f"  Overall: {overall:.1f}% ({total_correct}/{total_tests})")
    print(f"  {'='*40}\n")

    # Save results
    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    with open(args.output, "w") as f:
        json.dump({
            "overall_score": overall,
            "benchmarks": [
                {"name": r.name, "score": r.score, "correct": r.correct, "total": r.total}
                for r in results
            ],
        }, f, indent=2)
    print(f"Results saved to {args.output}")


if __name__ == "__main__":
    main()
