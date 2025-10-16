# compbio_grader/checks.py
import os, random
from typing import Callable, Tuple, List

# ----------  ACRONYM SETUP ----------
_WORD = "REPLICATOR"

def _get_shuffled_word() -> str:
    """Shuffle once per session (optionally seed for reproducibility)."""
    seed = os.getenv("COMPBIO_GRADER_SEED")  # optional env var for reproducibility
    rng = random.Random(seed) if seed else random
    letters = list(_WORD)
    rng.shuffle(letters)
    return "".join(letters)

_SHUFFLED = _get_shuffled_word()

# ----------  EXERCISE 1: PatternCount ----------
def _ref_pattern_count(dna: str, pattern: str) -> int:
    k = len(pattern)
    return sum(1 for i in range(len(dna) - k + 1) if dna[i:i+k] == pattern)

_HIDDEN_TESTS = [
    ("ATATATATAT", "ATA", 4),
    ("GCCGCCGCC",  "GCC", 3),
    ("AAAAAA",     "AA",  5),
    ("CGCGCGCG",   "GCG", 3),
]

def check_patterncount(fn: Callable[[str, str], int]) -> Tuple[bool, str]:
    """
    Run hidden tests for PatternCount.
    Returns (passed: bool, awarded_letter: str)
    """
    for dna, pat, ans in _HIDDEN_TESTS:
        try:
            if fn(dna, pat) != ans:
                print("❌ One or more hidden tests failed.")
                return False, ""
        except Exception as e:
            print(f"❌ Error: {e}")
            return False, ""
    # success
    letter = _SHUFFLED[0]  # the 1st letter in the shuffled word
    print(f"✅ All hidden tests passed! You earned letter: {letter}")
    return True, letter

# Optional helpers (if you ever need them)
def shuffled_word() -> str:
    return _SHUFFLED

def letter_for_exercise(index: int) -> str:
    """Return the letter assigned to exercise index (0-based)."""
    return _SHUFFLED[index % len(_SHUFFLED)]

# ----- Exercise 2: FrequencyTable -----

from typing import Callable, Dict, List, Tuple

def _ref_frequency_table(dna: str, k: int) -> Dict[str, int]:
    """Reference implementation for hidden checks (overlapping k-mers)."""
    n = len(dna)
    freq: Dict[str, int] = {}
    if k <= 0:
        # Keep it simple/valid: treat k<=0 as no kmers
        return {}
    for i in range(n - k + 1):
        pat = dna[i:i+k]
        freq[pat] = freq.get(pat, 0) + 1
    return freq

# Hidden test set: valid, slightly tricky, but still fair.
# We compute the expected dict via the reference (so you can tweak DNA/k freely).
_HIDDEN_FREQTABLE: List[Tuple[str, int]] = [
    ("ACGTTTCACGTTTTACGG", 3),  # similar to visible, full dict equality check
    ("AAAAA", 2),               # heavy overlap: 'AA' x 4
    ("AAAAA", 4),               # 'AAAA' x 2
    ("ATATAT", 3),              # alternating: {'ATA':2, 'TAT':2}
    ("CCCCCC", 1),              # homopolymer single-base counts
    ("ACGT", 4),                # k == n -> single k-mer
    ("ACGT", 5),                # k > n -> empty dict
    ("ACACAGTGT", 2),           # mixed repeats
]

def check_frequencytable(fn: Callable[[str, int], Dict[str, int]]):
    """
    Run hidden tests for FrequencyTable.
    Returns (passed: bool, awarded_letter: str)
    """
    try:
        for dna, k in _HIDDEN_FREQTABLE:
            out = fn(dna, k)
            if not isinstance(out, dict):
                print("❌ Function must return a dict.")
                return False, ""
            exp = _ref_frequency_table(dna, k)
            if out != exp:
                print(f"❌ Mismatch for DNA='{dna[:12]}...' k={k}")
                return False, ""
    except Exception as e:
        print(f"❌ Error during checks: {e}")
        return False, ""

    # One exercise = one letter (use index 1 for exercise #2)
    letter = _SHUFFLED[1] if len(_SHUFFLED) > 1 else ""
    print(f"✅ All hidden tests passed! Awarded letter: {letter}")
    return True, letter

# ----- Exercise 3: MaxMap -----

from typing import Dict, Callable, Tuple, List

