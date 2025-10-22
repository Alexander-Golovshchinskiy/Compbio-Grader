# ==============================
# EXERCISE 7 — Hidden check for E. coli ori window (k=9, d=1)
# ==============================

from typing import Iterable, List, Tuple, Union, Set
from collections import defaultdict

# Reuse your acronym utilities if present:
# - letter_for_exercise
# - _as_int_list (not needed here)
# We'll define local refs for this checker.

def _ref_hamming(a: str, b: str) -> int:
    return sum(x != y for x, y in zip(a, b))

def _ref_neighbors(pattern: str, d: int) -> Set[str]:
    alpha = ("A", "C", "G", "T")
    if d == 0:
        return {pattern}
    if len(pattern) == 1:
        return set(alpha)
    neighborhood = set()
    for t in _ref_neighbors(pattern[1:], d):
        if _ref_hamming(pattern[1:], t) < d:
            for x in alpha:
                neighborhood.add(x + t)
        else:
            neighborhood.add(pattern[0] + t)
    return neighborhood

def _ref_rc(s: str) -> str:
    return s.translate(str.maketrans("ACGT", "TGCA"))[::-1]

def _ref_frequent_with_rc(Text: str, k: int, d: int) -> List[str]:
    """
    Return all k-mers maximizing Count_d(Text, p) + Count_d(Text, rc(p)).
    """
    n = len(Text)
    if k <= 0 or d < 0 or n < k:
        return []
    counts = defaultdict(int)
    for i in range(n - k + 1):
        kmer = Text[i:i+k]
        for neigh in _ref_neighbors(kmer, d):
            counts[neigh] += 1
    if not counts:
        return []
    scores = {}
    for p, c in counts.items():
        scores[p] = c + counts.get(_ref_rc(p), 0)
    max_score = max(scores.values())
    return sorted({p for p, s in scores.items() if s == max_score})

def _as_str_set(maybe_vals: Union[str, Iterable[str], List[str]]) -> Set[str]:
    """
    Accept a list/iterable of strings OR a single space-separated string.
    Normalize to uppercase; ignore empty tokens; de-duplicate.
    """
    if isinstance(maybe_vals, str):
        tokens = [t for t in maybe_vals.strip().split() if t]
    else:
        tokens = [str(t) for t in maybe_vals]
    return {t.upper() for t in tokens}

def check_ecoli_ori(ans: Union[str, Iterable[str], List[str]], *, award_letter: bool = True):
    """
    Hidden checker for Exercise 7.
    - Reads E. coli genome from 'E_coli.txt' in the current working directory.
    - Slices the window [3923620, 3923620+500).
    - Computes the most frequent 9-mers with <=1 mismatch + reverse complements.
    - Compares against student's `ans` (list of strings OR space-separated string).
    Returns (passed: bool, letter: str).
    """
    # Load genome
    try:
        with open("E_coli.txt") as f:
            genome = f.read().replace("\n", "").strip().upper()
    except FileNotFoundError:
        print("❌ Could not find 'E_coli.txt' in the working directory.")
        return False, ""
    except Exception as e:
        print(f"❌ Error reading 'E_coli.txt': {e}")
        return False, ""

    # Define window and parameters
    start = 3923620  # zero-based
    L = 500
    k = 9
    d = 1

    if start < 0 or start + L > len(genome):
        print("❌ Window bounds are out of range for the provided genome.")
        return False, ""

    window = genome[start:start + L]

    # Compute expected winners
    expected = set(_ref_frequent_with_rc(window, k, d))

    # Normalize student answer
    try:
        got = _as_str_set(ans)
    except Exception as e:
        print(f"❌ Could not parse your answer: {e}")
        return False, ""

    # Compare sets
    if got != expected:
        missing = expected - got
        extra = got - expected
        print("❌ Incorrect ori-window motifs.")
        if missing:
            show_miss = " ".join(sorted(list(missing))[:10])
            print(f"  Missing ({len(missing)}): {show_miss}{' ...' if len(missing) > 10 else ''}")
        if extra:
            show_extra = " ".join(sorted(list(extra))[:10])
            print(f"  Extra ({len(extra)}): {show_extra}{' ...' if len(extra) > 10 else ''}")
        return False, ""

    print("✅ Correct! Your motifs match the most frequent 9-mers (≤1 mismatch, with RC) in the ori window.")
    # Exercise 7 → 0-based index 6 for letter assignment
    return (True, letter_for_exercise(6)) if award_letter else (True, "")

