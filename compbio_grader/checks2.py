
from typing import Iterable, List, Tuple, Union
import os
import random

# ----------  ACRONYM / LETTER AWARDING ----------
_WORD = "PROTEIN"

def _get_shuffled_word() -> str:
    """Shuffle once per session (optionally seed via COMPBIO_GRADER_SEED)."""
    seed = os.getenv("COMPBIO_GRADER_SEED")
    rng = random.Random(seed) if seed else random
    letters = list(_WORD)
    rng.shuffle(letters)
    return "".join(letters)

_SHUFFLED = _get_shuffled_word()

def shuffled_word() -> str:
    """Return the per-session shuffled acronym."""
    return _SHUFFLED

def letter_for_exercise(index: int) -> str:
    """Return the letter assigned to exercise index (0-based)."""
    return _SHUFFLED[index % len(_SHUFFLED)]

# ----------  REFERENCE SOLUTION ----------
_EXERCISE_GENOME = "GAGCCACCGCGATA"

def _ref_skew_values(genome: str) -> List[int]:
    """Compute skew values for the genome: +1 for G, -1 for C, 0 for A/T."""
    vals = [0]
    skew = 0
    for ch in genome:
        if ch == "G":
            skew += 1
        elif ch == "C":
            skew -= 1
        vals.append(skew)
    return vals

_EXPECTED = _ref_skew_values(_EXERCISE_GENOME)

# ----------  HELPER ----------
def _as_int_list(maybe_vals: Union[str, Iterable[int], List[int]]) -> List[int]:
    """
    Accept either:
      - a list/iterable of ints, or
      - a space-separated string of ints
    Returns list[int].
    """
    if isinstance(maybe_vals, str):
        parts = maybe_vals.strip().split()
        return [int(x) for x in parts]
    return [int(x) for x in maybe_vals]

# ----------  MAIN CHECK FUNCTION ----------
def check_skew(ans: Union[str, Iterable[int], List[int]], *, award_letter: bool = True) -> Tuple[bool, str]:
    """
    Compare submitted `ans` to the true skew values for 'GAGCCACCGCGATA'.
    `ans` may be a list of ints or a space-separated string of ints.

    Returns (passed: bool, awarded_letter: str).
    """
    try:
        got = _as_int_list(ans)
    except Exception as e:
        print(f"❌ Could not parse your answer: {e}")
        return False, ""

    if len(got) != len(_EXPECTED):
        print(f"❌ Wrong number of values. Expected {len(_EXPECTED)}, got {len(got)}.")
        return False, ""

    if got != _EXPECTED:
        print("❌ Incorrect. Your skew values do not match the expected result.")
        return False, ""

    # success
    print("✅ Correct! Your skew values match exactly.")
    return (True, letter_for_exercise(0)) if award_letter else (True, "")




# ==============================
# EXERCISE 2 — Minimum Skew (E. coli)
# ==============================

_EXPECTED_ECOLI_MIN_SKEW = [3923620, 3923621, 3923622, 3923623]

def check_minimumskew(ans: Union[str, Iterable[int], List[int]], *, award_letter: bool = True) -> Tuple[bool, str]:
    """
    Check whether the submitted `ans` matches the known minimum-skew
    positions for the E. coli genome.

    Parameters
    ----------
    ans : list[int] | str
        Student answer — can be a list of ints or a space-separated string of ints.
    award_letter : bool
        Whether to return a session letter.

    Returns
    -------
    (passed: bool, letter: str)
    """
    try:
        got = _as_int_list(ans)
    except Exception as e:
        print(f"❌ Could not parse your answer: {e}")
        return False, ""

    if got != _EXPECTED_ECOLI_MIN_SKEW:
        print("❌ Incorrect. Your positions do not match the expected E. coli minimum-skew indices.")
        print(f"Expected: {_EXPECTED_ECOLI_MIN_SKEW}")
        print(f"Got:      {got}")
        return False, ""

    print("✅ Correct! Your positions match the E. coli minimum-skew indices.")
    return (True, letter_for_exercise(1)) if award_letter else (True, "")

# ==============================
# EXERCISE 5 — Approximate Pattern Count
# ==============================

_HIDDEN_TESTS_EX5 = [
    # (Text, Pattern, d, expected_count)
    ("TTTAGAGCCTTCAGAGG", "GAGG", 2, 4),                # sample
    ("AACAAGCTGATAAACATTTAAAGAG", "AAAAA", 1, 4),       # from description
    ("AAAAA", "AAAAA", 0, 1),                           # exact match
    ("AAAAAA", "AAA", 0, 4),                            # overlapping
    ("AAAAAA", "AAA", 1, 6),                            # mismatches allowed
    ("ACGTACGTACGT", "ACG", 1, 6),
]

def check_approximatepatterncount(fn: Callable[[str, str, int], int], *, award_letter: bool = True):
    """
    Run hidden tests for ApproximatePatternCount.
    """
    for text, pattern, d, expected in _HIDDEN_TESTS_EX5:
        try:
            result = fn(text, pattern, d)
        except Exception as e:
            print(f"❌ Error while running your function: {e}")
            return False, ""
        if result != expected:
            print(f"❌ Failed on input: ({pattern}, {text}, {d})")
            print(f"Expected {expected}, got {result}")
            return False, ""

    print("✅ All hidden tests passed!")
    return (True, letter_for_exercise(4)) if award_letter else (True, "")

# ===== Add to compbio_grader/checks2.py — Hidden Tests for Neighbors =====

# EXERCISE 6 — Neighbors (d-neighborhood)

def _ref_hamming(a: str, b: str) -> int:
    return sum(x != y for x, y in zip(a, b))

def _ref_neighbors(pattern: str, d: int):
    alphabet = ("A", "C", "G", "T")
    if d == 0:
        return [pattern]
    if len(pattern) == 1:
        return list(alphabet)
    neighborhood = set()
    suffix_neighbors = _ref_neighbors(pattern[1:], d)
    for text in suffix_neighbors:
        if _ref_hamming(pattern[1:], text) < d:
            for x in alphabet:
                neighborhood.add(x + text)
        else:
            neighborhood.add(pattern[0] + text)
    return sorted(neighborhood)

_HIDDEN_TESTS_EX6 = [
    ("ACG", 1),   # sample
    ("ACG", 0),
    ("A",   1),
    ("A",   0),
    ("AT",  2),
    ("GGGG", 1),
    ("TTTT", 2),
    ("AGTC", 3),
]

def check_neighbors(fn, *, award_letter: bool = True):
    """
    Hidden tests for Neighbors. `fn` should be the student's Neighbors function.
    Compares set equality against a trusted reference implementation.
    Returns (passed: bool, letter: str).
    """
    for pat, d in _HIDDEN_TESTS_EX6:
        try:
            got = set(fn(pat, d))
        except Exception as e:
            print(f"❌ Error while running your function on ({pat}, {d}): {e}")
            return False, ""
        expected = set(_ref_neighbors(pat, d))
        if got != expected:
            # Provide a compact diff
            missing = expected - got
            extra = got - expected
            print(f"❌ Mismatch for Pattern={pat}, d={d}")
            if missing:
                print(f"  Missing {min(len(missing),5)} example(s): {', '.join(list(sorted(missing))[:5])}")
            if extra:
                print(f"  Extra {min(len(extra),5)} example(s): {', '.join(list(sorted(extra))[:5])}")
            return False, ""

    print("✅ All hidden Neighbors tests passed!")
    return (True, letter_for_exercise(5)) if award_letter else (True, "")

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

