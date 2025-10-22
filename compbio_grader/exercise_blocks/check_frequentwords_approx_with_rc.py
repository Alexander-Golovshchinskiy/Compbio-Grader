# ===== Add to compbio_grader/checks2.py — Hidden Tests for FrequentWordsApproximateWithRC =====

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

def _ref_rc(s: str) -> str:
    comp = str.maketrans("ACGT", "TGCA")
    return s.translate(comp)[::-1]

def _ref_frequent_words_with_rc(Text: str, k: int, d: int) -> List[str]:
    n = len(Text)
    if k <= 0 or d < 0 or n < k:
        return []
    counts: Dict[str, int] = defaultdict(int)
    for i in range(n - k + 1):
        kmer = Text[i:i+k]
        for neigh in _ref_neighbors(kmer, d):
            counts[neigh] += 1
    if not counts:
        return []
    scores: Dict[str, int] = {}
    for p, c in counts.items():
        scores[p] = c + counts.get(_ref_rc(p), 0)
    maxs = max(scores.values())
    return sorted({p for p, s in scores.items() if s == maxs})

_HIDDEN_TESTS_EX6_RC: List[Tuple[str, int, int, List[str]]] = [
    ("ACGTTGCATGTCGCATGATGCATGAGAGCT", 4, 1, ["ACAT", "ATGT"]),  # sample
    ("ATATAT", 2, 0, ["AT"]),                                    # palindromic case
    ("", 5, 1, []),
    ("AAA", 4, 1, []),
    ("AAAAAAAAAA", 3, 1, _ref_frequent_words_with_rc("AAAAAAAAAA", 3, 1)),
    ("GATTACA", 3, 1, _ref_frequent_words_with_rc("GATTACA", 3, 1)),
    ("CTAGCTAG", 3, 2, _ref_frequent_words_with_rc("CTAGCTAG", 3, 2)),
]

def check_frequentwords_approx_with_rc(fn: Callable[[str, int, int], List[str]], *, award_letter: bool = True):
    """
    Hidden tests for FrequentWords with mismatches + reverse complements.
    Compares lexicographically sorted outputs to a trusted reference.
    Returns (passed: bool, letter: str).
    """
    for text, k, d, expected in _HIDDEN_TESTS_EX6_RC:
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

    print("✅ All hidden FrequentWordsApproximateWithRC tests passed!")
    return (True, letter_for_exercise(7)) if award_letter else (True, "")

