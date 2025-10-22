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

