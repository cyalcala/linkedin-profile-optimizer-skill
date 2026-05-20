#!/usr/bin/env python3
"""Create a lightweight LinkedIn keyword map from target texts and a profile draft.

The script uses only the Python standard library so it can run inside a skill
without dependency setup. It is a first-pass aid, not a replacement for judgment.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


STOPWORDS = {
    "a",
    "about",
    "above",
    "across",
    "after",
    "all",
    "also",
    "an",
    "and",
    "any",
    "are",
    "as",
    "at",
    "be",
    "because",
    "been",
    "being",
    "between",
    "both",
    "but",
    "by",
    "can",
    "could",
    "did",
    "do",
    "does",
    "doing",
    "during",
    "each",
    "for",
    "from",
    "had",
    "has",
    "have",
    "having",
    "how",
    "i",
    "if",
    "in",
    "into",
    "is",
    "it",
    "its",
    "more",
    "most",
    "must",
    "of",
    "on",
    "or",
    "our",
    "out",
    "over",
    "own",
    "per",
    "should",
    "such",
    "than",
    "that",
    "the",
    "their",
    "them",
    "then",
    "there",
    "these",
    "they",
    "this",
    "through",
    "to",
    "using",
    "was",
    "we",
    "were",
    "with",
    "within",
    "will",
    "would",
    "you",
    "your",
}


DEFAULT_PHRASES = {
    "account management",
    "account executive",
    "agile development",
    "ai agents",
    "api integration",
    "artificial intelligence",
    "b2b saas",
    "business development",
    "business intelligence",
    "cloud infrastructure",
    "conversion optimization",
    "cross-functional",
    "customer success",
    "data analysis",
    "data engineering",
    "data science",
    "digital marketing",
    "etl pipeline",
    "full stack",
    "generative ai",
    "go to market",
    "growth strategy",
    "large language model",
    "lead generation",
    "machine learning",
    "market research",
    "marketing automation",
    "natural language processing",
    "operations management",
    "performance marketing",
    "product management",
    "project management",
    "prompt engineering",
    "revenue operations",
    "sales development",
    "search engine optimization",
    "software engineering",
    "stakeholder management",
    "technical leadership",
    "user experience",
    "user research",
}


TOKEN_RE = re.compile(r"[a-zA-Z][a-zA-Z0-9+#./-]*")


@dataclass(frozen=True)
class KeywordRow:
    keyword: str
    target_hits: int
    profile_hits: int
    sources: int

    @property
    def gap(self) -> bool:
        return self.target_hits > 0 and self.profile_hits == 0

    @property
    def score(self) -> tuple[int, int, str]:
        return (self.target_hits, self.sources, self.keyword)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def tokenize(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_RE.findall(text)]


def normalized_text(text: str) -> str:
    return " ".join(tokenize(text))


def interesting_unigrams(tokens: Iterable[str]) -> Counter[str]:
    counts: Counter[str] = Counter()
    for token in tokens:
        if token in STOPWORDS:
            continue
        if len(token) < 3 and token not in {"ai", "ml", "go"}:
            continue
        if token.isdigit():
            continue
        counts[token] += 1
    return counts


def ngrams(tokens: list[str], n: int) -> Counter[str]:
    counts: Counter[str] = Counter()
    for i in range(0, max(0, len(tokens) - n + 1)):
        gram_tokens = tokens[i : i + n]
        if any(token in STOPWORDS for token in gram_tokens):
            continue
        if all(len(token) < 3 for token in gram_tokens):
            continue
        counts[" ".join(gram_tokens)] += 1
    return counts


def phrase_hits(text: str, phrases: Iterable[str]) -> Counter[str]:
    normalized = f" {normalized_text(text)} "
    counts: Counter[str] = Counter()
    for phrase in phrases:
        needle = f" {phrase.lower()} "
        count = normalized.count(needle)
        if count:
            counts[phrase.lower()] += count
    return counts


def extract_keywords(text: str, phrases: Iterable[str], max_ngrams: int) -> Counter[str]:
    tokens = tokenize(text)
    counts = interesting_unigrams(tokens)
    counts.update(phrase_hits(text, phrases))
    for n in range(2, max_ngrams + 1):
        for gram, count in ngrams(tokens, n).items():
            if count >= 2:
                counts[gram] += count
    return counts


def load_phrases(paths: list[Path]) -> set[str]:
    phrases = set(DEFAULT_PHRASES)
    for path in paths:
        for line in read_text(path).splitlines():
            item = line.strip().lower()
            if item and not item.startswith("#"):
                phrases.add(item)
    return phrases


def build_rows(
    target_texts: list[str],
    profile_text: str,
    phrases: Iterable[str],
    max_ngrams: int,
) -> list[KeywordRow]:
    target_counts: Counter[str] = Counter()
    source_counts: defaultdict[str, int] = defaultdict(int)

    for text in target_texts:
        extracted = extract_keywords(text, phrases, max_ngrams)
        target_counts.update(extracted)
        for keyword in extracted:
            source_counts[keyword] += 1

    profile_counts = extract_keywords(profile_text, phrases, max_ngrams) if profile_text else Counter()

    rows = [
        KeywordRow(
            keyword=keyword,
            target_hits=target_counts[keyword],
            profile_hits=profile_counts.get(keyword, 0),
            sources=source_counts[keyword],
        )
        for keyword in target_counts
    ]
    return sorted(rows, key=lambda row: row.score, reverse=True)


def placement_hint(keyword: str) -> str:
    if " " in keyword:
        return "headline/about/experience"
    if keyword in {"python", "react", "sql", "aws", "azure", "figma", "salesforce", "hubspot"}:
        return "skills/experience"
    return "about/skills"


def render_markdown(rows: list[KeywordRow], limit: int) -> str:
    visible = rows[:limit]
    lines = [
        "# LinkedIn Keyword Map",
        "",
        "| Keyword | Target hits | Source docs | Profile hits | Gap | Suggested placement |",
        "|---|---:|---:|---:|---|---|",
    ]
    for row in visible:
        lines.append(
            f"| {row.keyword} | {row.target_hits} | {row.sources} | "
            f"{row.profile_hits} | {'yes' if row.gap else 'no'} | {placement_hint(row.keyword)} |"
        )
    gap_count = sum(1 for row in rows if row.gap)
    lines.extend(
        [
            "",
            f"Total target keywords considered: {len(rows)}",
            f"Profile gaps in considered keywords: {gap_count}",
            "",
            "Use this as an input to human judgment. Do not add a keyword unless it is truthful.",
        ]
    )
    return "\n".join(lines)


def render_json(rows: list[KeywordRow], limit: int) -> str:
    data = [
        {
            "keyword": row.keyword,
            "target_hits": row.target_hits,
            "source_docs": row.sources,
            "profile_hits": row.profile_hits,
            "gap": row.gap,
            "suggested_placement": placement_hint(row.keyword),
        }
        for row in rows[:limit]
    ]
    return json.dumps(data, indent=2, sort_keys=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a LinkedIn keyword gap map.")
    parser.add_argument("--jobs", nargs="+", type=Path, required=True, help="Target job/client text files.")
    parser.add_argument("--profile", type=Path, help="Current profile or draft text file.")
    parser.add_argument("--phrases", nargs="*", type=Path, default=[], help="Optional newline keyword phrase files.")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--limit", type=int, default=40)
    parser.add_argument("--max-ngrams", type=int, default=3)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    phrases = load_phrases(args.phrases)
    target_texts = [read_text(path) for path in args.jobs]
    profile_text = read_text(args.profile) if args.profile else ""
    rows = build_rows(target_texts, profile_text, phrases, args.max_ngrams)
    if args.format == "json":
        print(render_json(rows, args.limit))
    else:
        print(render_markdown(rows, args.limit))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
