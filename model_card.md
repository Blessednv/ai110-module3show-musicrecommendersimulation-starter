# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

**MusicChoice 1.0**

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

**What kind of recommendations does it generate?**
It looks at a small list of songs and picks the top 5 that best match what one person says they like. It's not looking at millions of songs, just this one small practice catalog.

**What assumptions does it make about the user?**
It assumes the user can describe their taste in exactly one genre, one mood, one energy level (from 0 to 1), and whether they like acoustic songs or not. It assumes people's taste fits neatly into those four boxes, which isn't really true for real listeners.

**Is this for real users or classroom exploration?**
This is for classroom exploration, not real users. It's a small project built to learn how recommender systems work, not something ready for real people to use every day.

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

**What features of each song are used?**
Each song has a genre, a mood, an energy level, and an acousticness level (how "unplugged" it sounds).

**What user preferences are considered?**
The user profile has a favorite genre, a favorite mood, a target energy level, and whether they like acoustic songs.

**How does the model turn those into a score?**
The model checks the song against each of those four things one at a time. It gives points if the genre matches, points if the mood matches, points based on how close the song's energy is to what the user wants, and points if the acousticness fits the user's taste. Then it adds all the points together to get one score per song, and the songs with the highest scores get recommended.

**What changes did you make from the starter logic?**
I mostly filled in what was left as TODOs, the scoring math and the ranking logic. Later, during experiments, I temporarily tried doubling the energy weight and halving the genre weight, and separately tried turning off the mood check completely, just to see what would happen. Both changes were reverted afterward, so the real system still uses the original weights.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

**How many songs are in the catalog?**
There are 21 songs in the catalog.

**What genres or moods are represented?**
There are 15 different genres (pop, lofi, rock, ambient, jazz, synthwave, indie pop, hip-hop, classical, country, metal, reggae, folk, EDM, R&B) and a bunch of different one-word moods like happy, chill, intense, sad, relaxed, moody, focused, confident, melancholic, nostalgic, angry, carefree, romantic, euphoric, and sensual.

**Did you add or remove data?**
Yes, I added 3 new rock songs (Broken Amplifier, Riot Chorus, Gravel Road) partway through testing, because I noticed rock only had one song and it was winning every rock-related search by default, not because it was actually the best match.

**Are there parts of musical taste missing in the dataset?**
Yes, a lot is missing. Most genres only have one song each, so there's basically no variety if that's your favorite genre. There's also no way to search by artist, decade, or language, and moods are just single words instead of a range, so there's no in-between feeling like "kind of happy but a little tired."

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

**User types for which it gives reasonable results?**
It works best for users whose favorite genre has more than one song to pick from, like lofi or rock (after I added more rock songs). Those profiles get results that actually feel like a real comparison happened.

**Any patterns you think your scoring captures correctly?**
The energy-closeness scoring works the way I'd expect, it always picks the song whose energy number is nearest to what the user asked for, and never picks something wildly off unless nothing better exists.

**Cases where the recommendations matched your intuition?**
The Chill Lofi profile felt the most "right" to me. It picked slow, mellow, acoustic-leaning songs, which is exactly what someone asking for chill lofi music would want.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

The biggest weakness I found while running my experiments wasn't really in the scoring math, it was in the data. I counted up the genres in songs.csv and 13 out of the 21 songs are the *only* song in their genre. Rock, lofi, and pop are the only genres with any real variety (4, 3, and 2 songs), and everything else, jazz, ambient, classical, metal, country, reggae, folk, hip-hop, R&B, synthwave, indie pop, and EDM, has exactly one entry. So if your favorite genre happens to be jazz, the system doesn't really "recommend" anything for you, it just hands you Coffee Shop Stories every time, whether you wanted something chill or something intense. That's not really personalization, it's just the only song available pretending to be a personalized pick. I only noticed this because I kept seeing the same songs win over and over in my Step 1 stress tests, and when I dug into why, it turned out for some profiles the "winner" was never competing against anything at all.

Here's a simple way to think about it. Imagine a toy box with only one red toy in it. If someone asks for "the red toy," you hand them that one toy every time, no matter what kind of red toy they actually wanted. That's basically what happens to a user who says their favorite genre is jazz, metal, or reggae. The system isn't being smart about it, it just has nothing else to offer, so the "only" choice looks like the "best" choice even when it isn't.

There's a second problem I found too, and it's about how the words have to match exactly. The code checks `song['genre'] == user_prefs['favorite_genre']`, which means the two words have to be spelled the exact same way to count as a match. If a song is labeled "synthwave" and a user types "synth pop," the system says no match at all, even though those two things sound pretty similar to a real person. It's like asking a friend for a "soda" and they say they don't have any, but they're holding a can of "pop" the whole time, same drink, different word, and the system just isn't smart enough to know that.

