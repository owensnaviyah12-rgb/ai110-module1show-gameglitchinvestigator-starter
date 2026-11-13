import random

import streamlit as st

from logic_utils import (
    get_range_for_difficulty,
    parse_guess,
    check_guess,
    update_score,
    get_temperature,
)

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")


def start_new_game():
    """Reset game state and draw a secret from the current range."""
    new_low, new_high = get_range_for_difficulty(difficulty)
    st.session_state.secret = random.randint(new_low, new_high)
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.difficulty = difficulty


# First load: set up a game.
if "secret" not in st.session_state:
    start_new_game()

# FIX: Changing difficulty used to keep a secret from the old range.
if st.session_state.get("difficulty") != difficulty:
    start_new_game()

st.subheader("Make a guess")

# Empty placeholders. They are filled at the END of the script so they
# show the newest numbers instead of last click's numbers.
info_slot = st.empty()
debug_slot = st.empty()


def refresh_status_panels():
    """Redraw the attempts banner and debug panel with current state."""
    info_slot.info(
        f"Guess a number between {low} and {high}. "
        f"Attempts left: {attempt_limit - st.session_state.attempts}"
    )
    with debug_slot.container():
        with st.expander("Developer Debug Info"):
            st.write("Secret:", st.session_state.secret)
            st.write("Attempts:", st.session_state.attempts)
            st.write("Score:", st.session_state.score)
            st.write("Difficulty:", difficulty)
            st.write("History:", st.session_state.history)


raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    # FIX: New Game now uses the selected difficulty's range (it used to be a
    # hardcoded randint(1, 100)) and also resets status, score, and history so
    # the game is playable again after a win or loss.
    start_new_game()
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
elif submit:
    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        # FIX: Invalid input no longer costs an attempt. The counter used to
        # increase before the guess was validated.
        st.error(err)
    else:
        st.session_state.attempts += 1

        # FIX: The secret used to be converted to a string on even-numbered
        # attempts, which broke numeric comparison. It is now always an int.
        outcome, message = check_guess(guess_int, st.session_state.secret)

        heat = ""
        if outcome != "Win":
            heat = get_temperature(
                guess_int, st.session_state.secret, low, high
            )

        st.session_state.history.append(
            {
                "Attempt": st.session_state.attempts,
                "Guess": guess_int,
                "Result": outcome,
                "Heat": heat,
            }
        )

        if show_hint:
            st.warning(f"{message} {heat}".strip())

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    "Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

if st.session_state.history:
    st.subheader("Guess history")
    st.dataframe(st.session_state.history, hide_index=True)

refresh_status_panels()

st.divider()
st.caption("Game Glitch Investigator 🎮")