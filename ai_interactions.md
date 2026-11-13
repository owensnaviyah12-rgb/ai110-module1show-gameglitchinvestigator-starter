# AI Interactions Log

> Stretch-feature log. Each section below matches one stretch feature.

---

## Agent Workflow (SF8)

**Tool used:** Claude (chat). I applied its code changes to my files by hand
and ran everything in GitHub Codespaces.

**What task did you give the agent?**

I gave the AI my assignment rubric and my code and asked it to help me earn
every point, including the stretch features. For the feature expansion I
asked it to add three things to the game: a guess history table, hot/cold
hints with emojis, and an "Attempts left" banner that updates right after
each guess. I also asked it to fix invalid guesses using up an attempt.

**Files modified:** `app.py`, `logic_utils.py`, `tests/test_game_logic.py`

**What did the agent do?**

- `logic_utils.py`: added `get_temperature(guess, secret, low, high)`, which
  returns an emoji label based on how far the guess is from the secret as a
  fraction of the range. It also gave every function a full docstring with
  Args and Returns.
- `app.py`:
  - Moved `attempts += 1` so it only runs for valid guesses.
  - Added `st.empty()` placeholders and a `refresh_status_panels()` function
    so the banner and debug panel show the newest numbers.
  - Stored each valid guess in `history` as a dictionary with the attempt,
    guess, result and heat label.
  - Showed the history with `st.dataframe`.
  - Replaced `st.stop()` with `if / elif` so the page always finishes
    drawing.
- `tests/test_game_logic.py`: added edge-case tests for `parse_guess`,
  `check_guess`, `update_score` and `get_temperature`.

**What did you have to verify or fix manually?**

- My first paste into `app.py` kept the old `if submit:` block, an `else:`
  with the wrong indentation and the old duplicate code, which would have
  caused a `SyntaxError`. I removed the leftovers and pasted the corrected
  block.
- The test functions had been pasted into the bottom of `app.py`, where
  pytest never runs them, so I moved them into the test file.
- pytest failed with "import file mismatch" because my repo had two files
  named `test_game_logic.py`, one in `test/` and one in `tests/`. I deleted
  the extra folder with `git rm -r test` and cleared the caches.
- Some terminal commands were written for PowerShell and did not work in the
  Codespaces bash terminal (`type`, `Select-String`, backslash paths), so I
  switched to `cat`, `grep` and forward slashes.
- I confirmed the result by running `python -m pytest -v` in Codespaces:
  44 passed.

---

## Test Generation (SF7)

**Prompt used:** "Here is my rubric and my `logic_utils.py`. Write pytest
edge-case tests for non-numeric strings, negative numbers and empty input so
I earn the Advanced Edge-Case Testing stretch."

**Result:** `python -m pytest -v` collected 44 items and all passed
(`44 passed in 0.12s`, Python 3.14.2 in Codespaces).

| Edge Case | Test | Did It Pass? | Reasoning |
|---|---|---|---|
| Empty, whitespace and `None` | `test_parse_guess_rejects_empty_input` | Yes | A blank box is the most common mistake, and it must show "Enter a guess." instead of crashing |
| Non-numeric text (`abc`, `12abc`, `1e3`, `inf`, `nan`, `1,000`) | `test_parse_guess_rejects_non_numeric_strings` | Yes | `int()` and `float()` accept some surprising strings, so each risky one is pinned down |
| Negative, decimal and padded numbers | `test_parse_guess_accepts_negative_decimal_and_padded` | Yes | Documents that `-5` is accepted, `7.9` becomes 7 and spaces are ignored |
| Overflowing decimal | `test_parse_guess_handles_overflowing_decimal` | Yes | `int(float(...))` raises `OverflowError` on infinity, and the game must catch it |
| Negative guess vs secret | `test_check_guess_negative_guess_is_too_low` | Yes | A negative guess is below any secret, so it must say "Too Low" |
| Exact match | `test_check_guess_exact_match_wins` | Yes | The win path must not depend on the hint branches |
| Wrong guesses on every attempt | `test_wrong_guess_always_costs_five` | Yes | Guards against the old bug that added +5 on even-numbered attempts |
| Score floor | `test_win_score_drops_with_attempts_but_never_below_ten` | Yes | A late win must still earn at least 10 points |
| Hard vs Normal range | `test_hard_is_harder_than_normal` | Yes | Guards against the old 1–50 Hard range |
| Hot/cold labels | `test_temperature_*` | Yes | Checks each label, the range scaling and the one-number range |

