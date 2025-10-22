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

