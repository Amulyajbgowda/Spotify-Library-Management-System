import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from spotify_utils import get_user_playlists, get_playlist_tracks, predict_moods, create_playlist, load_library_metadata, save_library_metadata
from datetime import datetime, timedelta
import random
import os

# Check if authenticated (only prompt if needed)
try:
    playlists = get_user_playlists()
    authenticated = True
except Exception as e:
    authenticated = False
    st.error("Not authenticated with Spotify. Follow the steps below.")
    st.write("1. Click the link to authorize the app in your browser.")
    st.write("2. After authorizing, copy the code from the URL and paste it below.")
    
    # Trigger OAuth URL
    from spotipy.oauth2 import SpotifyOAuth
    sp_oauth = SpotifyOAuth(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
        scope="playlist-read-private playlist-modify-private playlist-modify-public user-library-read user-read-recently-played"
    )
    auth_url = sp_oauth.get_authorize_url()
    st.markdown(f"[Click here to authorize]({auth_url})")
    
    # Input for authorization code
    auth_code = st.text_input("Paste the authorization code here:")
    if st.button("Submit Code"):
        try:
            token_info = sp_oauth.get_access_token(auth_code)
            if token_info:
                st.success("✅ Authentication successful! Refresh the page to continue.")
                st.rerun()  # Refresh to proceed
            else:
                st.error("❌ Invalid code. Try again.")
        except Exception as e:
            st.error(f"❌ Authentication failed: {e}")
    st.stop()

if not authenticated:
    st.stop()

# Initialize session state here, before any access
if 'library' not in st.session_state:
    st.session_state.library = []
    st.session_state.metadata = load_library_metadata()

st.set_page_config(page_title="Spotify Library Enhancer", page_icon="🎵", layout="wide")
st.markdown("""
    <style>
    .main {background: linear-gradient(135deg, #121212 0%, #1a1a1a 100%); color: #1DB954;}
    .stButton>button {background: linear-gradient(45deg, #1DB954, #1ed760); color: white; border-radius: 25px; border: none; padding: 10px 20px; font-weight: bold;}
    .stTextInput, .stSelectbox {background-color: #282828; color: white; border-radius: 10px; border: 1px solid #1DB954;}
    .css-1d391kg {background: #121212;}
    h1, h2, h3 {color: #1DB954;}
    .metric-card {background: rgba(40, 40, 40, 0.8); border-radius: 15px; padding: 20px; margin: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.5); text-align: center;}
    .metric-card h4 {margin: 0; font-size: 1.2em; color: #1DB954;}
    .metric-card p {margin: 5px 0 0 0; font-size: 1.5em; font-weight: bold; color: white;}
    </style>
    """, unsafe_allow_html=True)

st.title("🎵 Spotify Library Enhancer")

st.sidebar.title("🎶 Quick Nav")
page = st.sidebar.radio("Go to", ["Dashboard & Stats", "Library Management", "Advanced Search", "Smart Playlists", "Rate Tracks"])

# Reload Library button in sidebar
if st.sidebar.button("🔄 Reload Library (Apply Overrides)"):
    if st.session_state.library:
        metadata = load_library_metadata()
        for track in st.session_state.library:
            track_id = track['id']
            if track_id in metadata and 'mood_override' in metadata[track_id]:
                track['mood'] = metadata[track_id]['mood_override']
        st.success("Library reloaded with manual overrides applied!")
    else:
        st.error("Load library first!")

playlists = get_user_playlists()
playlist_options = {pl['name']: pl['id'] for pl in playlists}
selected_playlist = st.sidebar.selectbox("Select Playlist", list(playlist_options.keys()), index=0 if playlists else None)

library = st.session_state.library
metadata = st.session_state.metadata

if st.button("🔄 Load Selected Playlist Tracks"):
    if selected_playlist:
        playlist_id = playlist_options[selected_playlist]
        try:
            tracks = get_playlist_tracks(playlist_id)
            st.session_state.library = predict_moods(tracks, metadata)  # Pass metadata for overrides
            st.success(f"✅ Tracks from '{selected_playlist}' loaded!")
        except Exception as e:
            st.error(f"❌ Failed: {e}")
    else:
        st.error("Select a playlist first!")

