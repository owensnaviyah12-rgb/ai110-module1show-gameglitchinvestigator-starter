# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

I asked the AI to review and revise my Streamlit guessing game code. I wanted it to identify bugs, fix errors, and make sure the game worked correctly with the selected difficulty, attempts, scoring, and secret number.

<!-- Describe the goal you asked the agent to accomplish -->


**What did the agent do?**
The AI reviewed the main Streamlit file and:

Fixed incorrect f-string formatting.
Fixed the secret number being converted from an integer to a string.
Changed the attempt counter to start at 0.
Made invalid guesses not count as attempts.
Updated the New Game button to reset the game correctly.
Added logic to reset the game when the difficulty changes.
Improved the attempts-left calculation.
Cleaned up comments and removed the unresolved FIXME after fixing the issue.
<!-- List the steps the agent took (files edited, commands run, etc.) -->


**What did you have to verify or fix manually?**

<!-- Describe anything the agent got wrong or that required human review -->

I reviewed the revised code to make sure the changes matched the requirements of the project. I also needed to verify that the game still used the functions from logic_utils.py, that the difficulty settings worked correctly, and that the guessing, scoring, and game-over conditions behaved as expected.
---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|Invalid input|"How should the guessing game handle a non-number input?"|Enter letters instead of a number and verify that an error is displayed without using an attempt.|yes |Invalid input should not count as a valid guess or break the game.|
|Maximum attempts |"Check what happens when the player reaches the attempt limit." |Make incorrect guesses until the attempt limit is reached and verify that the game ends. |Yes|The game should change to a lost state after the allowed number of attempts |
|Correct guess |"Test what should happen when the player guesses the secret number." |Enter the correct secret number and verify that the player wins and receives a score. | Yes | A correct guess should end the game with a win.|
| | | | | |

---

## Linting & Style (SF9)

> Document your use of AI for linting or code style improvements.

**Prompt used:** 

```
<!-- Paste the prompt you gave the AI -->
```Review my Streamlit Python code for syntax errors, formatting problems, and code style issues. Identify anything that could cause the program to fail or make the code harder to read.

**Linting output before:**

```
<!-- Paste relevant linter warnings/errors -->
```
The code contained malformed f-string formatting such as: f"Range: ***{***low***}*** to ***{***high***}***" The code also converted the secret number from an integer to a string on even-numbered attempts, which could cause problems when comparing the guess to the secret number.

**Changes applied:** 

<!-- Describe what you changed based on the AI's suggestions -->

--- I corrected the f-string formatting and kept the secret number as an integer so it could be compared correctly with the user's numeric guess. I also cleaned up the formatting and comments to make the code easier to read and maintain.

## Model Comparison (SF11)

> Compare two AI models on the same task.

**Task given to both models:**

<!-- Describe what you asked each model to do -->
I asked two AI models to review the same Streamlit guessing game code, identify bugs, and suggest improvements to make the game function correctly.

| | Model A | Model B |
|-||---------|
| **Model name** |GPT-5.6 Luna | Claude Sonnet 4.5 |
| **Response summary** |Identified syntax and formatting errors, the integer-to-string bug, attempt-counting issues, and game-reset problems. It also provided a revised version of the code |Identified similar issues and recommended keeping the secret number as an integer, improving the attempt counter, and resetting the game state when starting a new game.. |
| **More Pythonic?** |  Yes |  yes |
| **Clearer explanation?** |Yes | Yes |

**Which did you prefer and why?**

<!-- Your conclusion --> I preferred GPT-5.6 Luna because the response explained the problems in my code clearly and provided specific fixes. It also organized the revised code in a way that made it easier for me to understand how the game logic worked.
