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

**Algorithm Recipe (finalized):**
| Rule | Points |
|---|---|
| Genre match (`song.genre == favorite_genre`) | +2.0 |
| Mood match (`song.mood == favorite_mood`) | +1.0 |
| Energy similarity: `2.0 * (1 - abs(song.energy - target_energy))` | up to +2.0 |
| Acousticness fit (high if `likes_acoustic`, low if not) | +1.0 |

Max possible score: **6.0**

**Potential biases:**
This system might over-prioritize genre and mood matches, since those are worth the most points, and could bury a song that's a near-perfect energy match but sits in a genre the user didn't list as a favorite. It also assumes a single `favorite_genre` and `favorite_mood` per user, which flattens people who like more than one genre equally. Since the catalog is small and hand-picked, it can't reveal how these weights would hold up against a large, real-world dataset with more overlap between genres and moods.

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

Actual output from `python -m src.main`, using the default profile (`favorite_genre="pop"`, `favorite_mood="happy"`, `target_energy=0.8`, `likes_acoustic=False`):

```
Loaded songs: 18

Top recommendations:

========================================
1. Sunrise City by Neon Echo
   Score: 5.96
   Because: Genre match (+2.0), Mood match (+1.0), Energy similarity (+1.96), Acousticness match (+1.0)
========================================
2. Gym Hero by Max Pulse
   Score: 4.74
   Because: Genre match (+2.0), Energy similarity (+1.74), Acousticness match (+1.0)
========================================
3. Rooftop Lights by Indigo Parade
   Score: 3.92
   Because: Mood match (+1.0), Energy similarity (+1.92), Acousticness match (+1.0)
========================================
4. Night Drive Loop by Neon Echo
   Score: 2.90
   Because: Energy similarity (+1.90), Acousticness match (+1.0)
========================================
5. Storm Runner by Voltline
   Score: 2.78
   Because: Energy similarity (+1.78), Acousticness match (+1.0)
========================================
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

A recommender system like this one turns data into predictions by reducing everything about a song, and everything about a listener, into a small set of numbers and labels, then measuring how closely they line up. Genre and mood become simple category matches, energy and acousticness become numeric distances, and every one of those pieces gets converted into points that are added together into a single score. The song with the highest total score is treated as the "best" prediction, even though that score is really just an arithmetic proxy for taste, not any deeper understanding of what a listener actually wants to hear.

- about where bias or unfairness could show up in systems like this

Bias and unfairness can show up in a system like this in ways that are easy to miss just by reading the code. In this project, one bias came from the data itself: several genres had only one song, so any user who preferred that genre received the same result every time, regardless of how well it actually matched their mood or energy. A second bias came from the weighting: genre and mood together were worth enough points that a song could win even with a badly mismatched energy value, meaning the system quietly favored certain kinds of matches over others without ever being explicitly designed to do so. Neither kind of bias was visible from a single test case, it only became clear after comparing many different user profiles side by side.

**What was your biggest learning moment during this project?**
The most significant moment arrived not while writing code, but while comparing outputs across profiles. I had assumed the scoring logic behaved correctly because it produced a plausible list for the default profile. It was only through systematic comparison, testing ten distinct profiles side by side, that I recognized certain songs were winning for reasons entirely unrelated to a genuine match. That experience taught me that testing a single case, however sensible it appears, does not constitute a full evaluation of a scoring rule's behavior.

**How did using AI tools help you, and when did you need to double-check them?**
AI assistance was most useful for two tasks: rapidly proposing edge-case profiles I would not have devised independently, such as the contradictory mood/energy example and the unknown-genre example, and explaining, with the actual weight values, why a particular song had ranked first. I needed to verify each explanation myself rather than accept it outright. In one instance, I confirmed a claim that a genre had only one representative song by counting genre entries directly in the dataset, rather than trusting the summary as given. I also re-ran the recommender after every proposed change to confirm the reported scores matched the actual terminal output, rather than trusting a description of what the change "should" do.

**What surprised you about how simple algorithms can still "feel" like recommendations?**
What surprised me most was how convincingly a handful of conditional checks and one weighted sum could imitate the impression of personal taste. Because the scoring produces a ranked list with a plausible explanation attached to each song, it is easy to mistake consistent behavior for genuinely intelligent judgment. Only by deliberately attempting to break the logic with adversarial profiles did the underlying simplicity, and its resulting biases, become visible.

**What would you try next if you extended this project?**
If I extended this project, I would first address the exact-match limitation on genre and mood by introducing some notion of similarity between labels, rather than requiring identical text. I would also expand the dataset so that every genre has multiple representative songs, removing the artificial dominance that occurs when a song has no real competitor. Finally, I would experiment with allowing a user profile to specify a small set of acceptable moods or genres rather than exactly one, since real listeners rarely confine their taste to a single narrow preference.



