"""
MiniAgent RAG — Retrieval-Augmented Generation for Advertising Knowledge

Searches a local knowledge base of advertising expertise before generating answers.
No external dependencies — uses TF-IDF-like similarity with Python stdlib.

Usage:
    from miniagent.rag import KnowledgeBase
    kb = KnowledgeBase()
    kb.load_from_skills("./skills/")
    kb.load_from_docs("./docs/")
    context = kb.search("What is CPA?", top_k=3)
"""

import json
import math
import os
import re
from collections import Counter
from pathlib import Path
from typing import List, Tuple


class KnowledgeBase:
    """Simple TF-IDF knowledge base for advertising domain."""

    def __init__(self):
        self.documents: List[dict] = []  # {"text": str, "source": str, "title": str}
        self._index_dirty = True
        self._idf: dict = {}
        self._doc_vectors: list = []

    def add(self, text: str, source: str = "", title: str = ""):
        """Add a document to the knowledge base."""
        text = text.strip()
        if len(text) < 20:
            return
        self.documents.append({"text": text, "source": source, "title": title})
        self._index_dirty = True

    def load_from_skills(self, skills_dir: str):
        """Load SKILL.md files as knowledge chunks."""
        skills_path = Path(skills_dir)
        if not skills_path.exists():
            return 0
        count = 0
        for skill_dir in skills_path.iterdir():
            skill_file = skill_dir / "SKILL.md"
            if skill_file.exists():
                content = skill_file.read_text(encoding="utf-8")
                chunks = self._chunk_markdown(content)
                for chunk in chunks:
                    self.add(chunk, source=str(skill_file), title=skill_dir.name)
                    count += 1
        print(f"Loaded {count} chunks from {skills_dir}")
        return count

    def load_from_docs(self, docs_dir: str):
        """Load markdown docs as knowledge chunks."""
        docs_path = Path(docs_dir)
        if not docs_path.exists():
            return 0
        count = 0
        for md_file in docs_path.rglob("*.md"):
            content = md_file.read_text(encoding="utf-8")
            chunks = self._chunk_markdown(content)
            for chunk in chunks:
                self.add(chunk, source=str(md_file), title=md_file.stem)
                count += 1
        print(f"Loaded {count} chunks from {docs_dir}")
        return count

    def load_from_jsonl(self, path: str):
        """Load from a JSONL file (pretrain or SFT format)."""
        if not os.path.exists(path):
            return 0
        count = 0
        seen = set()
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                item = json.loads(line.strip())
                text = item.get("text", "")
                if not text:
                    user = item.get("user", "")
                    assistant = item.get("assistant", "")
                    text = f"Q: {user}\nA: {assistant}" if user else ""
                if text and text not in seen:
                    self.add(text, source=path)
                    seen.add(text)
                    count += 1
        print(f"Loaded {count} unique entries from {path}")
        return count

    def search(self, query: str, top_k: int = 3) -> List[dict]:
        """Find the most relevant documents for a query."""
        if self._index_dirty:
            self._build_index()

        query_tokens = self._tokenize(query)
        query_vec = self._vectorize(query_tokens)

        scores = []
        for i, doc_vec in enumerate(self._doc_vectors):
            score = self._cosine_sim(query_vec, doc_vec)
            scores.append((score, i))

        scores.sort(reverse=True)
        results = []
        for score, idx in scores[:top_k]:
            if score > 0:
                doc = self.documents[idx].copy()
                doc["relevance"] = round(score, 4)
                results.append(doc)
        return results

    def get_context(self, query: str, top_k: int = 3, max_chars: int = 2000) -> str:
        """Get formatted context string for RAG prompting."""
        results = self.search(query, top_k)
        if not results:
            return ""
        parts = []
        total = 0
        for r in results:
            text = r["text"]
            if total + len(text) > max_chars:
                text = text[:max_chars - total]
            parts.append(text)
            total += len(text)
            if total >= max_chars:
                break
        return "\n\n---\n\n".join(parts)

    def save(self, path: str):
        """Save knowledge base to JSON."""
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.documents, f, ensure_ascii=False, indent=2)
        print(f"Saved {len(self.documents)} documents to {path}")

    def load(self, path: str):
        """Load knowledge base from JSON."""
        with open(path, "r", encoding="utf-8") as f:
            self.documents = json.load(f)
        self._index_dirty = True
        print(f"Loaded {len(self.documents)} documents from {path}")

    def _chunk_markdown(self, text: str, max_chunk: int = 500) -> List[str]:
        """Split markdown into chunks by headers and paragraphs."""
        text = re.sub(r"```[\s\S]*?```", "", text)
        text = re.sub(r"---\n.*?\n---", "", text)
        sections = re.split(r"\n#{1,4}\s+", text)
        chunks = []
        for section in sections:
            section = section.strip()
            if len(section) < 30:
                continue
            section = re.sub(r"\|[^\n]+\|", " ", section)
            section = re.sub(r"\n{3,}", "\n\n", section)
            section = re.sub(r"[*_`#>|]", "", section)
            section = section.strip()
            if len(section) > max_chunk:
                paragraphs = section.split("\n\n")
                current = ""
                for p in paragraphs:
                    if len(current) + len(p) > max_chunk and current:
                        chunks.append(current.strip())
                        current = p
                    else:
                        current += "\n\n" + p if current else p
                if current.strip():
                    chunks.append(current.strip())
            elif len(section) >= 30:
                chunks.append(section)
        return chunks

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        text = re.sub(r"[^a-z0-9_\s]", " ", text)
        return [w for w in text.split() if len(w) > 1]

    def _build_index(self):
        all_tokens = []
        doc_token_lists = []
        for doc in self.documents:
            tokens = self._tokenize(doc["text"])
            doc_token_lists.append(tokens)
            all_tokens.extend(set(tokens))

        df = Counter(all_tokens)
        n = len(self.documents) or 1
        self._idf = {t: math.log(n / (1 + c)) for t, c in df.items()}

        self._doc_vectors = []
        for tokens in doc_token_lists:
            self._doc_vectors.append(self._vectorize(tokens))

        self._index_dirty = False

    def _vectorize(self, tokens: List[str]) -> dict:
        tf = Counter(tokens)
        total = len(tokens) or 1
        return {t: (c / total) * self._idf.get(t, 0) for t, c in tf.items()}

    def _cosine_sim(self, a: dict, b: dict) -> float:
        common = set(a.keys()) & set(b.keys())
        if not common:
            return 0.0
        dot = sum(a[k] * b[k] for k in common)
        norm_a = math.sqrt(sum(v * v for v in a.values()))
        norm_b = math.sqrt(sum(v * v for v in b.values()))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot / (norm_a * norm_b)


def build_default_kb(repo_root: str = ".") -> KnowledgeBase:
    """Build knowledge base from all available sources in the repo."""
    kb = KnowledgeBase()
    root = Path(repo_root)

    kb.load_from_skills(str(root / "skills"))
    kb.load_from_docs(str(root / "docs"))

    for jsonl in ["dataset/pretrain_ads.jsonl", "dataset/sft_ads.jsonl"]:
        path = root / jsonl
        if path.exists():
            kb.load_from_jsonl(str(path))

    return kb


if __name__ == "__main__":
    kb = build_default_kb()
    print(f"\nKnowledge base: {len(kb.documents)} documents")

    test_queries = [
        "What is CPA in Google Ads?",
        "How do I set up conversion tracking?",
        "Compare Google Ads and Meta Ads",
        "What is ACOS on Amazon?",
    ]
    for q in test_queries:
        results = kb.search(q, top_k=2)
        print(f"\nQ: {q}")
        for r in results:
            print(f"  [{r['relevance']:.3f}] {r['text'][:100]}...")