I also checked these cases by hand in the running app:

| Manual check | Prompt used | What I did | Did It Pass? |
|---|---|---|---|
| Invalid input | "How should the guessing game handle a non-number input?" | Entered letters and confirmed an error shows | Yes |
| Maximum attempts | "Check what happens when the player reaches the attempt limit." | Made wrong guesses until the limit and confirmed the game ends | Yes |
| Correct guess | "Test what should happen when the player guesses the secret number." | Entered the secret and confirmed a win and a score | Yes |

---

## Linting & Style (SF9)

**Prompt used:**

```
Review my Python code for PEP 8 problems and style issues. Add professional
docstrings with Args and Returns to every function in logic_utils.py.
```

**Commands run:**

```
python -m flake8 ../starter_run/app.py ../starter_run/logic_utils.py > lint_before.txt
python -m flake8 app.py logic_utils.py tests/test_game_logic.py > lint_after.txt
```

**Linting output before** (flake8 on the original starter code):

```
../starter_run/app.py:4:1: E302 expected 2 blank lines, found 1
../starter_run/app.py:67:1: E305 expected 2 blank lines after class or function definition, found 1
../starter_run/logic_utils.py:3:80: E501 line too long (87 > 79 characters)
../starter_run/logic_utils.py:12:80: E501 line too long (87 > 79 characters)
../starter_run/logic_utils.py:21:80: E501 line too long (87 > 79 characters)
../starter_run/logic_utils.py:26:80: E501 line too long (87 > 79 characters)
```

**Linting output after:**

```
cat lint_after.txt
flake8 exit code: 1
app.py:5:1: F401 'logic_utils.update_score' imported but unused
logic_utils.py:136:12: F821 undefined name 'current_score'
```

**Changes the AI suggested and I applied:**

- Rewrote every docstring in `logic_utils.py` with Args and Returns.
- Wrapped the long `from logic_utils import ...` line into a multi-line
  import.
- Shortened the `start_new_game` docstring to fit 79 characters.
- Removed the stray `f` from `"Out of attempts! "`, which had nothing to
  fill in.
- Added the two blank lines PEP 8 wants around functions and removed
  trailing whitespace.

**Suggestion I did not apply:** an AI review said my f-strings were
malformed, with `f"Range: ***{***low***}***..."` as the example. I checked the
lines in `app.py`, found them valid, and left them unchanged. The asterisks
were bold markdown in the chat, not part of my code.

---

## Model Comparison (SF11)

**Task given to both models:**

I gave two AI models the same Streamlit guessing game code and asked each to
find the bugs and suggest fixes. I compared them on one bug: `app.py`
converted the secret number from an integer to a string on even-numbered
attempts, so `check_guess` compared text instead of numbers.

| | Model A | Model B |
|---|---|---|
| **Model name** | GPT-5.6 Luna | Claude Sonnet 4.5 |
| **Response summary** | Found syntax and formatting errors, the integer-to-string bug, attempt-counting problems and game-reset problems, and returned a full revised version of the code | Found similar issues, recommended keeping the secret as an integer, improving the attempt counter and resetting the game state on a new game |
| **Fix for the string bug** | Keep the secret as an int so the guess is compared to it as a number | Keep the secret as an int so the guess is compared to it as a number |
| **More Pythonic?** | Tie | Tie |
| **Clearer explanation?** | Yes | Less clear |

**Which more Pythonic?** It was a tie. Both models gave the same core fix:
remove the string conversion so the comparison is int against int, with no
workarounds or extra conversions. The difference was in how the answers were
presented, not in the code.

**Which explanation was easier to understand?** Model A. It explained each
problem clearly, gave specific fixes and organized the revised code so I could
follow how the game logic fit together.

**Which did you prefer and why?** I preferred GPT-5.6 Luna because the
response explained the problems in my code clearly and provided specific
fixes. It also organized the revised code in a way that made it easier for me
to understand how the game logic worked.