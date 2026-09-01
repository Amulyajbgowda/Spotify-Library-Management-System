# Spotify Library Management System 🎵

A Python-based music library management and analytics application that integrates with the Spotify Web API to analyze user playlists, classify songs based on mood, and generate intelligent playlists.

The system retrieves music information from a user's Spotify library and processes track metadata and audio features using Machine Learning to provide mood-based song classification and interactive music analytics.

---

## 🖼️ Application Screenshots

The project was developed as an interactive Streamlit application for Spotify library analysis and management.

> Screenshots demonstrate the application interface and functionality during the development of the project.

### Dashboard

![Dashboard](screenshots/dashboard.png)

### Music Analytics

![Music Analytics](screenshots/analytics.png)

### Playlist Analysis

![Playlist Analysis](screenshots/playlist-analysis.png)

---

## 🚀 Features

### 🎵 Spotify Library Management

- Spotify OAuth authentication
- Access and analyze user playlists
- Retrieve playlist tracks
- Extract track metadata
- Support for private and public playlists
- Automatic music library analysis
- Smart playlist creation through Spotify Web API

### 🎶 Track Information Analysis

The system extracts and analyzes:

- Track name
- Artist
- Album
- Release year
- Genre
- Track duration
- Date added

### 🧠 Mood-Based Song Classification

The application uses a trained Machine Learning model to classify songs into different mood categories.

Supported moods include:

- Happy
- Sad
- Angry
- Chill
- Energetic
- Romantic
- Rap

The classification process combines:

- Spotify audio features
- Machine Learning predictions
- Genre-based classification
- Song name analysis
- Artist-based mood overrides
- User-defined mood overrides

### 📊 Music Analytics Dashboard

The Streamlit dashboard provides interactive insights into the user's music library, including:

- Mood distribution
- Genre distribution
- Playlist analysis
- Track analysis
- Audio feature analysis
- Music library patterns
- Interactive visualizations

### 🤖 Smart Playlist Generation

The system can automatically create playlists based on analyzed music data.

Tracks can be organized according to:

- Mood
- Genre
- Music characteristics
- Classification results

---

## 🏗️ Project Architecture

```text
Spotify-Library-Enhancer/
│
├── spotify_en_newmood.py
│   └── Main Streamlit application
│
├── spotify_utils.py
│   └── Spotify API utility functions
│
├── train_mood_model.py
│   └── Machine Learning model training
│
├── mood_model.pkl
│   └── Trained mood classification model
│
├── spotify_mood_data.csv
│   └── Dataset used for model training
│
├── screenshots/
│   ├── dashboard.png
│   ├── analytics.png
│   └── playlist-analysis.png
│
├── requirements.txt
│   └── Project dependencies
│
├── .env.example
│   └── Environment variable template
│
├── .gitignore
│   └── Ignored files configuration
│
└── README.md
```

---

## 🧠 System Workflow

```text
                  ┌─────────────────────┐
                  │   User Login        │
                  │ Spotify OAuth       │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ Spotify Web API     │
                  │ Authentication      │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ Retrieve Playlists  │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ Extract Track Data  │
                  │ Metadata + Genre    │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ Audio Feature       │
                  │ Analysis            │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ Machine Learning    │
                  │ Mood Classification │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ Music Analytics     │
                  │ Dashboard           │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ Smart Playlist      │
                  │ Generation          │
                  └─────────────────────┘
```

---

## 💻 Technology Stack

### Application

- Python
- Streamlit

### Spotify Integration

- Spotify Web API
- Spotipy
- Spotify OAuth

### Machine Learning

- Scikit-learn
- Joblib

### Data Processing

- Pandas

### Data Visualization

- Plotly
- Streamlit Interactive Charts

### Configuration

- Python-dotenv

---

## ⚙️ Installation

### Prerequisites

Make sure you have installed:

- Python 3.9+
- pip
- Git
- Spotify Developer Account

---

## 🔧 Project Setup

### 1. Clone the repository

```bash
git clone https://github.com/Amulyajbgowda/Spotify-Library-Enhancer.git
cd Spotify-Library-Enhancer
```

### 2. Create a virtual environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Spotify API Configuration

### 1. Create Spotify Developer Credentials

