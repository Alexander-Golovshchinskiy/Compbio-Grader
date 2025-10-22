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

