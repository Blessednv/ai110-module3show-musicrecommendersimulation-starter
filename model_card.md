# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

### Step 2: Accuracy Check and Surprises

**Does it feel right?** Comparing the 10 runs above to my own intuition, one pattern stood out immediately: the same songs keep winning across very different profiles.

| Profile | #1 Song |
|---|---|
| Starter default (pop/happy/0.8) | Sunrise City |
| High-Energy Pop (pop/happy/0.9) | Sunrise City |
| Zero-Energy Boundary (pop/happy/0.0) | Sunrise City |
| Max-Energy Boundary (pop/happy/1.0) | Sunrise City |
| Deep Intense Rock | Storm Runner |
| Contradictory Energy vs. Mood | Storm Runner |
| Acoustic Contradicts Energy | Storm Runner |
| Chill Lofi | Library Rain |
| Unknown Genre | Coffee Shop Stories |
| All-Neutral | Midnight Coding |

"Sunrise City" wins 4 of the 10 runs, and "Storm Runner" wins 3 — notably, both times a profile only shares a genre with those songs, the same song still comes out on top *even when the target energy is set to the opposite extreme* (0.0 vs. 1.0). That does not match my intuition of what a "personalized" recommendation should look like — it suggests the genre weight is dominating the ranking regardless of how badly other preferences are mismatched.

**Prompt I gave my AI coding assistant:**

> "In the Zero-Energy Boundary profile (`target_energy: 0.0`, wanting a *low-energy* pop/happy song), why did 'Sunrise City' — a song with `energy: 0.82`, nearly the *opposite* of what the user asked for — still rank #1?"

**The assistant's explanation, based on the weights in `recommender.py`'s `score_song()`:**

- Genre match (`pop == pop`): +2.0
- Mood match (`happy == happy`): +1.0
- Energy similarity: `2.0 * (1 - abs(0.82 - 0.0))` = `2.0 * 0.18` = +0.36 (small, but never negative — the formula only shrinks toward 0 as the mismatch grows, it never penalizes a bad match)
- Acousticness fit (`acousticness=0.18 ≤ 0.4`, `likes_acoustic=False`): +1.0

Total: **4.36**. Even though the energy score collapsed almost to zero, genre + mood + acoustic alone add up to 4.0 — enough to beat any song that doesn't also match genre and mood, even one with a perfect energy fit (since energy can only ever contribute up to +2.0 max).

**What this reveals:** this is exactly the failure mode described in the assignment instructions — *"if the same song keeps appearing at the top of every list, your Genre weight might be too strong, or your dataset might be too small to provide variety."* Here, the genre+mood ceiling (3.0 combined) outweighs how badly energy mismatches, because a mismatch on one axis is "cheap" to survive as long as genre and mood are winning. A future fix would be to lower the genre weight, raise the energy weight, or scale energy similarity more aggressively so a bad mismatch costs more than +0.36.

**Digging deeper: dataset size vs. weighting — two separate causes.** Checking `data/songs.csv` directly shows the repetition actually comes from two distinct problems, not one:

| Genre | # of songs in catalog |
|---|---|
| pop | 2 (Sunrise City, Gym Hero) |
| rock | 1 (Storm Runner) |
| lofi | 3 |
| everything else | 1 each |

- **Storm Runner's dominance is a dataset-size problem.** "Rock" has exactly one song in the whole catalog. Any rock-favoring profile (Deep Intense Rock, Contradictory Energy vs. Mood, Acoustic Contradicts Energy) is guaranteed to rank it #1, because there is no other rock song to compete with — this would happen no matter how the weights were tuned, since the genre bonus only ever has one candidate to award.
- **Sunrise City's dominance is a weighting problem.** "Pop" has two candidates — Sunrise City (mood: happy) and Gym Hero (mood: intense) — so there is real competition to observe. Sunrise City still wins every pop/happy profile, including the Zero-Energy Boundary case above where its energy match was nearly the opposite of what the user wanted. That is not a data-scarcity artifact; it is the genre+mood combined weight (3.0) overpowering a badly mismatched energy score, exactly as broken down above.

So the assignment's diagnostic checklist ("Genre weight too strong, OR dataset too small") isn't an either/or in this project — both are true, but for different songs and for different reasons. Fixing the dataset (adding more rock songs) would resolve Storm Runner's repetition; fixing the weights (lowering genre/mood or steepening the energy penalty) would resolve Sunrise City's.

**Verifying the fix: added 3 more rock songs.** To test the dataset-size hypothesis, I added 3 new rock songs to `data/songs.csv` (`Broken Amplifier` — sad mood, moderate energy; `Riot Chorus` — happy mood, high energy; `Gravel Road` — chill mood, low energy, higher acousticness), giving "rock" real internal variety instead of a single guaranteed winner. Re-running the same 8 profiles confirmed the hypothesis:

