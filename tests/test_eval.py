"""Tests for advertising benchmarks."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_gaql_eval():
    from eval.advertising_bench import run_gaql_eval
    result = run_gaql_eval(model=None)
    assert result.score == 100.0
    assert result.name == "GAQL-Eval"

def test_ppc_math_eval():
    from eval.advertising_bench import run_ppc_math_eval
    result = run_ppc_math_eval(model=None)
    assert result.score == 100.0

def test_cross_platform_eval():
    from eval.advertising_bench import run_cross_platform_eval
    result = run_cross_platform_eval(model=None)
    assert result.score == 100.0
