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
    print(f"✅ All checks passed! Awarded letters: {' '.join(letters)}")
    return True, letters