- **Contradictory Energy vs. Mood** (rock/sad/0.9) — the #1 result flipped from **Storm Runner** (intense mood, no mood match, score 4.98) to **Broken Amplifier** (sad mood — an actual match, score 5.10). With real competition in the genre, the recommender now correctly rewards the song that matches mood *and* genre over the one that only matches genre and has slightly better energy. This confirms Storm Runner's earlier dominance was purely a dataset-size artifact, not a flaw in the scoring logic.
- **Sunrise City still wins every pop/happy profile** (High-Energy Pop, Zero-Energy Boundary, Max-Energy Boundary), even though "pop" already had 2 songs *before* this fix and gained no new competitor. This confirms that repetition really is a weighting problem — adding more data to a genre that already had variety didn't change the outcome, because the genre+mood ceiling still outweighs a bad energy mismatch.

This is a useful takeaway about debugging recommender systems generally: **the same symptom (one song always ranking #1) can have entirely different root causes for different genres in the same catalog, and testing a fix against one genre doesn't tell you whether it fixed the other.**

### Terminal Output: Stress Test & Adversarial Profiles

I tested 8 distinct user profiles (3 baseline + 5 adversarial/edge-case) by running `python3 -m src.main` and observing the top 5 recommendations for each. Full terminal output below.

**High-Energy Pop** — `{'favorite_genre': 'pop', 'favorite_mood': 'happy', 'target_energy': 0.9, 'likes_acoustic': False}`

```
1. Sunrise City by Neon Echo
   Score: 5.84
   Because: Genre match (+2.0), Mood match (+1.0), Energy similarity (+1.84), Acousticness match (+1.0)
2. Gym Hero by Max Pulse
   Score: 4.94
   Because: Genre match (+2.0), Energy similarity (+1.94), Acousticness match (+1.0)
3. Rooftop Lights by Indigo Parade
   Score: 3.72
   Because: Mood match (+1.0), Energy similarity (+1.72), Acousticness match (+1.0)
4. Storm Runner by Voltline
   Score: 2.98
   Because: Energy similarity (+1.98), Acousticness match (+1.0)
5. Pulse Overdrive by DJ Kinetic
   Score: 2.90
   Because: Energy similarity (+1.90), Acousticness match (+1.0)
```

**Chill Lofi** — `{'favorite_genre': 'lofi', 'favorite_mood': 'chill', 'target_energy': 0.3, 'likes_acoustic': True}`

```
1. Library Rain by Paper Lanterns
   Score: 5.90
   Because: Genre match (+2.0), Mood match (+1.0), Energy similarity (+1.90), Acousticness match (+1.0)
2. Midnight Coding by LoRoom
   Score: 5.76
   Because: Genre match (+2.0), Mood match (+1.0), Energy similarity (+1.76), Acousticness match (+1.0)
3. Focus Flow by LoRoom
   Score: 4.80
   Because: Genre match (+2.0), Energy similarity (+1.80), Acousticness match (+1.0)
4. Spacewalk Thoughts by Orbit Bloom
   Score: 3.96
   Because: Mood match (+1.0), Energy similarity (+1.96), Acousticness match (+1.0)
5. Autumn Sonata by Elena Vance
   Score: 2.90
   Because: Energy similarity (+1.90), Acousticness match (+1.0)
```

**Deep Intense Rock** — `{'favorite_genre': 'rock', 'favorite_mood': 'intense', 'target_energy': 0.95, 'likes_acoustic': False}`

```
1. Storm Runner by Voltline
   Score: 5.92
   Because: Genre match (+2.0), Mood match (+1.0), Energy similarity (+1.92), Acousticness match (+1.0)
2. Gym Hero by Max Pulse
   Score: 3.96
   Because: Mood match (+1.0), Energy similarity (+1.96), Acousticness match (+1.0)
3. Pulse Overdrive by DJ Kinetic
   Score: 3.00
   Because: Energy similarity (+2.00), Acousticness match (+1.0)
4. Iron Collapse by Deathgrip
   Score: 2.96
   Because: Energy similarity (+1.96), Acousticness match (+1.0)
5. Sunrise City by Neon Echo
   Score: 2.74
   Because: Energy similarity (+1.74), Acousticness match (+1.0)
```

**Adversarial: Contradictory Energy vs. Mood** — `{'favorite_genre': 'rock', 'favorite_mood': 'sad', 'target_energy': 0.9, 'likes_acoustic': False}`

```
1. Storm Runner by Voltline
   Score: 4.98
   Because: Genre match (+2.0), Energy similarity (+1.98), Acousticness match (+1.0)
2. Gym Hero by Max Pulse
   Score: 2.94
   Because: Energy similarity (+1.94), Acousticness match (+1.0)
3. Pulse Overdrive by DJ Kinetic
   Score: 2.90
   Because: Energy similarity (+1.90), Acousticness match (+1.0)
4. Iron Collapse by Deathgrip
   Score: 2.86
   Because: Energy similarity (+1.86), Acousticness match (+1.0)
5. Sunrise City by Neon Echo
   Score: 2.84
   Because: Energy similarity (+1.84), Acousticness match (+1.0)
```

**Adversarial: Unknown Genre** — `{'favorite_genre': 'jazz', 'favorite_mood': 'chill', 'target_energy': 0.5, 'likes_acoustic': True}`

```
1. Coffee Shop Stories by Slow Stereo
   Score: 4.74
   Because: Genre match (+2.0), Energy similarity (+1.74), Acousticness match (+1.0)
2. Midnight Coding by LoRoom
   Score: 3.84
   Because: Mood match (+1.0), Energy similarity (+1.84), Acousticness match (+1.0)
3. Library Rain by Paper Lanterns
   Score: 3.70
   Because: Mood match (+1.0), Energy similarity (+1.70), Acousticness match (+1.0)
4. Spacewalk Thoughts by Orbit Bloom
   Score: 3.56
   Because: Mood match (+1.0), Energy similarity (+1.56), Acousticness match (+1.0)
5. Dust Road Home by Wade County
   Score: 3.00
   Because: Energy similarity (+2.00), Acousticness match (+1.0)
```

**Adversarial: Zero-Energy Boundary** — `{'favorite_genre': 'pop', 'favorite_mood': 'happy', 'target_energy': 0.0, 'likes_acoustic': False}`

```
1. Sunrise City by Neon Echo
   Score: 4.36
   Because: Genre match (+2.0), Mood match (+1.0), Energy similarity (+0.36), Acousticness match (+1.0)
2. Gym Hero by Max Pulse
   Score: 3.14
   Because: Genre match (+2.0), Energy similarity (+0.14), Acousticness match (+1.0)
3. Rooftop Lights by Indigo Parade
   Score: 2.48
   Because: Mood match (+1.0), Energy similarity (+0.48), Acousticness match (+1.0)
4. Island Sway by Marley Tide
   Score: 1.90
   Because: Energy similarity (+0.90), Acousticness match (+1.0)
5. Velvet Confession by Simone Rae
   Score: 1.84
   Because: Energy similarity (+0.84), Acousticness match (+1.0)
```

**Adversarial: Max-Energy Boundary** — `{'favorite_genre': 'pop', 'favorite_mood': 'happy', 'target_energy': 1.0, 'likes_acoustic': False}`

```
1. Sunrise City by Neon Echo
   Score: 5.64
   Because: Genre match (+2.0), Mood match (+1.0), Energy similarity (+1.64), Acousticness match (+1.0)
2. Gym Hero by Max Pulse
   Score: 4.86
   Because: Genre match (+2.0), Energy similarity (+1.86), Acousticness match (+1.0)
3. Rooftop Lights by Indigo Parade
   Score: 3.52
   Because: Mood match (+1.0), Energy similarity (+1.52), Acousticness match (+1.0)
4. Iron Collapse by Deathgrip
   Score: 2.94
   Because: Energy similarity (+1.94), Acousticness match (+1.0)
5. Pulse Overdrive by DJ Kinetic
   Score: 2.90
   Because: Energy similarity (+1.90), Acousticness match (+1.0)
```

**Adversarial: Acoustic Contradicts Energy** — `{'favorite_genre': 'rock', 'favorite_mood': 'intense', 'target_energy': 0.95, 'likes_acoustic': True}`

```
1. Storm Runner by Voltline
   Score: 4.92
   Because: Genre match (+2.0), Mood match (+1.0), Energy similarity (+1.92)
2. Gym Hero by Max Pulse
   Score: 2.96
   Because: Mood match (+1.0), Energy similarity (+1.96)
3. Dust Road Home by Wade County
   Score: 2.10
   Because: Energy similarity (+1.10), Acousticness match (+1.0)
4. Pulse Overdrive by DJ Kinetic
   Score: 2.00
   Because: Energy similarity (+2.00)
5. Iron Collapse by Deathgrip
   Score: 1.96
   Because: Energy similarity (+1.96)
```

**Adversarial: All-Neutral/Apathetic** — `{'favorite_genre': 'lofi', 'favorite_mood': 'happy', 'target_energy': 0.5, 'likes_acoustic': False}`

```
1. Midnight Coding by LoRoom
   Score: 3.84
   Because: Genre match (+2.0), Energy similarity (+1.84)
2. Focus Flow by LoRoom
   Score: 3.80
   Because: Genre match (+2.0), Energy similarity (+1.80)
3. Library Rain by Paper Lanterns
   Score: 3.70
   Because: Genre match (+2.0), Energy similarity (+1.70)
4. Rooftop Lights by Indigo Parade
   Score: 3.48
   Because: Mood match (+1.0), Energy similarity (+1.48), Acousticness match (+1.0)
5. Sunrise City by Neon Echo
   Score: 3.36
   Because: Mood match (+1.0), Energy similarity (+1.36), Acousticness match (+1.0)
```

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
