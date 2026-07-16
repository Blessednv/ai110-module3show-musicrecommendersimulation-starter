# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

Real-world music recommenders, like the ones behind Spotify or YouTube Music, work by turning each song into a set of numbers that describe how it sounds and feels, then comparing those numbers to what a listener seems to want. They don't actually "understand" music the way a person does. They just find patterns: which songs are close together in energy, mood, and style, and which ones tend to get played together. My version is a simplified version of that idea. Instead of learning from millions of listening histories, it uses a small, hand-picked catalog of songs and a single user profile that states preferences directly. It prioritizes matching a song's genre and mood first, since those say the most about overall "vibe," and then fine-tunes the ranking using numerical closeness on energy and a preference for acoustic vs. non-acoustic sound. The goal isn't to build something as powerful as a real streaming service, but to show, in a small and readable way, how raw data can be turned into a ranked list of recommendations.

**Song features:**
- `genre` — the song's musical style/category (e.g., pop, lofi, jazz)
- `mood` — a labeled emotional tag (e.g., happy, chill, intense)
- `energy` — how intense or high-arousal the song feels (0-1)
- `valence` — how positive or upbeat the song feels (0-1)
- `tempo_bpm` — the song's speed in beats per minute
- `danceability` — how suited the song is to dancing (0-1)
- `acousticness` — how acoustic vs. electronically produced the song sounds (0-1)

**UserProfile fields:**
- `favorite_genre` — the genre the user wants to hear
- `favorite_mood` — the mood the user wants to hear
- `target_energy` — a target energy level (0-1)
- `likes_acoustic` — whether the user prefers acoustic-leaning songs (true/false)

**How the Recommender scores a song:**
For each song, it checks whether `genre` matches `favorite_genre` and whether `mood` matches `favorite_mood`, giving points for each match. For `energy`, it doesn't just reward high values — it rewards whichever value is *closest* to `target_energy`, using a simple "1 minus the distance" formula. `likes_acoustic` acts as a smaller bonus/penalty based on whether the song's `acousticness` is high or low. All of these pieces are combined into one weighted score per song, with genre weighted highest, since it says the most about overall vibe, mood weighted a bit less, and energy/acousticness filling in the finer-grained match.

**How songs get recommended:**
Once every song in the catalog has a score, the Recommender sorts the full list from highest score to lowest and returns the top N songs. The scoring rule decides how good a single song is; the ranking rule decides the order the user actually sees.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