if st.button("🔄 Load All Playlist Tracks (Full Library)"):
    try:
        from spotify_utils import get_all_playlist_tracks
        all_tracks = predict_moods(get_all_playlist_tracks(), metadata)  # Pass metadata for overrides
        # Deduplicate by track ID to avoid counting duplicates
        seen_ids = set()
        deduped_tracks = []
        for track in all_tracks:
            if track['id'] not in seen_ids:
                seen_ids.add(track['id'])
                deduped_tracks.append(track)
        st.session_state.library = deduped_tracks
        st.success("✅ All playlist tracks loaded and deduplicated!")
    except Exception as e:
        st.error(f"❌ Failed: {e}")

if page == "Dashboard & Stats" and library:
    st.header("📊 Dashboard & Statistics")
    
    df = pd.DataFrame(library)
    df['added_date'] = pd.to_datetime(df['added_at'], utc=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'''
        <div class="metric-card">
            <h4>🎵 Total Tracks</h4>
            <p>{len(df)}</p>
        </div>
        ''', unsafe_allow_html=True)
    with col2:
        total_time_hrs = round(df['duration_min'].sum() / 60, 1)
        st.markdown(f'''
        <div class="metric-card">
            <h4>⏱️ Listening Time (hrs)</h4>
            <p>{total_time_hrs}</p>
        </div>
        ''', unsafe_allow_html=True)
    with col3:
        top_mood = df['mood'].mode()[0] if not df.empty else "N/A"
        st.markdown(f'''
        <div class="metric-card">
            <h4>😊 Top Mood</h4>
            <p>{top_mood}</p>
        </div>
        ''', unsafe_allow_html=True)
    with col4:
        unique_artists = df['artist'].nunique()
        st.markdown(f'''
        <div class="metric-card">
            <h4>🎤 Unique Artists</h4>
            <p>{unique_artists}</p>
        </div>
        ''', unsafe_allow_html=True)
    
    st.subheader("🎭 Mood Insights")
    mood_counts = df['mood'].value_counts()
    fig_mood = px.pie(mood_counts, names=mood_counts.index, values=mood_counts.values, title="Mood Distribution", 
                      color_discrete_sequence=['#1DB954', '#ff6b6b', '#4ecdc4', '#ffe66d', '#ff9ff3', '#ff3838', '#ff9f80', '#74b9ff'], hole=0.4)
    fig_mood.update_layout(paper_bgcolor="#121212", plot_bgcolor="#121212", font_color="white")
    st.plotly_chart(fig_mood, use_container_width=True)
    
    st.subheader("📈 Listening Trends & Comparisons")
    col1, col2 = st.columns(2)
    with col1:
        # Fetch recently played tracks for listening activities
        try:
            from spotify_utils import sp  # Import sp from utils
            recent_plays = sp.current_user_recently_played(limit=50)  # Get last 50 plays
            play_data = []
            for item in recent_plays['items']:
                track = item['track']
                played_at = pd.to_datetime(item['played_at'], utc=True)
                play_data.append({
                    'day': played_at.date(),
                    'duration_min': track['duration_ms'] / 60000  # Approximate play time
                })
            if play_data:
                play_df = pd.DataFrame(play_data)
                trends = play_df.groupby('day')['duration_min'].sum().reset_index()
                # Ensure full 30-day range
                now_utc = pd.Timestamp.now(tz='UTC')
                full_days = pd.date_range(end=now_utc.date(), periods=30, freq='D')
                trends = trends.set_index('day').reindex(full_days, fill_value=0).reset_index()
                trends.columns = ['day', 'duration_min']
                trends = trends.sort_values('day')
            else:
                # Fallback to added dates if no recent plays
                now_utc = pd.Timestamp.now(tz='UTC')
                recent_df = df[df['added_date'] > now_utc - pd.Timedelta(days=30)]
                if recent_df.empty:
                    days = pd.date_range(end=now_utc.date(), periods=30, freq='D')
                    trends = pd.DataFrame({'day': days, 'duration_min': [0] * 30})
                else:
                    recent_df['day'] = pd.to_datetime(recent_df['added_date'].dt.date)
                    trends = recent_df.groupby('day')['duration_min'].sum().reset_index()
                    full_days = pd.date_range(end=now_utc.date(), periods=30, freq='D')
                    trends = trends.set_index('day').reindex(full_days, fill_value=0).reset_index()
                    trends.columns = ['day', 'duration_min']
                trends = trends.sort_values('day')
        except Exception as e:
            st.warning(f"Could not fetch recent plays: {e}. Using added dates.")
            # Fallback to added dates
            now_utc = pd.Timestamp.now(tz='UTC')
            recent_df = df[df['added_date'] > now_utc - pd.Timedelta(days=30)]
            if recent_df.empty:
                days = pd.date_range(end=now_utc.date(), periods=30, freq='D')
                trends = pd.DataFrame({'day': days, 'duration_min': [0] * 30})
            else:
                recent_df['day'] = pd.to_datetime(recent_df['added_date'].dt.date)
                trends = recent_df.groupby('day')['duration_min'].sum().reset_index()
                full_days = pd.date_range(end=now_utc.date(), periods=30, freq='D')
                trends = trends.set_index('day').reindex(full_days, fill_value=0).reset_index()
                trends.columns = ['day', 'duration_min']
            trends = trends.sort_values('day')
        
        fig_trends = px.line(trends, x='day', y='duration_min', title="Daily Listening Trends (Last 30 Days)", 
                             color_discrete_sequence=['#1DB954'])
        fig_trends.update_traces(mode='lines+markers', connectgaps=True)
        fig_trends.update_layout(paper_bgcolor="#121212", plot_bgcolor="#121212", font_color="white", 
                                 xaxis_title="Date", yaxis_title="Duration (min)")
        st.plotly_chart(fig_trends, use_container_width=True)
    with col2:
        top_artists = df['artist'].value_counts().head(10)
        fig_artists = px.bar(top_artists, x=top_artists.index, y=top_artists.values, title="Top 10 Artists", color_discrete_sequence=['#1DB954'])
        fig_artists.update_layout(paper_bgcolor="#121212", plot_bgcolor="#121212", font_color="white", xaxis_tickangle=-45)
        st.plotly_chart(fig_artists, use_container_width=True)
    
    st.subheader("🔥 Activity Heatmap")
    df_copy = df.copy()  # Avoid modifying original df to fix warning
    df_copy.loc[:, 'day'] = df_copy['added_date'].dt.day_name()
    heatmap_data = df_copy.groupby(['day', 'mood']).size().unstack().fillna(0)
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    for day in weekdays:
        if day not in heatmap_data.index:
            heatmap_data.loc[day] = 0
    heatmap_data = heatmap_data.reindex(weekdays)
    fig_heatmap = go.Figure(data=go.Heatmap(z=heatmap_data.values, x=heatmap_data.columns, y=heatmap_data.index, 
                                            colorscale='Greens', text=heatmap_data.values, texttemplate="%{text}", textfont={"color": "white"}))
    fig_heatmap.update_layout(title="Weekly Mood Activity", paper_bgcolor="#121212", plot_bgcolor="#121212", font_color="white")
    st.plotly_chart(fig_heatmap, use_container_width=True)
    
    st.subheader("🚀 Advanced Insights")
    genre_diversity = len(df['genre'].unique()) / len(df) * 100 if len(df) > 0 else 0
    st.metric("Genre Diversity Score", f"{genre_diversity:.1f}%")
    now_utc = pd.Timestamp.now(tz='UTC')
    recent_tracks = df[df['added_date'] > now_utc - pd.Timedelta(days=30)]
    st.metric("Tracks Added This Month", len(recent_tracks))
    
    if st.button("📤 Export Dashboard Data"):
        df.to_csv("stats.csv", index=False)
        st.success("Data exported!")

