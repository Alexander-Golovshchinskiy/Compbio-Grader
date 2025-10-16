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

