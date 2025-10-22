# ===== Add to compbio_grader/checks2.py — Hidden Tests for FrequentWordsApproximate =====

from typing import Callable, List, Tuple, Dict
from collections import defaultdict

def _ref_hamming(a: str, b: str) -> int:
    return sum(x != y for x, y in zip(a, b))

def _ref_neighbors(pattern: str, d: int):
    alpha = ("A", "C", "G", "T")
    if d == 0:
        return [pattern]
    if len(pattern) == 1:
        return list(alpha)
    neighborhood = set()
    for text in _ref_neighbors(pattern[1:], d):
        if _ref_hamming(pattern[1:], text) < d:
            for x in alpha:
                neighborhood.add(x + text)
        else:
            neighborhood.add(pattern[0] + text)
    return neighborhood

def _ref_frequent_words_approx(Text: str, k: int, d: int) -> List[str]:
    counts: Dict[str, int] = defaultdict(int)
    for i in range(len(Text) - k + 1):
        kmer = Text[i:i+k]
        for neigh in _ref_neighbors(kmer, d):
            counts[neigh] += 1
    if not counts:
        return []
    maxc = max(counts.values())
    return sorted([p for p, c in counts.items() if c == maxc])

_HIDDEN_TESTS_EX5B: List[Tuple[str, int, int, List[str]]] = [
    # (Text, k, d, expected-most-frequent list (lexicographically sorted))
    ("ACGTTGCATGTCGCATGATGCATGAGAGCT", 4, 1, ["ATGC", "ATGT", "GATG"]),  # textbook sample
    ("", 4, 1, []),
    ("AAA", 4, 1, []),
    ("AAAAAAAAAA", 3, 0, ["AAA"]),
    # For all As with d=1, winners are the whole 1-neighborhood of "AAA"
    ("AAAAAAAAAA", 3, 1, sorted(_ref_neighbors("AAA", 1))),
    ("GATTACA", 3, 1, _ref_frequent_words_approx("GATTACA", 3, 1)),
    ("ATATATAT", 2, 1, _ref_frequent_words_approx("ATATATAT", 2, 1)),
]

def check_frequentwordsapproximate(fn: Callable[[str, int, int], List[str]], *, award_letter: bool = True):
    """
    Hidden tests for FrequentWordsApproximate.
    Compares lexicographically sorted outputs to a trusted reference.
    Returns (passed: bool, letter: str).
    """
    for text, k, d, expected in _HIDDEN_TESTS_EX5B:
        try:
            got = fn(text, k, d)
        except Exception as e:
            print(f"❌ Error on input (k={k}, d={d}): {e}")
            return False, ""
        if sorted(got) != sorted(expected):
            print("❌ Mismatch.")
            print(f"Text (len {len(text)}), k={k}, d={d}")
            print(f"Expected: {' '.join(expected)}")
            print(f"Got:      {' '.join(sorted(got))}")
            return False, ""

    print("✅ All hidden FrequentWordsApproximate tests passed!")
    return (True, letter_for_exercise(6)) if award_letter else (True, "")

