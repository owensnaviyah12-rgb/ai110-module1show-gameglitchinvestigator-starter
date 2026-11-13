# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🎯 Purpose

This is a number-guessing game built with Streamlit. The player picks a
difficulty (Easy, Normal or Hard), which sets a number range and an attempt
limit. They then guess until they find the secret number or run out of
attempts, earning more points the faster they win. The starter version was
full of AI-written bugs, and this project finds, documents and fixes them.

| Difficulty | Range | Attempts |
|---|---|---|
| Easy | 1–20 | 6 |
| Normal | 1–100 | 8 |
| Hard | 1–200 | 5 |

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the app: `python -m streamlit run app.py`
3. Run the tests: `python -m pytest -v`

## 🐞 Bugs Found

| # | Bug | Code-level cause | Expected | Actual |
|---|-----|------------------|----------|--------|
| 1 | Hints were backwards | `check_guess` paired `"Too High"` with `"Go HIGHER!"` and `"Too Low"` with `"Go LOWER!"` | Too High tells the player to go lower | Player was told the opposite |
| 2 | Secret compared as text | `app.py` converted `st.session_state.secret` to a string on every other attempt before calling `check_guess` | Numeric comparison on every attempt | `"9" > "57"` is true as text, so hints were wrong on alternating guesses |
| 3 | New Game ignored difficulty | The New Game handler called `random.randint(1, 100)` | Secret drawn from the selected range (Easy is 1–20) | Secret could fall outside the stated range |
| 4 | Hard was easier than Normal | `get_range_for_difficulty("Hard")` returned `1, 50` | Hard has a wider range than Normal | Hard was narrower (1–50 vs 1–100) |
| 5 | Wrong guesses could raise the score | `update_score` added +5 for `"Too High"` on even-numbered attempts | Every wrong guess costs points | Score went up after some wrong guesses |
| 6 | Invalid guesses used an attempt | `attempts += 1` ran before `parse_guess` validated the input | Bad input shows an error and costs nothing | "Attempts left" dropped on empty or non-numeric input |
| 7 | Instructions showed the wrong range | On-screen text hardcoded "between 1 and 100" | Text uses the real `low` and `high` | Easy and Hard showed 1–100 |

## 🔧 Fixes Applied

- **Refactor:** moved `get_range_for_difficulty`, `parse_guess`, `check_guess`
  and `update_score` out of `app.py` into `logic_utils.py` and imported them
  back, so the logic can be tested without running Streamlit.
- **Hints (bug 1):** `check_guess` now returns `"Go LOWER!"` for `"Too High"`
  and `"Go HIGHER!"` for `"Too Low"`. This works because the message now
  matches the direction of the comparison.
- **Secret as text (bug 2):** removed the string conversion, so `check_guess`
  always compares two ints.
- **New Game range (bug 3):** `start_new_game()` calls
  `get_range_for_difficulty(difficulty)` and draws from that range. It also
  resets status, score and history.
- **Hard range (bug 4):** Hard changed from 1–50 to 1–200, so it is now
  harder than Normal (1–100).
- **Scoring (bug 5):** `update_score` now subtracts 5 for every wrong guess.
  The old even/odd rule that added points is gone.
- **Invalid guesses (bug 6):** `app.py` calls `parse_guess` first and only
  increments `attempts` in the valid-guess branch.
- **Instructions (bug 7):** the on-screen text uses the actual `low` and
  `high` values.

## 📸 Demo Walkthrough

1. The user selects "Normal". The app shows range 1 to 100 and 8 attempts.
2. The user enters 40 and clicks "Submit Guess 🚀". The app says "Go HIGHER!"
   with a hot/cold label and adds a row to the guess history table.
3. The user enters 70 and gets "Go LOWER!". "Attempts left" drops
   immediately.
4. The user types `abc` and clicks Submit. An error appears, and attempts
   do not change.
5. The user enters the secret number. The app shows balloons, the win
   message and the final score.
6. "New Game 🔁" draws a new secret from the selected difficulty's range and
   resets attempts, score and history.

## 🧪 Test Results

