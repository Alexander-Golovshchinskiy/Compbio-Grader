# ----- Exercise 5: ReverseComplement -----
from typing import Callable, Tuple, List

def _ref_reverse_complement(pattern: str) -> str:
    """Reference implementation for ReverseComplement."""
    comp = {"A": "T", "T": "A", "G": "C", "C": "G"}
    try:
        rc = "".join(comp[b] for b in reversed(pattern.upper()))
    except KeyError:
        # invalid base — treat as unchanged
        rc = "".join(comp.get(b, b) for b in reversed(pattern.upper()))
    return rc


_HIDDEN_REVERSECOMP: List[str] = [
    "AAAACCCGGT",        # classic test
    "ATCG",              # small example
    "ATATATAT",          # symmetric pattern
    "AGCTTTCGA",         # palindrome
    "acgtacgt",          # lowercase input
    "NNNN",              # invalid bases
    "",                  # empty string
    "GATTACA",           # random sequence
    "CCCGGGTTTAAA",      # larger sequence
]

def check_reversecomplement(fn: Callable[[str], str]) -> Tuple[bool, str]:
    """
    Run hidden tests for ReverseComplement.
    Returns (passed: bool, awarded_letter: str)
    """
    try:
        for dna in _HIDDEN_REVERSECOMP:
            result = fn(dna)
            expected = _ref_reverse_complement(dna)
            if result != expected:
                print(f"❌ Mismatch for input '{dna}': expected '{expected}', got '{result}'")
                return False, ""
    except Exception as e:
        print(f"❌ Error during hidden check: {e}")
        return False, ""

    # Award one random letter (use helper that avoids repeats)
    letter = _award_random_letter()
    print(f"✅ All hidden tests passed! Awarded letter: {letter}")
    return True, letter

