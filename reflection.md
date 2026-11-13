## 💭 Reflection: Game Glitch Investigator

## 1. What was broken when you started?

The first time I ran the game and started guessing, the hints were wrong in a confusing way, so I opened the Developer Debug Info panel and compared my guesses to the real secret. I found several separate bugs. The biggest were backwards hint messages and a secret number that was silently turned into text on every other attempt, so it was compared character by character instead of by value. I also found that New Game ignored the difficulty range, Hard was easier than Normal, wrong guesses could add points, and invalid input used up an attempt.

**Trace of the original starter code** (commit `<<FILL: first commit hash>>`):

```text
$ python -m streamlit run app.py          # original starter code
### Post-fix game session

Exported from the app's history table (`session_history.csv`). Normal
difficulty (range 1–100, 8 attempts). The secret was 44.

```text
Attempt  Guess  Result    Heat
1        46     Too High  🔥 Burning hot!
2        47     Too High  🔥 Burning hot!
3        48     Too High  🔥 Burning hot!
4        40     Too Low   🔥 Burning hot!
5        50     Too High  🌶️ Hot
6        49     Too High  🌶️ Hot
7        52     Too High  🌶️ Hot
8        35     Too Low   🌶️ Hot
```

Every hint matches the real number: guesses above 44 say Too High and guesses
below 44 say Too Low, and the hot/cold label gets warmer as the guess nears 44.
All 8 guesses were valid, and the game ended after the 8th attempt.
$ python -c "print('9' > '57', 9 > 57)"
True False
```

**Bug Reproduction Log**

| Input | Expected Behavior | Actual Behavior | Root Cause (code) |
|-------|-------------------|-----------------|-------------------|
| Guessed 50, 90 and 7 with the secret between 57 and 78 | 50 and 7 say "Go HIGHER!", 90 says "Go LOWER!" | Hints did not match the real numbers on every other guess | `app.py` converted `st.session_state.secret` to a string on even attempts, so `check_guess` compared text (`'9' > '57'` is `True`) |
| `check_guess(60, 50)` | "Too High" with "Go LOWER!" | "Too High" with "Go HIGHER!" | The messages in `check_guess` were swapped between the two outcomes |
| Selected Easy (1–20), then clicked "New Game 🔁" | New secret between 1 and 20 | Secret could be up to 100 | The New Game handler called `random.randint(1, 100)` |
| Selected Hard, read the range in the sidebar | Hard is wider than Normal | Hard showed 1–50, narrower than Normal's 1–100 | `get_range_for_difficulty` returned `1, 50` for Hard |
| Made wrong "Too High" guesses on attempts 1, 2, 3, 4 | Score drops by 5 each time | Score went up on even-numbered attempts | `update_score` added +5 for "Too High" when `attempt_number % 2 == 0` |
| Left the box empty (or typed `abc`) and clicked Submit | Error message, attempts unchanged | Error message, but "Attempts left" dropped by 1 | `attempts += 1` ran before `parse_guess` validated the input |

---

## 2. How did you use AI as a teammate?

I used Claude as my main AI assistant, both as a tutor and as a code reviewer.

**An AI explanation of a bug.** I asked Claude to explain a line I didn't understand, `if attempt_number % 2 == 0`. It explained that `%` gives the remainder after dividing, so the condition is true on every even-numbered attempt, and that the starter used it to add +5 points for a "Too High" guess on even attempts. That means a wrong guess could raise the score, which is a real bug.

**A suggestion that was correct.** Claude said the secret was being converted to a string on every other attempt, which would make `check_guess` compare text instead of numbers. This was correct, and I confirmed it two ways. In the running game, the hints were wrong on alternating guesses. In the terminal, `'9' > '57'` is `True` while `9 > 57` is `False`. The fix was to keep the secret as an int.

**A suggestion I rejected.** One AI review said my code had "malformed f-string formatting" such as `f"Range: ***{***low***}***..."`. I rejected this after checking the actual line in `app.py`. The f-strings were valid, and the asterisks were bold markdown from the chat window, not part of my code. Changing them would have meant "fixing" something that wasn't broken.

**A suggestion I revised.** An AI log said invalid guesses "no longer counted as attempts", but my code still had `attempts += 1` above `parse_guess`, so empty and non-numeric input still used up an attempt. I moved the increment into the valid-guess branch and checked it by submitting `abc` and watching "Attempts left".

I also used Claude to check my work against the assignment rubric so I could see which sections still needed evidence.

---

## 3. Debugging and testing your fixes

I treated a bug as fixed and teaching tool  when I could see the wrong behavior disappear in the running app and also explain which line caused it. I used pytest as the second check: the tests in `test_game_logic.py` cover the swapped hints, the Easy and Hard ranges, the scoring rule (every wrong guess costs 5) and edge cases such as empty input, `abc`, negative numbers and an overflowing decimal. All 44 tests pass with `python -m pytest -v`. Claude helped me design the edge cases and explained why each one mattered, for example that `parse_guess` has to catch `OverflowError` or a huge decimal would crash the game. Some things, like the "Attempts left" banner, I could only check by hand in the app.

---

## 4. What did you learn about Streamlit and state?

Streamlit reruns the whole script from top to bottom every time you click a button or type in a widget, so ordinary variables are reset on every rerun. Anything that must survive, like the secret number, the attempt count and the score, has to live in `st.session_state`. I also learned that the page is drawn in order, which is why my "Attempts left" banner showed old numbers until I filled it in at the end of the script with `st.empty()` placeholders.

---

## 5. Looking ahead: your developer habits


One habit I want to keep is checking an AI's bug report against real, reproducible behavior instead of accepting its list as complete, because bugs can hide behind other bugs and confirming a fix means running the code myself. I also learned to give AI tools like ChatGPT and Claude extra context up front, such as the assignment rubric or grading scheme, which helps them understand the details of what I actually need. Next time I would break down the logic myself earlier: read through the code line by line, remove any code or lines that aren't needed, and revise it on my own, then go back to the AI with specific questions about the logic. I would also make small commits as I go and use them to see what the output produces and whether it matches what the assignment expects. This project changed how I see AI-generated code: it is a starting point to question and test, not an answer to trust the first time.