Create a Spotify application and obtain:

- Client ID
- Client Secret

### 2. Configure Redirect URI

Configure the following redirect URI:

```text
http://localhost:8501
```

### 3. Create Environment Variables

Create a `.env` file based on `.env.example`.

Example:

```env
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
SPOTIFY_REDIRECT_URI=http://localhost:8501
```

> Never commit your actual `.env` file or Spotify credentials to GitHub.

---

## ▶️ Running the Application

Start the Streamlit application:

```bash
streamlit run spotify_en_newmood.py
```

The application will typically run at:

```text
http://localhost:8501
```

---

## 🧠 Machine Learning Model

The project includes a trained Machine Learning model:

```text
mood_model.pkl
```

The model uses Spotify audio features to classify songs into different mood categories.

The model is trained using the dataset:

```text
spotify_mood_data.csv
```

The training script is available in:

```text
train_mood_model.py
```

To retrain the model:

```bash
python train_mood_model.py
```

---

## 📊 Dataset

The project includes a music dataset containing Spotify track information and audio features.

The dataset includes:

- Danceability
- Energy
- Key
- Loudness
- Mode
- Speechiness
- Acousticness
- Instrumentalness
- Liveness
- Valence
- Tempo

These features are used as input for the mood classification model.

---

## 🔌 Spotify API Integration

The project uses the Spotify Web API through the Spotipy Python library.

The application requests permissions for:

- Reading user playlists
- Reading private playlists
- Creating private playlists
- Creating public playlists
- Reading the user's saved music library

OAuth scopes:

```text
playlist-read-private
playlist-modify-private
playlist-modify-public
user-library-read
```

---

## ⚠️ Current Spotify API Availability

This project was originally developed and tested using the Spotify Web API during its development period.

The application relies on Spotify API access for core functionality such as:

- User authentication
- Playlist retrieval
- Track metadata extraction
- Genre analysis
- Audio feature retrieval
- Smart playlist creation

Spotify's API access policies and account eligibility requirements may change over time. As a result, some API-dependent functionality may not currently be available for all developer accounts.

Users may encounter authorization or access errors when attempting to retrieve playlists or access certain Spotify resources depending on current Spotify API policies and account eligibility.

The complete application source code, Machine Learning model, training dataset, dashboard implementation, and project architecture are included in this repository.

Application screenshots are provided above to demonstrate the functionality and output of the system during the project's development.

---

## 🔒 Security and Environment Variables

Sensitive credentials should never be committed to GitHub.

The project includes:

```text
.env.example
```

Use it as a template.

### Windows

```bash
copy .env.example .env
```

### Linux/macOS

```bash
cp .env.example .env
```

The `.gitignore` excludes sensitive and generated files such as:

```text
.env
.cache
venv/
.venv/
__pycache__/
*.pyc
```

---

## ⚡ Project Highlights

- Spotify Web API integration
- OAuth authentication
- User playlist analysis
- Music metadata extraction
- Genre analysis
- Audio feature analysis
- Machine Learning-based mood classification
- Genre-based music organization
- Smart playlist generation
- Interactive Streamlit dashboard
- Music analytics and visualization
- Persistent user mood overrides
- Automated playlist creation

---

## 🔮 Future Improvements

Possible future enhancements include:

- Replace the existing mood classification model with modern deep learning approaches
- Content-based music recommendation system
- Similar song detection
- Personalized music recommendations
- Music clustering based on audio features
- Explainable AI-based music recommendations
- Hybrid recommendation system
- Advanced playlist quality analysis
- Natural language music search
- Sentiment-aware playlist generation
- Support for additional music APIs
- Advanced listening analytics
- Improved dashboard visualizations
- Real-time music recommendations

---

## 🛠️ Development

### Run the Streamlit development server

```bash
streamlit run spotify_en_newmood.py
```

### Retrain the Machine Learning model

```bash
python train_mood_model.py
```

---

## 📄 License

This project is intended for educational and portfolio purposes.

---

## 👨‍💻 Author

**Amulya**

MCA Graduate | Software Developer | Python | Machine Learning | Data Analytics

GitHub: Amulyajbgowda

⭐ If you found this project interesting, consider giving the repository a star!