```
============================================================================ test session starts =============================================================================
platform linux -- Python 3.14.2, pytest-9.2.0, pluggy-1.7.0 -- /home/codespace/.python/current/bin/python
cachedir: .pytest_cache
rootdir: /workspaces/ai110-module1show-gameglitchinvestigator-starter
plugins: platformdirs-4.14.0, anyio-4.15.1
collected 44 items                                                                                                                                                           

tests/test_game_logic.py::test_too_high_returns_correct_hint PASSED                                                                                                    [  2%]
tests/test_game_logic.py::test_too_low_returns_correct_hint PASSED                                                                                                     [  4%]
tests/test_game_logic.py::test_easy_range_is_1_to_20 PASSED                                                                                                            [  6%]
tests/test_game_logic.py::test_hard_is_harder_than_normal PASSED                                                                                                       [  9%]
tests/test_game_logic.py::test_unknown_difficulty_falls_back_to_normal PASSED                                                                                          [ 11%]
tests/test_game_logic.py::test_parse_guess_rejects_empty_input[] PASSED                                                                                                [ 13%]
tests/test_game_logic.py::test_parse_guess_rejects_empty_input[   ] PASSED                                                                                             [ 15%]
tests/test_game_logic.py::test_parse_guess_rejects_empty_input[\t\n] PASSED                                                                                            [ 18%]
tests/test_game_logic.py::test_parse_guess_rejects_empty_input[None] PASSED                                                                                            [ 20%]
tests/test_game_logic.py::test_parse_guess_rejects_non_numeric_strings[abc] PASSED                                                                                     [ 22%]
tests/test_game_logic.py::test_parse_guess_rejects_non_numeric_strings[12abc] PASSED                                                                                   [ 25%]
tests/test_game_logic.py::test_parse_guess_rejects_non_numeric_strings[1e3] PASSED                                                                                     [ 27%]
tests/test_game_logic.py::test_parse_guess_rejects_non_numeric_strings[inf] PASSED                                                                                     [ 29%]
tests/test_game_logic.py::test_parse_guess_rejects_non_numeric_strings[nan] PASSED                                                                                     [ 31%]
tests/test_game_logic.py::test_parse_guess_rejects_non_numeric_strings[--5] PASSED                                                                                     [ 34%]
tests/test_game_logic.py::test_parse_guess_rejects_non_numeric_strings[1.2.3] PASSED                                                                                   [ 36%]
tests/test_game_logic.py::test_parse_guess_rejects_non_numeric_strings[1,000] PASSED                                                                                   [ 38%]
tests/test_game_logic.py::test_parse_guess_rejects_non_numeric_strings[five] PASSED                                                                                    [ 40%]
tests/test_game_logic.py::test_parse_guess_rejects_non_numeric_strings[!] PASSED                                                                                       [ 43%]
tests/test_game_logic.py::test_parse_guess_accepts_negative_decimal_and_padded[-5--5] PASSED                                                                           [ 45%]
tests/test_game_logic.py::test_parse_guess_accepts_negative_decimal_and_padded[-0-0] PASSED                                                                            [ 47%]
tests/test_game_logic.py::test_parse_guess_accepts_negative_decimal_and_padded[7.9-7] PASSED                                                                           [ 50%]
tests/test_game_logic.py::test_parse_guess_accepts_negative_decimal_and_padded[-7.9--7] PASSED                                                                         [ 52%]
tests/test_game_logic.py::test_parse_guess_accepts_negative_decimal_and_padded[  42  -42] PASSED                                                                       [ 54%]
tests/test_game_logic.py::test_parse_guess_accepts_negative_decimal_and_padded[+7-7] PASSED                                                                            [ 56%]
tests/test_game_logic.py::test_parse_guess_accepts_negative_decimal_and_padded[007-7] PASSED                                                                           [ 59%]
tests/test_game_logic.py::test_parse_guess_handles_overflowing_decimal PASSED                                                                                          [ 61%]
tests/test_game_logic.py::test_check_guess_negative_guess_is_too_low PASSED                                                                                            [ 63%]
tests/test_game_logic.py::test_check_guess_exact_match_wins PASSED                                                                                                     [ 65%]
tests/test_game_logic.py::test_wrong_guess_always_costs_five[Too High-1] PASSED                                                                                        [ 68%]
tests/test_game_logic.py::test_wrong_guess_always_costs_five[Too High-2] PASSED                                                                                        [ 70%]
tests/test_game_logic.py::test_wrong_guess_always_costs_five[Too High-3] PASSED                                                                                        [ 72%]
tests/test_game_logic.py::test_wrong_guess_always_costs_five[Too High-4] PASSED                                                                                        [ 75%]
tests/test_game_logic.py::test_wrong_guess_always_costs_five[Too Low-1] PASSED                                                                                         [ 77%]
tests/test_game_logic.py::test_wrong_guess_always_costs_five[Too Low-2] PASSED                                                                                         [ 79%]
tests/test_game_logic.py::test_wrong_guess_always_costs_five[Too Low-3] PASSED                                                                                         [ 81%]
tests/test_game_logic.py::test_wrong_guess_always_costs_five[Too Low-4] PASSED                                                                                         [ 84%]
tests/test_game_logic.py::test_win_score_drops_with_attempts_but_never_below_ten PASSED                                                                                [ 86%]
tests/test_game_logic.py::test_unknown_outcome_leaves_score_unchanged PASSED                                                                                           [ 88%]
tests/test_game_logic.py::test_temperature_close_guess_is_burning_hot PASSED                                                                                           [ 90%]
tests/test_game_logic.py::test_temperature_far_guess_is_freezing_cold PASSED                                                                                           [ 93%]
tests/test_game_logic.py::test_temperature_middle_distances PASSED                                                                                                     [ 95%]
tests/test_game_logic.py::test_temperature_scales_with_range_size PASSED                                                                                               [ 97%]
tests/test_game_logic.py::test_temperature_single_number_range_does_not_crash PASSED                                                                                   [100%]
============================== 44 passed in 0.07s ==============================
```

## 🚀 Stretch Features

### Advanced edge-case testing
`test_game_logic.py` covers empty and whitespace input, `None`, non-numeric
strings (`abc`, `12abc`, `1e3`, `inf`, `nan`), negative numbers, decimals,
padded input and an overflowing decimal. The passing output is in the Test
Results section above. Prompts and reasons are in `ai_interactions.md`.

### Feature expansion
Added a guess history table, hot/cold hints and a live attempts banner. See
the Agent Workflow section of `ai_interactions.md`.

### Professional documentation and style
Every function in `logic_utils.py` has a docstring with Args and Returns, and
the code was checked with flake8:

```
app.py:5:1: F401 'logic_utils.update_score' imported but unused
logic_utils.py:136:12: F821 undefined name 'current_score'
```

### Enhanced game UI and formatting
- `get_temperature` (in `logic_utils.py`) returns an emoji label from
  "🔥 Burning hot!" to "🧊 Freezing cold!". It measures distance as a
  fraction of the range, so the same distance feels different on Easy and
  Hard.
- The hint in `app.py` now shows the direction and the hot/cold label together.
- A "Guess history" table (`st.dataframe`) lists the attempt number, guess,
  result and heat for each valid guess.
- `refresh_status_panels` in `app.py` redraws the "Attempts left" banner and
  debug panel at the end of each run, so they never show out-of-date numbers.

### AI model comparison
See the Model Comparison section of `ai_interactions.md`.