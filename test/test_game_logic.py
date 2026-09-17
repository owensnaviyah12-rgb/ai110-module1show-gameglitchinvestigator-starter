from logic_utils import check_guess, get_range_for_difficulty

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