elif page == "Library Management":
    st.header("📁 Library Management")
    genre = st.text_input("Genre")
    mood = st.selectbox("Mood", ["Happy", "Sad", "Energetic", "Calm", "Rap", "Angry", "Romantic", "Chill"])
    if st.button("Create Playlist"):
        filtered_tracks = [t for t in library if t.get('mood') == mood]
        track_ids = [t['id'] for t in filtered_tracks]
        name = f"Folder: {genre} / {mood} (from {selected_playlist})"
        create_playlist(name, track_ids)
        st.success(f"Playlist '{name}' created in Spotify!")
    
    st.subheader("🤖 Auto-Generate Mood Folders (Playlists)")
    if st.button("Show Mood Counts "):
        if library:
            df = pd.DataFrame(library)
            mood_counts = df['mood'].value_counts()
            st.write("Mood Distribution:")
            st.dataframe(mood_counts)
        else:
            st.error("Load library first!")
    
    if st.button("Generate All Mood Playlists"):
        if library:
            moods = ['Happy', 'Sad', 'Energetic', 'Calm', 'Rap', 'Angry', 'Romantic', 'Chill']
            for mood in moods:
                filtered_tracks = [t for t in library if t.get('mood') == mood]
                if filtered_tracks:
                    track_ids = [t['id'] for t in filtered_tracks]
                    name = f"Auto Mood: {mood}"
                    create_playlist(name, track_ids)
                    st.success(f"Created '{name}' in Spotify with {len(filtered_tracks)} tracks!")
                else:
                    st.info(f"No tracks for '{mood}' mood – skipped.")
        else:
            st.error("Load library first!")

