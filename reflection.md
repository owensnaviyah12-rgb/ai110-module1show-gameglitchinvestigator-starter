# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

The first time I ran the game ans started guessing, the hints were consistently wrong regards of what I entered (50,90, or 7 as a secret of 57-78). Two concrete bugs surfaced is secret number gets sliently converted to compares strings character by character instead of value. 


**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
|Guessed 50, 90, and 7 against a secret between 57–78 |Hints should correctly say "go higher" or "go lower" based on numeric comparison to the secret |All three guesses returned "Go HIGHER!" or "Go LOWER!" in ways that didn't consistently match the actual numeric relationship to the secret | No error/crash shown in the UI|
|check_guess outcome vs. message pairing (visible directly in code, lines returning "Too High" / "Too Low")|"Too High" outcome should tell the player to go lower; "Too Low" should tell them to go higher |Messages are swapped: "Too High" returns "Go HIGHER!", "Too Low" returns "Go LOWER!" |None — logic error
|Selected "Easy" difficulty (range 1–20), then clicked "New Game 🔁" |New secret should still be drawn from 1–20 |new_game handler calls random.randint(1, 100), ignoring the selected difficulty's range |None — no error |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

I decided a bug was confirmed once the actual in app behavior that matched a concrete explanation of why the code would produce the result to assuming the Claude's first bug was complete or corrrect. CLaude helped me design a manual testing rather than a response of " I tested manual reproduction test rather than a formal pytest. 
---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
Streamlit reruns the whole script top to bottom every time you interact with a widget, so any value you want to persist across those reruns like the secret number or attempt count. 
---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

One habit from this project I want to keep using is verfiying an AI bug report against real, reproducible behavior instead of accepting the list as complete. When Claude intially named three bugs that took me actually running guess to ensure the report result were excat before being impactful bug. One thing I'd do differently next time is give that AI concrete input and ouput to eariler in the process to asking it to speculate about what might be wrong. The project changed by what i think about AI genereated code to not find ask AI to find the bug once and trust what it says. Bugs can be hidden by other bugs to confiriming fixed that reguire running the code yourself. 