The same exact-match problem happens with mood. Moods in the dataset are things like "happy," "chill," "intense," "sad," and "melancholic." If a user wants something "energetic" but the system only knows the word "intense," they get zero mood points, even if "energetic" and "intense" mean almost the same thing to a human. The system can't tell that two words are close in meaning, it can only tell if they are spelled identically.

There's also a smaller, sneakier bias in how the acoustic check works. Looking at `score_song()`, a song only gets the acoustic bonus point if its acousticness score is 0.6 or higher (for users who like acoustic songs) or 0.4 or lower (for users who don't). But that leaves a gap right in the middle, between 0.4 and 0.6, where a song gets no acoustic bonus either way. It's like a rule that says "you're only tall enough for the ride if you're really short or really tall," and anyone in between just gets ignored, even though "in between" is a totally normal thing to be.

Put together, all of these problems point to the same root cause: the system was built to compare things that match *perfectly*, but real listeners rarely think in perfectly matching words or perfectly measured numbers. A person doesn't wake up and think "I want exactly 0.9 energy today," they think "I want something upbeat." Because the system can only work with exact labels and exact number ranges, it ends up being unfair in a quiet way, not because it's trying to play favorites, but because its rules are too rigid to notice when two things are basically the same, just described a little differently.

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

### Step 3: Small Data Experiments (Sensitivity Testing)

To test how sensitive the recommender is to its own scoring rules, I ran two separate experiments in `recommender.py`'s `score_song()`, one at a time, then restored the original logic before moving on.

#### Experiment 1: Weight Shift (genre halved, energy doubled)

**Prompt given to the AI coding assistant:** *"In `score_song()`, double the weight of energy similarity from a max of +2.0 to a max of +4.0, and halve the genre match weight from +2.0 to +1.0. Keep mood (+1.0) and acousticness (+1.0) unchanged. Verify the math stays valid — no negative scores, no score exceeding the new maximum."*

**Math verification:** since `energy_diff = abs(song['energy'] - target_energy)` is always between 0 and 1 (both values are on a 0-1 scale), `4.0 * (1 - energy_diff)` is always between 0 and 4.0 — the `max(0.0, ...)` wrapper still guarantees it can't go negative. New max possible score: `1.0 (genre) + 1.0 (mood) + 4.0 (energy) + 1.0 (acoustic) = 7.0` (up from 6.0).

**Result — mostly *different*, not more accurate:**
- **One win:** in the "Unknown Genre" (jazz) profile, the #1 result flipped from "Coffee Shop Stories" (the only jazz song, winning on genre alone) to "Midnight Coding" (lofi, a real mood + energy match) — genre alone stopped being enough to override an actual mood/energy fit.
- **One new problem:** in the "Zero-Energy Boundary" (pop/happy/0.0) profile, "Autumn Sonata" — a classical/melancholic song with *zero* genre or mood match — climbed into the top 5, purely because its energy value happened to be close to 0.0 and energy was now worth up to +4.0.
- **Verdict:** this traded one bias for another. It fixed "genre alone shouldn't win" but introduced "energy alone can smuggle in a vibe-mismatched song," which is arguably worse since energy is a single number while genre/mood describe more of what a song actually sounds and feels like.

#### Experiment 2: Feature Removal (mood check disabled)

**Prompt given to the AI coding assistant:** *"Temporarily comment out the mood-match check in `score_song()` (do not delete it) so I can see how rankings change without it, keeping genre, energy, and acousticness weights at their original values."*

**Result — a clear regression, not just a difference:**
- **"Contradictory Energy vs. Mood" (rock/sad/0.9)** is the clearest case: with mood active, "Broken Amplifier" (the actual sad rock song) correctly ranked #1. With mood removed, it dropped to **#3**, and "Storm Runner" (mood: intense — the *wrong* mood entirely) reclaimed #1 purely on genre + energy. Removing mood undid the exact fix verified in Step 2's dataset experiment.
- **"High-Energy Pop" (pop/happy/0.9)** flipped order: "Sunrise City" previously won by a full point thanks to its mood match; without mood, "Gym Hero" (mood: intense, not happy at all) edges it out by 0.10 points purely because its energy value is marginally closer to the target.
- **Verdict:** unlike the weight-shift experiment, this wasn't a trade-off — it was a straightforward loss of accuracy. Mood is the only signal that lets the system tell apart same-genre songs with very different vibes (e.g., "intense" vs. "sad" rock), and removing it collapses that distinction entirely.

