# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [ ] This is a number - guessing games built with Streamlit.The player selects a difficulty (Easy, Normal, or Hard), which sets a numeric range and an attempt limit. The player then guesses numbers until they either guess the secret number correctly or run out of attempts, earning points based on how quickly they win.

- [ ] Detail which bugs you found.check_guess` returned the outcome `"Too High"` paired with the message `"Go HIGHER!"`, and `"Too Low"` paired with `"Go LOWER!"`. This told the player the opposite of what they should do next. clicking "New Game 🔁" always redrew the secret from `random.randint(1, 100)`, regardless of whether the player was on Easy (1–20) or Hard (1–50), so restarting a game on those difficulties could produce a secret outside the stated range.`app.py` converted `st.session_state.secret` to a string before calling `check_guess` on every other attempt, which broke numeric comparison and produced incorrect hints (this bug is documented but not yet fixed).
- [ ] Explain what fixes you applied. Refactored `get_range_for_difficulty`, `parse_guess`, `check_guess`, and `update_score` out of `app.py` into a new `logic_utils.py` module, and imported them back into `app.py`.
- Fixed the inverted hint messages in `check_guess` so `"Too High"` now correctly returns `"Go LOWER!"` and `"Too Low"` returns `"Go HIGHER!"`.
- Fixed the "New Game" button to call `get_range_for_difficulty(difficulty)` and use that range instead of a hardcoded `1, 100`.
- Also corrected the on-screen instructions, which hardcoded "between 1 and 100" regardless of difficulty, to use the actual `low`/`high` values.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. User selects "Normal" difficulty from the sidebar; the app shows a range of 1 to 100 and an attempt limit of 8.
2. User enters a guess of 40 and clicks "Submit Guess 🚀" → the app returns "Too Low" with the message "Go HIGHER!"
3. User enters a guess of 70 → the app returns "Too High" with the message "Go LOWER!"
4. Score updates after each guess based on the outcome and attempt number.
5. User continues guessing until entering the correct secret number → the app shows a win message, displays balloons, and reveals the final score.
6. If the user selects "New Game 🔁" instead, a new secret number is drawn from the correct range for the currently selected difficulty, and attempts reset to 0.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
# Paste your pytest output here, e.g.:================== test session starts ===================
platform win32 -- Python 3.13.14, pytest-9.1.1, pluggy-1.6.0 -- c:\Users\owens\OneDrive\Documents\GitHub\ai110-module1show-gameglitchinvestigator-starter\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\owens\OneDrive\Documents\GitHub\ai110-module1show-gameglitchinvestigator-starter
plugins: anyio-4.14.2
collected 0 items                                         

================= no tests ran in 1.10s =================
# pytest tests/
# ========================= X passed in 0.XXs =========================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