elif page == "Advanced Search":
    st.header("🔍 Advanced Search")
    search_genre = st.text_input("Genre")
    search_year = st.text_input("Year")
    search_mood = st.selectbox("Mood", ["", "Happy", "Sad", "Energetic", "Calm", "Rap", "Angry", "Romantic", "Chill"])
    search_artist = st.text_input("Artist")
    if st.button("Search"):
        results = library
        if search_genre: results = [t for t in results if search_genre.lower() in t.get('genre', '').lower()]
        if search_year: results = [t for t in results if t['year'] == search_year]
        if search_mood: results = [t for t in results if t['mood'] == search_mood]
        if search_artist: results = [t for t in results if search_artist.lower() in t['artist'].lower()]
        st.dataframe(pd.DataFrame(results))

elif page == "Smart Playlists":
    st.header("🤖 Smart Playlists")
    rule = st.text_input("Rule (e.g., happy, rap, sad, angry, romantic, rating>4, last_month)")
    if st.button("Create Smart Playlist"):
        last_month = datetime.now() - timedelta(days=30)
        smart_tracks = []
        for t in library:
            added_date = datetime.fromisoformat(t['added_at'][:-1])
            rating = metadata.get(t['id'], {}).get('rating', 0)
            mood = t.get('mood', '').lower()
            match = False
            if 'happy' in rule.lower() and mood == 'happy':
                match = True
            if 'sad' in rule.lower() and mood == 'sad':
                match = True
            if 'energetic' in rule.lower() and mood == 'energetic':
                match = True
            if 'calm' in rule.lower() and mood == 'calm':
                match = True
            if 'rap' in rule.lower() and mood == 'rap':
                match = True
            if 'angry' in rule.lower() and mood == 'angry':
                match = True
            if 'romantic' in rule.lower() and mood == 'romantic':
                match = True
            if 'chill' in rule.lower() and mood == 'chill':
                match = True
            if 'rating>' in rule:
                threshold = int(rule.split('rating>')[1])
                if rating > threshold:
                    match = True
            if 'last_month' in rule.lower() and added_date > last_month:
                match = True
            if match:
                smart_tracks.append(t['id'])
        if smart_tracks:
            name = f"Smart: {rule}"
            playlist_id = create_playlist(name, smart_tracks)
            if playlist_id:
                st.success(f"Smart playlist '{name}' created with {len(smart_tracks)} tracks! ID: {playlist_id}")
                smart_df = pd.DataFrame([t for t in library if t['id'] in smart_tracks])
                smart_df.to_csv(f"{name.replace(' ', '_')}.csv", index=False)
                st.download_button("Download Playlist CSV", data=smart_df.to_csv(index=False), file_name=f"{name}.csv")
        else:
            st.warning("No tracks match the rule. Try 'happy', 'rap', 'angry', or 'rating>3'.")

elif page == "Rate Tracks":
    st.header("⭐ Rate Tracks")
    if library:
        track_to_rate = st.selectbox("Track", [t['name'] for t in library])
        rating = st.slider("Rating", 1, 5)
        mood_override = st.selectbox("Override Mood (optional)", ["", "Happy", "Sad", "Energetic", "Calm", "Rap", "Angry", "Romantic", "Chill"])
        if st.button("Save Rating & Mood"):
            track_id = next(t['id'] for t in library if t['name'] == track_to_rate)
            metadata[track_id] = {'rating': rating}
            if mood_override:
                metadata[track_id]['mood_override'] = mood_override
                for track in st.session_state.library:
                    if track['id'] == track_id:
                        track['mood'] = mood_override
                        break
            save_library_metadata(metadata)
            st.success("Rating and mood saved!!!")
    else:
        st.error("Load library first!")

if not library:
    st.info("Load your library first!")