**Overall takeaway from Step 3:** changing weights (Experiment 1) shifts *which* bias the system has, while removing a whole feature (Experiment 2) removes a capability the system needs — these are not the same kind of change, and "more accurate" vs. "just different" depends entirely on which one you're doing.

### Step 5: Comparing Profiles Side-by-Side

**Which profiles I tested:** I ended up testing 10 different profiles total — the original starter default, 3 "normal" profiles meant to represent distinct, realistic tastes (High-Energy Pop, Chill Lofi, Deep Intense Rock), and 5 adversarial/edge-case profiles designed to try to break the scoring logic (Contradictory Energy vs. Mood, Unknown Genre, Zero-Energy Boundary, Max-Energy Boundary, Acoustic Contradicts Energy, All-Neutral). The full terminal output for all of them is below.

**What surprised me most, overall:** how often a song won not because it was a great match, but because it was the *only* option in its lane, and how a song could win despite missing one of the four criteria entirely, as long as it made up for it with the other three. Neither of those things would be obvious just from reading the scoring code, you really only notice it by running a bunch of profiles side by side and asking "wait, why did that one win?"

**Pairing up profiles and comparing what changed:**

- **High-Energy Pop vs. Chill Lofi.** These two are basically opposites on purpose: one wants fast, upbeat pop (`target_energy=0.9`), the other wants slow, relaxed lofi (`target_energy=0.3`). The results make total sense: High-Energy Pop's top pick, Sunrise City, has an actual measured energy of 0.82 (close to loud and fast), while Chill Lofi's top pick, Library Rain, has an energy of 0.35 (close to slow and mellow). The system is correctly separating "loud" music from "quiet" music here, which is exactly what the energy number is supposed to capture.

- **Deep Intense Rock vs. Contradictory Energy vs. Mood.** Both profiles ask for `favorite_genre: rock`, but one wants mood "intense" and the other wants mood "sad," with both requesting high energy (0.95 and 0.9). Deep Intense Rock's winner is Storm Runner (mood: intense — an actual match). Contradictory Energy vs. Mood's winner is Broken Amplifier (mood: sad — also an actual match), even though Broken Amplifier's own energy (0.45) is nowhere near the requested 0.9. This makes sense once you realize mood match is worth a full point: a real mood match plus a mediocre energy fit can still beat a great energy fit with no mood match, which is the system correctly prioritizing "does this feel right" over "is this exactly the right loudness."

- **Zero-Energy Boundary vs. Max-Energy Boundary.** Same profile in every other way (pop, happy, not acoustic) except the energy target sits at the two opposite extremes, 0.0 versus 1.0. Both still pick Sunrise City as the #1 result, but the score is very different (4.36 vs. 5.64). That makes sense mathematically, Sunrise City's real energy is 0.82, so it's much closer to the "1.0" request than the "0.0" request, but it's a little strange from a listener's point of view: a system that recommends the exact same song whether you say you want the calmest or the most intense song in the world isn't really listening to that part of your request at all, it's leaning on genre and mood to paper over a bad energy fit.

- **Unknown Genre vs. All-Neutral.** Neither profile has a clean genre-and-mood combo that "belongs together" the way pop/happy or rock/intense do. Unknown Genre asks for jazz (a genre that exists once in the catalog) with mood "chill" (which doesn't match that jazz song's actual mood, "relaxed"), so it only ever gets credit for genre, never mood. All-Neutral asks for lofi with mood "happy," which doesn't match any lofi song's real mood ("chill" or "focused"), so it only ever gets credit for genre too. Both end up with a winner that "sort of" fits, sort of doesn't, which makes sense: when a user's own preferences don't naturally go together in real music, the system can't manufacture agreement that isn't there in the data.

- **Acoustic Contradicts Energy vs. Chill Lofi.** Both profiles set `likes_acoustic: True`, but Chill Lofi pairs it with a low energy target (0.3), which is a combination that shows up naturally in real acoustic music, while Acoustic Contradicts Energy pairs it with a very high energy target (0.95), a combination that's rare or nonexistent in the catalog. Chill Lofi's winner scores 5.90 out of a possible 6.0, nearly a perfect match on every criterion. Acoustic Contradicts Energy's winner only scores 4.92, and it does not get the acoustic bonus point at all, because no rock song loud enough to satisfy 0.95 energy is also acoustic-leaning. This makes complete sense: you can only get a great score when your stated preferences describe a song that could actually exist, and this profile describes one that basically can't.

