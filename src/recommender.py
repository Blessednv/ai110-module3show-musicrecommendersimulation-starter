import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    Reads each row with csv.DictReader and converts numeric fields to int/float.
    """
    songs = []
    with open(csv_path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": int(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    Awards points for genre, mood, energy closeness, and acousticness fit, returning (score, reasons).
    """
    # TODO: Implement scoring logic using your Algorithm Recipe from Phase 2.
    # Expected return format: (score, reasons)
    score = 0.0
    reasons = []

    if song['genre'] == user_prefs['favorite_genre']:
        score += 2.0
        reasons.append('Genre match (+2.0)')

    if song['mood'] == user_prefs['favorite_mood']:
        score += 1.0
        reasons.append('Mood match (+1.0)')

    energy_diff = abs(song['energy'] - user_prefs['target_energy'])
    energy_points = max(0.0, 2.0 * (1 - energy_diff))
    score += energy_points
    reasons.append(f'Energy similarity (+{energy_points:.2f})')

    if user_prefs['likes_acoustic'] and song['acousticness'] >= 0.6:
        score += 1.0
        reasons.append('Acousticness match (+1.0)')
    elif not user_prefs['likes_acoustic'] and song['acousticness'] <= 0.4:
        score += 1.0
        reasons.append('Acousticness match (+1.0)')

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5, artist_penalty: float = 1.5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    Scores every song with score_song(), then returns the top k sorted highest to lowest.
    """
    # TODO: Implement scoring and ranking logic
    # Expected return format: (song_dict, score, explanation)
    base_scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        base_scored.append((song, score, reasons))

    # Challenge 3: Diversity and Fairness Logic. Instead of just sorting once
    # and taking the top k, build the list one song at a time. Once an
    # artist already has a song in the list, any other song by that same
    # artist gets a penalty applied to its score for the remaining picks —
    # so it can still make the list, but only if it's still clearly better
    # than everything else after the penalty.
    selected = []
    seen_artists = set()
    remaining = list(base_scored)

    while remaining and len(selected) < k:
        def effective_score(entry):
            song, score, _ = entry
            penalty = artist_penalty if song['artist'] in seen_artists else 0.0
            return score - penalty

        remaining.sort(key=effective_score, reverse=True)
        song, score, reasons = remaining.pop(0)

        penalty = artist_penalty if song['artist'] in seen_artists else 0.0
        reason_list = list(reasons)
        if penalty > 0:
            reason_list.append(f"Diversity penalty (-{penalty:.2f}, artist already in list)")

        selected.append((song, score - penalty, ", ".join(reason_list)))
        seen_artists.add(song['artist'])

    return selected
