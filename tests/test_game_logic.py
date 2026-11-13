import pytest

from logic_utils import (
    check_guess,
    get_range_for_difficulty,
    get_temperature,
    parse_guess,
    update_score,
)


# --- Core bug fixes -------------------------------------------------------
def test_too_high_returns_correct_hint():
    # Bug fix: guess of 60 against secret of 50 should say "Too High"
    # and tell the player to go LOWER (not higher, as the old buggy code did)
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message.upper()


def test_too_low_returns_correct_hint():
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message.upper()


def test_easy_range_is_1_to_20():
    # Bug fix: "New Game" should respect this range instead of always 1-100
    low, high = get_range_for_difficulty("Easy")
    assert (low, high) == (1, 20)


def test_hard_is_harder_than_normal():
    # Bug fix: Hard used to be 1-50, which was easier than Normal (1-100)
    assert get_range_for_difficulty("Hard")[1] > (
        get_range_for_difficulty("Normal")[1]
    )


def test_unknown_difficulty_falls_back_to_normal():
    assert get_range_for_difficulty("Impossible") == (1, 100)


# --- Edge cases: empty, non-numeric, negative, huge input -----------------
@pytest.mark.parametrize("raw", ["", "   ", "\t\n", None])
def test_parse_guess_rejects_empty_input(raw):
    assert parse_guess(raw) == (False, None, "Enter a guess.")


@pytest.mark.parametrize(
    "raw",
    [
        "abc", "12abc", "1e3", "inf", "nan",
        "--5", "1.2.3", "1,000", "five", "!",
    ],
)
def test_parse_guess_rejects_non_numeric_strings(raw):
    assert parse_guess(raw) == (False, None, "That is not a number.")


@pytest.mark.parametrize(
    "raw, expected",
    [
        ("-5", -5),
        ("-0", 0),
        ("7.9", 7),
        ("-7.9", -7),
        ("  42  ", 42),
        ("+7", 7),
        ("007", 7),
    ],
)
def test_parse_guess_accepts_negative_decimal_and_padded(raw, expected):
    assert parse_guess(raw) == (True, expected, None)


def test_parse_guess_handles_overflowing_decimal():
    # float() turns this into infinity and int(inf) raises OverflowError,
    # which parse_guess must catch instead of crashing the game.
    raw = "1" + "0" * 400 + ".5"
    assert parse_guess(raw) == (False, None, "That is not a number.")


def test_check_guess_negative_guess_is_too_low():
    outcome, message = check_guess(-5, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message.upper()


def test_check_guess_exact_match_wins():
    assert check_guess(50, 50)[0] == "Win"


# --- Scoring --------------------------------------------------------------
@pytest.mark.parametrize("attempt", [1, 2, 3, 4])
@pytest.mark.parametrize("outcome", ["Too High", "Too Low"])
def test_wrong_guess_always_costs_five(outcome, attempt):
    # Bug fix: "Too High" used to ADD 5 points on even-numbered attempts.
    assert update_score(0, outcome, attempt) == -5


def test_win_score_drops_with_attempts_but_never_below_ten():
    assert update_score(0, "Win", 1) == 80
    assert update_score(0, "Win", 3) == 60
    assert update_score(0, "Win", 20) == 10


def test_unknown_outcome_leaves_score_unchanged():
    assert update_score(7, "Unknown", 1) == 7


# --- Hot/cold hints (UI enhancement) --------------------------------------
def test_temperature_close_guess_is_burning_hot():
    # Range 1-101 is 100 wide, so 2 away is 2% of the range.
    assert "burning hot" in get_temperature(52, 50, 1, 101).lower()


def test_temperature_far_guess_is_freezing_cold():
    assert "freezing" in get_temperature(101, 1, 1, 101).lower()


def test_temperature_middle_distances():
    assert "hot" in get_temperature(60, 50, 1, 101).lower()    # 10%
    assert "warm" in get_temperature(70, 50, 1, 101).lower()   # 20%
    assert "cold" in get_temperature(90, 50, 1, 101).lower()   # 40%


def test_temperature_scales_with_range_size():
    narrow = get_temperature(15, 5, 1, 20)    # 10 / 19, far away
    wide = get_temperature(110, 100, 1, 200)  # 10 / 199, close
    assert "cold" in narrow.lower() or "freezing" in narrow.lower()
    assert "burning" in wide.lower() or "hot" in wide.lower()


def test_temperature_single_number_range_does_not_crash():
    # low == high would divide by zero without the max(..., 1) guard.
    assert get_temperature(5, 5, 5, 5)
