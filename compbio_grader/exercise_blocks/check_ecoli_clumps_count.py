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
    print(f"✅ Correct! Awarded letters: {' '.join(ltrs)}")
    return True, ltrs