def _ref_maxmap(freqMap: Dict[str, int]) -> int:
    """Reference implementation."""
    if not freqMap:
        return 0
    return max(freqMap.values())

# A mix of edge & tricky valid cases.
_HIDDEN_MAXMAP: List[Dict[str, int]] = [
    {"A": 10, "B": 2, "C": 5},        # simple
    {"AA": 1, "BB": 1, "CC": 1},      # all equal
    {},                               # empty dict
    {"X": -5, "Y": -2, "Z": -10},     # negative values
    {"A": 9999999},                   # single key
    {f"K{i}": i for i in range(1000)}, # large dict
]

def check_maxmap(fn: Callable[[Dict[str, int]], int]) -> Tuple[bool, str]:
    """
    Run hidden tests for MaxMap.
    Returns (passed: bool, awarded_letter: str)
    """
    try:
        for freq in _HIDDEN_MAXMAP:
            result = fn(dict(freq))  # copy to avoid mutation
            expected = _ref_maxmap(freq)
            if result != expected:
                print(f"❌ Mismatch for input {list(freq.items())[:3]}... → expected {expected}, got {result}")
                return False, ""
    except Exception as e:
        print(f"❌ Error during hidden check: {e}")
        return False, ""

    # One exercise = one letter (index 2 for Exercise 3)
    letter = _SHUFFLED[2] if len(_SHUFFLED) > 2 else ""
    print(f"✅ All hidden tests passed! Awarded letter: {letter}")
    return True, letter

# ----- Exercise 4: FrequentWords -----
from typing import Callable, Dict, List, Tuple, Set

def _ref_frequent_words(dna: str, k: int) -> List[str]:
    """Reference: return all most-frequent k-mers (overlaps allowed)."""
    freq = _ref_frequency_table(dna, k)
    if not freq:
        return []
    m = _ref_maxmap(freq)
    return sorted([p for p, c in freq.items() if c == m])

# Valid-but-tricky hidden cases (ties, overlaps, k=1, k==n, k>n, homopolymers, alternating)
_HIDDEN_FREQWORDS: List[Tuple[str, int]] = [
    ("AAAAA", 2),                 # heavy overlaps -> {'AA'}
    ("AAAAA", 4),                 # -> {'AAAA'}
    ("ATATAT", 2),                # 'AT' more frequent than 'TA'
    ("ATATAT", 3),                # -> {'ATA'}
    ("ACGT", 1),                  # tie of all single letters
    ("ACGT", 4),                  # k == n -> [DNA]
    ("ACGT", 5),                  # k > n -> []
    ("GCGCGCGC", 2),              # 'GC' wins (4) over 'CG' (3)
    ("GCGCGCGC", 3),              # tie: {'GCG','CGC'}
    ("ACGTTGCATGTCGCATGATGCATGAGAGCT", 4),  # classic case (visible used elsewhere)
]

def check_frequentwords(fn: Callable[[str, int], List[str]]):
    """
    Hidden tests for FrequentWords(DNA, k).
    Returns (passed: bool, awarded_letter: str).
    """
    try:
        for dna, k in _HIDDEN_FREQWORDS:
            got = fn(dna, k)
            if not isinstance(got, list):
                print("❌ FrequentWords must return a list.")
                return False, ""
            # ensure elements are strings of length k (when k <= len(dna))
            if k <= len(dna):
                if any(not isinstance(x, str) or len(x) != k for x in got):
                    print(f"❌ Output contains non-{k}-mer entries for k={k}.")
                    return False, ""
                # avoid duplicates
                if len(set(got)) != len(got):
                    print("❌ Output contains duplicate patterns.")
                    return False, ""

            exp_set: Set[str] = set(_ref_frequent_words(dna, k))
            got_set: Set[str] = set(got)
            if got_set != exp_set:
                print(f"❌ Mismatch for DNA='{dna[:12]}...' k={k}\n"
                      f"   expected: {sorted(exp_set)}\n"
                      f"   got     : {sorted(got_set)}")
                return False, ""
    except Exception as e:
        print(f"❌ Error during hidden checks: {e}")
        return False, ""

    # One exercise = one letter (index 3 for exercise #4)
    letter = _SHUFFLED[3] if len(_SHUFFLED) > 3 else ""
    print(f"✅ All hidden tests passed! Awarded letter: {letter}")
    return True, letter