**Explaining it in plain language — why does "Gym Hero" keep showing up for people who just want "Happy Pop"?**

Imagine you tell a friend, "put on something happy and poppy for me." Gym Hero is a pop song, so it checks that first box. But its actual vibe, according to its own mood label, is "intense," not "happy" — it's more of a pump-you-up gym anthem than a genuinely cheerful song. The reason it still shows up near the top of the list anyway is that the system doesn't only care about mood, it also gives a lot of credit for how fast/energetic a song is, and Gym Hero is extremely high-energy (0.93), almost exactly what a "give me energetic pop" request is asking for numerically. So even though it misses the "happy" feeling completely, it makes up for that by nailing the genre and the energy so precisely that its total score ends up close to, or sometimes higher than, a song that actually is happy but whose energy is a slightly worse numeric match. In plain terms: the system is like a shopper who's told "get me something happy," but grabs the loudest, most pop-sounding thing on the shelf without checking if it's actually a happy song. It's not wrong on purpose, it's just weighting "is this the right kind of loud" almost as heavily as "does this actually feel happy," and sometimes that lets an intense song sneak in under a happy request.

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

**Additional features or preferences?**
I'd let users pick more than one favorite genre or mood instead of just one, since real people don't only like one thing.

**Better ways to explain recommendations?**
I'd want the explanations to sound more like a person talking, right now it just lists point values, which is clear but a little robotic.

**Improving diversity among the top results?**
I'd try to stop the same 1-2 songs from dominating every list, maybe by only showing one song per artist in the top 5, so the list feels less repetitive.

**Handling more complex user tastes?**
I'd add "closeness" matching for genre and mood instead of requiring an exact spelling match, so "synth pop" and "synthwave" could still count as similar.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

**What you learned about recommender systems?**
I learned that a recommendation system does not need sophisticated machine learning to appear personalized; a handful of simple rules, combined and weighted correctly, can produce results that feel tailored to an individual. At the same time, I learned that these same simple rules can conceal significant unfairness, patterns that remain invisible until the system is tested systematically across a range of different users.

**Something unexpected or interesting you discovered?**
The most striking discovery was that an identical symptom, the same song ranking first repeatedly, can originate from two entirely distinct causes. In one case, a song wins because the underlying data offers no genuine alternative. In another, it wins because the scoring formula itself overweights certain criteria. These two causes look identical when only the output is observed, yet they require completely different remedies.

**What was your biggest learning moment during this project?**
The most significant moment arrived not while writing code, but while comparing outputs across profiles. I had assumed the scoring logic behaved correctly because it produced a plausible list for the default profile. It was only through systematic comparison, testing ten distinct profiles side by side, that I recognized certain songs were winning for reasons entirely unrelated to a genuine match. That experience taught me that testing a single case, however sensible it appears, does not constitute a full evaluation of a scoring rule's behavior.

**How did using AI tools help you, and when did you need to double-check them?**
AI assistance was most useful for two tasks: rapidly proposing edge-case profiles I would not have devised independently, such as the contradictory mood/energy example and the unknown-genre example, and explaining, with the actual weight values, why a particular song had ranked first. I needed to verify each explanation myself rather than accept it outright. In one instance, I confirmed a claim that a genre had only one representative song by counting genre entries directly in the dataset, rather than trusting the summary as given. I also re-ran the recommender after every proposed change to confirm the reported scores matched the actual terminal output, rather than trusting a description of what the change "should" do.

**What surprised you about how simple algorithms can still "feel" like recommendations?**
What surprised me most was how convincingly a handful of conditional checks and one weighted sum could imitate the impression of personal taste. Because the scoring produces a ranked list with a plausible explanation attached to each song, it is easy to mistake consistent behavior for genuinely intelligent judgment. Only by deliberately attempting to break the logic with adversarial profiles did the underlying simplicity, and its resulting biases, become visible.

**What would you try next if you extended this project?**
If I extended this project, I would first address the exact-match limitation on genre and mood by introducing some notion of similarity between labels, rather than requiring identical text. I would also expand the dataset so that every genre has multiple representative songs, removing the artificial dominance that occurs when a song has no real competitor. Finally, I would experiment with allowing a user profile to specify a small set of acceptable moods or genres rather than exactly one, since real listeners rarely confine their taste to a single narrow preference.

**How this changed the way you think about music recommendation apps?**
This project changed how I interpret the recommendations produced by commercial platforms such as Spotify. I no longer assume that a suggested song reflects genuine understanding of my taste. It is more likely that my preferences have been reduced to a small set of numerical values, and the platform is simply returning whichever option scores highest according to its internal formula, limitations and biases included.
