"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

import textwrap

from src.recommender import load_songs, recommend_songs


# NEW FUNCTION (added for Step 1 of the evaluation phase).
#
# Why this exists: the original code below (inside main()) prints the top 5
# recommendations for exactly ONE user profile, using 6 lines of print()
# statements. Step 1 of the assignment asks us to test MANY different user
# profiles (8 total: 3 baseline + 5 adversarial/edge-case ones). Copy-pasting
# those same 6 print lines 8 times would mean if we ever want to change the
# print format, we'd have to update it in 8 places instead of 1.
#
# So instead, this function wraps that same print logic once, and takes the
# "changing part" (the profile name and the profile dict itself) as
# parameters. Every profile below just calls this one function with
# different arguments.
def print_recommendations(label: str, user_prefs: dict, songs, k: int = 5) -> None:
    # This does the exact same thing the original code does:
    # score every song against user_prefs and keep only the top k.
    recommendations = recommend_songs(user_prefs, songs, k=k)

    # label is just a human-readable name like "High-Energy Pop" so we can
    # tell, while reading the terminal output, which profile produced which
    # block of results.
    print(f"\n### {label}")
    print(f"User profile: {user_prefs}\n")

    # Challenge 4: Visual Summary Table. Instead of a separate print() line
    # for rank/title/artist/score/reasons, lay them out in aligned columns
    # so the terminal output reads like a table. Reasons text is often too
    # long to fit on one line, so it gets wrapped and continued on indented
    # lines below the row it belongs to.
    header = f"{'#':<3} {'Title':<22} {'Artist':<18} {'Score':<6} Reasons"
    print(header)
    print("-" * len(header))

    for rank, rec in enumerate(recommendations, start=1):
        song, score, explanation = rec
        wrapped = textwrap.wrap(explanation, width=50) or [""]
        print(f"{rank:<3} {song['title']:<22} {song['artist']:<18} {score:<6.2f} {wrapped[0]}")
        for extra_line in wrapped[1:]:
            print(f"{'':<3} {'':<22} {'':<18} {'':<6} {extra_line}")


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # Starter example profile
    user_prefs = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.8,
        "likes_acoustic": False,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    print("=" * 40)
    for rank, rec in enumerate(recommendations, start=1):
        # You decide the structure of each returned item.
        # A common pattern is: (song, score, explanation)
        song, score, explanation = rec
        print(f"{rank}. {song['title']} by {song['artist']}")
        print(f"   Score: {score:.2f}")
        print(f"   Because: {explanation}")
        print("=" * 40)

    # ==========================================================
    # STEP 1: STRESS TEST WITH DIVERSE PROFILES (NEW SECTION)
    # ==========================================================
    #
    # Everything above this line (the "Starter example profile" and its
    # print loop) is untouched from the original file — we did not delete
    # or modify any of it.
    #
    # Below, we define 3 "normal" user profiles that represent distinct,
    # realistic music tastes. Each one is just a plain Python dictionary
    # with the same 4 keys the scoring logic expects:
    #   - favorite_genre: a string like "pop", "rock", "lofi"
    #   - favorite_mood:  a string like "happy", "chill", "intense"
    #   - target_energy:  a number from 0.0 (low energy) to 1.0 (high energy)
    #   - likes_acoustic: True/False, whether the user prefers acoustic songs
    #
    # We picked genre/mood values that actually exist in data/songs.csv so
    # each profile has a real chance of matching songs.

    # Profile 1: someone who wants upbeat, high-energy pop music.
    high_energy_pop = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.9,
        "likes_acoustic": False,
    }

    # Profile 2: someone who wants relaxed, low-energy lofi music.
    chill_lofi = {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.3,
        "likes_acoustic": True,
    }

    # Profile 3: someone who wants aggressive, very high-energy rock music.
    deep_intense_rock = {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.95,
        "likes_acoustic": False,
    }

    # For each profile, call our new helper function instead of copy-pasting
    # the print loop again. This runs recommend_songs() on each profile and
    # prints its own top-5 list, labeled so we can tell them apart in the
    # terminal.
    print_recommendations("High-Energy Pop", high_energy_pop, songs)
    print_recommendations("Chill Lofi", chill_lofi, songs)
    print_recommendations("Deep Intense Rock", deep_intense_rock, songs)

    # ==========================================================
    # ADVERSARIAL / EDGE-CASE PROFILES (NEW SECTION)
    # ==========================================================
    #
    # The goal here is different from the 3 profiles above. Instead of
    # testing "normal" users, we're deliberately trying to break or confuse
    # the scoring logic in recommender.py -> score_song(), to see if it
    # behaves sensibly or produces weird/misleading results. Each profile
    # below targets a specific weak spot.

    # Edge case 1: the user's mood and energy preferences pull in opposite
    # directions (wants "sad" mood, but very high energy 0.9). In real
    # music, sad songs are usually low-energy, so this checks whether a
    # song can win the top spot purely on energy/genre points even though
    # it completely misses the mood the user asked for.
    contradictory_energy_vs_mood = {
        "favorite_genre": "rock",
        "favorite_mood": "sad",
        "target_energy": 0.9,
        "likes_acoustic": False,
    }

    # Edge case 2: favorite_genre is "jazz", which does NOT exist anywhere
    # in data/songs.csv. This checks that score_song() doesn't crash when a
    # genre never matches, and that it still returns a reasonable ranked
    # list based on mood/energy/acoustic points alone.
    unknown_genre = {
        "favorite_genre": "jazz",
        "favorite_mood": "chill",
        "target_energy": 0.5,
        "likes_acoustic": True,
    }

    # Edge case 3: target_energy is set to the absolute minimum (0.0).
    # This checks the math at the low boundary of the energy scale, making
    # sure the "energy similarity" score never goes negative or breaks.
    zero_energy_boundary = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.0,
        "likes_acoustic": False,
    }

    # Edge case 4: target_energy is set to the absolute maximum (1.0).
    # Same idea as above, but testing the high boundary instead of the low
    # one.
    max_energy_boundary = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 1.0,
        "likes_acoustic": False,
    }

    # Edge case 5: the user wants BOTH very high energy (0.95) AND acoustic
    # songs (likes_acoustic=True). In practice, high-energy songs tend to
    # have LOW acousticness, so these two preferences are hard to satisfy
    # at the same time. This checks whether the acoustic bonus points ever
    # actually apply here, or whether they basically never fire.
    acoustic_contradicts_energy = {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.95,
        "likes_acoustic": True,
    }

    # Edge case 6: a "middle of the road" profile with no strong signal in
    # any direction (medium energy, and a genre/mood combo that doesn't
    # naturally go together). This checks that when nothing stands out,
    # the recommender still breaks ties in a sensible way instead of
    # looking random.
    all_neutral_apathetic = {
        "favorite_genre": "lofi",
        "favorite_mood": "happy",
        "target_energy": 0.5,
        "likes_acoustic": False,
    }

    # Run and print each adversarial profile the same way as before, using
    # our shared helper function.
    print_recommendations("Adversarial: Contradictory Energy vs. Mood", contradictory_energy_vs_mood, songs)
    print_recommendations("Adversarial: Unknown Genre", unknown_genre, songs)
    print_recommendations("Adversarial: Zero-Energy Boundary", zero_energy_boundary, songs)
    print_recommendations("Adversarial: Max-Energy Boundary", max_energy_boundary, songs)
    print_recommendations("Adversarial: Acoustic Contradicts Energy", acoustic_contradicts_energy, songs)
    print_recommendations("Adversarial: All-Neutral/Apathetic", all_neutral_apathetic, songs)


if __name__ == "__main__":
    main()
