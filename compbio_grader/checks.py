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
    return True, letter

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
    letter = _SHUFFLED[4] if len(_SHUFFLED) > 4 else ""
    return True, letter

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
    return True, letter

# ----- Exercise 7: Genome-scale scan (fixed expected answer, two-letter award) -----
from typing import Callable, List, Union

# If your file already defines _SHUFFLED, this block is a no-op.
try:
    _SHUFFLED  # type: ignore[name-defined]
except NameError:
    # Minimal fallback so this block works standalone (keep behavior consistent)
    import os, random
    _WORD = "REPLICATOR"
    def _shuffled_word() -> str:
        seed = os.getenv("COMPBIO_GRADER_SEED")
        rng = random.Random(seed) if seed is not None else random.Random()
        letters = list(_WORD)
        rng.shuffle(letters)
        return "".join(letters)
    _SHUFFLED = _shuffled_word()

# The one correct list of start positions (0-based) for CTTGATCAT in Vibrio cholerae:
_EX7_CORRECT_POSITIONS: List[int] = [60039, 98409, 129189, 152283, 152354, 152411, 163207, 197028, 200160, 357976, 376771, 392723, 532935, 600085, 622755, 1065555]

def _ex7_normalize_positions(out: Union[str, List[int]]) -> List[int]:
    """
    Accept either a list[int] or a space-separated string of ints.
    Return sorted unique positions (strictly increasing).
    """
    if isinstance(out, list):
        pos = list(out)
    elif isinstance(out, str):
        s = out.strip()
        pos = [] if not s else [int(x) for x in s.split()]
    else:
        raise TypeError("Output must be a list of ints or a space-separated string of ints.")
    pos = sorted(set(int(x) for x in pos))
    return pos

def check_genome_scan(fn: Callable[..., Union[str, List[int]]]):
    """
    Hidden check for Exercise 7 (V. cholerae genome scan).
    Expects a callable that returns the student's submitted positions (list[int] or space-separated string).
    The callable may ignore its arguments (we pass dummy args).

    Returns:
        (passed: bool, letters: List[str])
        On success, awards TWO letters (fixed mapping: indices 6 and 7 of _SHUFFLED).
    """
    try:
        # Call with harmless dummy inputs; student wrapper will ignore them and return 'ans'
        out = fn("", "")
        got = _ex7_normalize_positions(out)
        ref = list(_EX7_CORRECT_POSITIONS)

        if got != ref:
            print("❌ Your submitted positions don’t match the expected answer.")
            # Helpful diagnostics without leaking the reference list fully
            print(f"   You submitted {len(got)} positions; expected {len(ref)}.")
            # Show first mismatch if lengths equal
            if len(got) == len(ref):
                for i, (a, b) in enumerate(zip(got, ref)):
                    if a != b:
                        print(f"   First mismatch at index {i}: got {a}, expected {b}")
                        break
            return False, []
    except Exception as e:
        print(f"❌ Error during submission check: {e}")
        return False, []

    # Success → award two letters (Exercise 7 bonus)
    l1 = _SHUFFLED[6] if len(_SHUFFLED) > 6 else ""
    l2 = _SHUFFLED[7] if len(_SHUFFLED) > 7 else ""
    letters = [l for l in (l1, l2) if l]
    return True, letters

# ----- Final scaled exercise: E. coli (9-mers forming (500,3)-clumps) -----
from typing import Callable, Union, List, Set, Dict

# TODO: set this to the true count for E_coli.txt once you compute it locally.
_EX9_CORRECT_COUNT: int = 1904  # <-- REPLACE with the correct integer before the workshop

def _ex9_parse_count(ans: Union[int, str]) -> int:
    """
    Accept either an int or a string containing an int (with optional whitespace).
    Raise ValueError if it isn't a clean integer.
    """
    if isinstance(ans, int):
        return ans
    if isinstance(ans, str):
        s = ans.strip()
        if s == "":
            raise ValueError("Empty string provided as answer.")
        return int(s)
    raise TypeError("Answer must be an int or a string containing an int.")

def check_ecoli_clumps_count(fn: Callable[[], Union[int, str]]):
    """
    Hidden check for: number of distinct 9-mers forming (500,3)-clumps in E. coli.
    The callable `fn` should return the student’s submitted answer (int or str).

    Returns:
        (passed: bool, letters: List[str])
    On success, awards TWO letters (indices 8 and 9 of the shuffled acronym).
    """
    # sanity guard: make sure the host filled the constant
    if not isinstance(_EX9_CORRECT_COUNT, int) or _EX9_CORRECT_COUNT < 0:
        print("❌ Grader not initialized: _EX9_CORRECT_COUNT is not set.")
        return False, []

    try:
        out = fn()  # pull the student’s submitted answer
        got = _ex9_parse_count(out)
    except Exception as e:
        print(f"❌ Could not read your answer as an integer: {e}")
        return False, []

    if got != _EX9_CORRECT_COUNT:
        print("❌ Not quite. Your number of (500,3)-clump 9-mers does not match.")
        return False, []

    # Success → award two letters (final bonus)
    ltrs = []
    if len(_SHUFFLED) > 8: ltrs.append(_SHUFFLED[8])
    if len(_SHUFFLED) > 9: ltrs.append(_SHUFFLED[9])
    return True, ltrs

