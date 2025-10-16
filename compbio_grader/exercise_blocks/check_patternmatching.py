# ----- Exercise 6: PatternMatching -----
from typing import Callable, List, Tuple

def _ref_pattern_matching(DNA: str, pattern: str) -> List[int]:
    """Reference implementation."""
    k = len(pattern)
    return [i for i in range(len(DNA) - k + 1) if DNA[i:i+k] == pattern]

# Tricky but valid hidden tests
_HIDDEN_PATTERNMATCHING: List[Tuple[str, str, List[int]]] = [
    ("GATATATGCATATACTT", "ATAT", [1, 3, 9]),     # standard
    ("AAAAA", "AA", [0, 1, 2, 3]),                # overlapping matches
    ("ACGTACGTACGT", "ACGT", [0, 4, 8]),          # periodic pattern
    ("ACACACAC", "ACAC", [0, 2, 4]),              # overlaps
    ("CCCC", "CCC", [0, 1]),                      # edge overlap
    ("AGTCAGTC", "AGT", [0, 4]),                  # simple repeats
    ("AGTCAGTCA", "GTCA", [1, 5]),                 # offset repeat
    ("AGTCAGTC", "AAAA", []),                     # no matches
    ("A", "A", [0]),                              # single-character match
    ("", "A", []),                                # empty DNA
]

def check_patternmatching(fn: Callable[[str, str], List[int]]):
    """
    Hidden tests for PatternMatching.
    Returns (passed: bool, awarded_letter: str)
    """
    try:
        for dna, pat, expected in _HIDDEN_PATTERNMATCHING:
            result = fn(dna, pat)
            if result != expected:
                print(f"❌ Mismatch for DNA='{dna[:12]}...' pattern='{pat}':")
                print(f"   expected {expected}, got {result}")
                return False, ""
    except Exception as e:
        print(f"❌ Error during hidden checks: {e}")
        return False, ""

    # one exercise = one letter (index 5 for Exercise 6)
    letter = _SHUFFLED[5] if len(_SHUFFLED) > 5 else ""
    print(f"✅ All hidden tests passed! Awarded letter: {letter}")
    return True, letter

