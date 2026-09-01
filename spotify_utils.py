import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import os
from dotenv import load_dotenv
import joblib
import pandas as pd
import time
import random

# ------------------ ENV ------------------
load_dotenv()

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

SCOPE = (
    "playlist-read-private "
    "playlist-modify-private "
    "playlist-modify-public "
    "user-library-read"
)

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE,
        cache_path=".cache"
    )
)

# ------------------ LOAD ML MODEL ------------------
try:
    model = joblib.load("mood_model.pkl")
    print("✅ ML model loaded")
except Exception as e:
    print(f"❌ ML model load failed: {e}")
    model = None


# ------------------ PLAYLIST FETCH ------------------
def get_user_playlists():
    playlists = []
    results = sp.current_user_playlists(limit=50)
    playlists.extend(results["items"])

    while results["next"]:
        results = sp.next(results)
        playlists.extend(results["items"])
        time.sleep(0.2)

    return playlists


def get_playlist_tracks(playlist_id):
    tracks = []
    results = sp.playlist_tracks(playlist_id, limit=100)

    while results:
        for item in results["items"]:
            track = item["track"]
            if not track:
                continue

            try:
                artist_info = sp.artist(track["artists"][0]["id"])
                genre = artist_info["genres"][0] if artist_info["genres"] else "Unknown"
            except:
                genre = "Unknown"

            tracks.append({
                "id": track["id"],
                "name": track["name"],
                "artist": track["artists"][0]["name"],
                "album": track["album"]["name"],
                "year": track["album"]["release_date"][:4],
                "added_at": item["added_at"],
                "duration_min": track["duration_ms"] / 60000,
                "genre": genre
            })

        if results["next"]:
            results = sp.next(results)
            time.sleep(0.2)
        else:
            break

    return tracks


def get_all_playlist_tracks():
    all_tracks = []
    for pl in get_user_playlists():
        all_tracks.extend(get_playlist_tracks(pl["id"]))
    return all_tracks


# ------------------ AUDIO FEATURES (BATCHED) ------------------
def get_audio_features(track_ids):
    all_features = []

    for i in range(0, len(track_ids), 50):  # Reduced batch size to avoid rate limits
        batch = track_ids[i:i + 50]
        try:
            features = sp.audio_features(batch)
            if features:
                all_features.extend([f for f in features if f])
            time.sleep(1)  # Add delay to avoid rate limits
        except Exception as e:
            print(f"❌ Audio feature error: {e}. Using simulated features.")
            return None  # Force simulation if API fails

    return all_features if all_features else None


def simulate_features(n):
    return [{
        "danceability": random.random(),
        "energy": random.random(),
        "key": random.randint(0, 11),
        "loudness": random.uniform(-30, 0),
        "mode": random.randint(0, 1),
        "speechiness": random.random(),
        "acousticness": random.random(),
        "instrumentalness": random.random(),
        "liveness": random.random(),
        "valence": random.random(),
        "tempo": random.uniform(60, 200)
    } for _ in range(n)]


# ------------------ MOOD PREDICTION ------------------
def predict_moods(tracks, metadata=None):
    if not tracks:
        return tracks

    if model is None:
        for t in tracks:
            t["mood"] = "Unknown"
        return tracks

    ids = [t["id"] for t in tracks]
    features = get_audio_features(ids) or simulate_features(len(ids))

    df = pd.DataFrame(features)
    required = [
        "danceability", "energy", "key", "loudness", "mode",
        "speechiness", "acousticness", "instrumentalness",
        "liveness", "valence", "tempo"
    ]

    df = df[required]

    predictions = model.predict(df)

    for i, t in enumerate(tracks):
        genre = t.get("genre", "").lower()
        name = t.get("name", "").lower()
        artist = t.get("artist", "").lower()
        
        # Expanded genre-based overrides
        if any(word in genre for word in ["sad", "blues", "indie", "folk", "alternative", "emo", "punjabi pop", "heartbreak", "melancholy"]):
            t["mood"] = "Sad"
        elif any(word in genre for word in ["rap", "hip-hop", "hip hop", "trap", "gangsta", "urban", "boom bap", "west coast", "east coast", "hindi hip hop"]):
            t["mood"] = "Rap"
        elif any(word in genre for word in ["rock", "metal", "punk", "grunge", "hardcore", "k-pop", "angry", "rage"]):
            t["mood"] = "Angry"
        elif any(word in genre for word in ["romantic", "ballad", "love song", "r&b", "soul", "bollywood", "romance"]):
            t["mood"] = "Romantic"
        elif any(word in genre for word in ["chill", "ambient", "lo-fi", "jazz", "classical", "tamil pop", "relax"]):
            t["mood"] = "Chill"
        elif any(word in genre for word in ["electronic", "disco", "funk", "techno", "house", "party", "dancehall"]):
            t["mood"] = "Energetic"
        elif any(word in genre for word in ["pop", "dance", "kannada pop", "marathi pop", "hindi pop", "happy", "joy"]):
            t["mood"] = "Happy"
        # Name-based overrides
        elif any(word in name for word in ["sad", "breakup", "heartbreak", "cry", "lonely", "depressed"]):
            t["mood"] = "Sad"
        elif any(word in name for word in ["happy", "joy", "smile", "fun"]):
            t["mood"] = "Happy"
        elif any(word in name for word in ["angry", "rage", "mad", "fury"]):
            t["mood"] = "Angry"
        elif any(word in name for word in ["love", "romantic", "kiss", "heart"]):
            t["mood"] = "Romantic"
        elif any(word in name for word in ["chill", "relax", "calm", "peace"]):
            t["mood"] = "Chill"
        elif any(word in name for word in ["energetic", "party", "dance", "pump"]):
            t["mood"] = "Energetic"
        elif any(word in name for word in ["rap", "hip hop", "trap"]):
            t["mood"] = "Rap"
        # Artist-based overrides (e.g., known sad artists)
        elif any(art in artist for art in ["arijit singh", "atif aslam", "alan walker"]):  # Add your known artists
            t["mood"] = "Sad"  # Example: Override to Sad for these artists
        else:
            t["mood"] = predictions[i].capitalize()
        
        # Apply saved overrides from metadata (persistence across runs)
        if metadata and t["id"] in metadata and 'mood_override' in metadata[t["id"]]:
            t["mood"] = metadata[t["id"]]['mood_override']
            print(f"Applied saved override for {t['name']}: {t['mood']}")
        
        print(f"Track: {t['name']} | Genre: {genre} | Name: {name} | Artist: {artist} | Mood: {t['mood']}")  # Enhanced debug

    return tracks


# ------------------ PLAYLIST CREATION ------------------
def create_playlist(name, track_ids, public=True):
    try:
        user_id = sp.current_user()["id"]

        playlist = sp.user_playlist_create(
            user=user_id,
            name=name,
            public=public,
            description="Auto-generated by Spotify Library Enhancer"
        )

        for i in range(0, len(track_ids), 100):
            sp.playlist_add_items(playlist["id"], track_ids[i:i + 100])
            time.sleep(0.2)

        return playlist["id"]

    except Exception as e:
        print(f"❌ Playlist creation failed: {e}")
        return None


# ------------------ METADATA ------------------
def load_library_metadata():
    if os.path.exists("library_metadata.json"):
        with open("library_metadata.json") as f:
            return json.load(f)
    return {}


def save_library_metadata(metadata):
    with open("library_metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)