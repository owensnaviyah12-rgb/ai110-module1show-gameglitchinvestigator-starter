"""Game logic for the Glitchy Guesser number-guessing game."""


def get_range_for_difficulty(difficulty: str):
    """
    Return the inclusive guessing range for a difficulty level.

    Args:
        difficulty: One of "Easy", "Normal" or "Hard". Any other value
            falls back to the Normal range.

    Returns:
        A (low, high) tuple of ints.
    """
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        # FIX: Hard used to be 1-50, which made it easier than Normal.
        return 1, 200
    return 1, 100


def parse_guess(raw):
    """
    Turn the text a player typed into an integer guess.

    Surrounding spaces are ignored and decimals are cut off toward zero
    ("7.9" becomes 7). Negative numbers are accepted here; deciding whether
    a guess is in range is left to the caller.

    Args:
        raw: The raw text from the input box, or None.

    Returns:
        A tuple (ok, guess_int, error_message):
            ok: True if the text was a usable number.
            guess_int: The integer guess, or None when ok is False.
            error_message: A message for the player, or None when ok is True.
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
    Compare a guess to the secret number.

    Args:
        guess: The player's guess as an int.
        secret: The secret number as an int.

    Returns:
        A tuple (outcome, message). The outcome is "Win", "Too High" or
        "Too Low", and the message is the hint to show the player.
    """
    # FIX: The hint messages were swapped ("Too High" used to say
    # "Go HIGHER!"). The old string-comparison fallback was removed because
    # app.py now always passes an int secret.
    if guess == secret:
        return "Win", "🎉 Correct!"
    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """
    Update the score after a guess.

    A win earns 100 - 10 * (attempt_number + 1) points, never less than 10.
    Every wrong guess costs 5 points.

    Args:
        current_score: The score before this guess.
        outcome: "Win", "Too High" or "Too Low".
        attempt_number: Which valid attempt this was, starting at 1.

    Returns:
        The new score as an int. An unknown outcome leaves it unchanged.
    """
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


def get_temperature(guess: int, secret: int, low: int, high: int):
    """
    Return a hot/cold label showing how close a guess is to the secret.

    Closeness is measured as a fraction of the whole range, so being 10 away
    is "hot" on Easy (1-20) but only "warm" on Hard (1-200).

    Args:
        guess: The player's guess.
        secret: The secret number.
        low: Lowest number in the current range.
        high: Highest number in the current range.

    Returns:
        A label with an emoji, from "Burning hot" down to "Freezing cold".
    """
    span = max(high - low, 1)  # avoid dividing by zero on a one-number range
    ratio = abs(guess - secret) / span

    if ratio <= 0.05:
        return "🔥 Burning hot!"
    if ratio <= 0.15:
        return "🌶️ Hot"
    if ratio <= 0.30:
        return "🙂 Warm"
    if ratio <= 0.50:
        return "❄️ Cold"
    return "🧊 Freezing cold!"
