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

