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

