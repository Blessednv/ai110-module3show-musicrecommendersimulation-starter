# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agentic Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

<!-- Describe the goal you asked the agent to accomplish -->

**Prompts used:**

<!-- Paste the key prompts you gave the agent -->

**What did the agent generate or change?**

<!-- List the files edited, code generated, or commands run -->

**What did you verify or fix manually?**

<!-- Describe anything the agent got wrong or that required human review -->

---

## Design Pattern (SF10)

> Document how AI helped you choose or implement a design pattern.

**Which design pattern did you use?**

<!-- e.g., Strategy, Factory, Observer, etc. -->

**How did AI help you brainstorm or implement it?**

<!-- Describe the conversation or suggestions that led to your decision -->

**How does the pattern appear in your final code?**

<!-- Point to the relevant class or method -->

---

## Challenge 3: Diversity and Fairness Logic

**What task did you give the agent?**

Add a rule to `recommend_songs()` in `src/recommender.py` that penalizes a song's score if its artist already has a song in the top-k list being built, so the same artist can't dominate multiple slots unless clearly still the best option.

**Prompt used:**

"In `recommend_songs()`, add a rule that penalizes a song's score by a fixed amount if its artist already appears among the songs already selected for the top-k list, applied greedily as the list is built one song at a time, not just penalizing duplicates after the fact, since two songs by the same artist could otherwise both land in the top 5."

**What did the agent generate or change?**

- Rewrote `recommend_songs()` to build the top-k list one song at a time (greedy selection) instead of a single sort-and-slice.
- Added an `artist_penalty` parameter (default 1.5) and a `seen_artists` set tracking which artists already have a pick.
- Before each pick, every remaining candidate's effective score is recalculated, subtracting `artist_penalty` if its artist is already in `seen_artists`.
- Appended a `"Diversity penalty (-1.50, artist already in list)"` line to the reasons string whenever the penalty applies, so it shows up in the terminal output.

**What did you verify or fix manually?**

- Ran `pytest` — both existing tests still passed, since they test the separate class-based `Recommender`, not this function.
- Re-ran `python -m src.main` across all profiles and confirmed the penalty actually fires: in the Chill Lofi profile, "Focus Flow" (by LoRoom, the same artist as the already-selected "Midnight Coding") got the -1.50 penalty and dropped to #4 instead of ranking higher on raw score alone.
- Checked that the penalty doesn't compound: a song only takes the flat -1.5 penalty once, regardless of how many same-artist songs were already selected before it.

---

## Challenge 4: Visual Summary Table

**What task did you give the agent?**

Improve the readability of the terminal output in `src/main.py` by replacing the `====`-block print style with a formatted table.

**Prompt used:**

"Suggest a way to format the terminal output as an aligned table with Rank, Title, Artist, Score, and Reasons columns, using plain Python string formatting (no new dependency), and make sure long reason text wraps onto additional lines instead of getting cut off."

**What did the agent generate or change?**

- Modified `print_recommendations()` in `src/main.py` to print a header row and per-song rows using f-string column widths (`:<N` alignment) instead of the old `====` separator blocks.
- Used `textwrap.wrap()` to break long "reasons" strings into multiple lines, printing continuation lines indented under the Reasons column so nothing gets cut off.

**What did you verify or fix manually?**

- Ran `python -m src.main` and visually checked that columns lined up; also ran a small `python -c` check that computed the exact character widths of the header vs. a data row vs. a wrapped continuation line, to confirm the apparent misalignment in the terminal was just font rendering and not an actual bug.
- Confirmed the original starter profile's print block at the top of `main()` was left untouched — only the profiles run through `print_recommendations()` use the new table format.
