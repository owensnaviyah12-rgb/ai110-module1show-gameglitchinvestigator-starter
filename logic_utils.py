def get_range_for_difficulty(difficulty: str):
    """Return the inclusive (low, high) guessing range for a difficulty level."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        # FIX: Hard used to be 1-50, which made it easier than Normal (1-100).
        return 1, 200
    return 1, 100


def parse_guess(raw):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None or raw.strip() == "":
        return False, None, "Enter a guess."

    raw = raw.strip()
    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except (ValueError, OverflowError):
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare an int guess to an int secret and return (outcome, message).

    outcome is one of: "Win", "Too High", "Too Low".
    """
    # FIX: Refactored into logic_utils.py. The hint messages were swapped
    # ("Too High" used to say "Go HIGHER!"). The old string-comparison
    # fallback was removed because app.py now always passes an int secret.
    if guess == secret:
        return "Win", "🎉 Correct!"
    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update the score based on the outcome and which attempt this was."""
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    # FIX: "Too High" used to add +5 on even attempts. Wrong guesses
    # should always cost points.
    if outcome in ("Too High", "Too Low"):
        return current_score - 5

    return current_score