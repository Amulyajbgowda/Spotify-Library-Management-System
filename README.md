\# Spotify Library Enhancer 🎵



A Python-based music library management and analytics application built using \*\*Streamlit, Spotify Web API, Machine Learning, and Data Visualization\*\*.



The application connects with a user's Spotify account, analyzes playlists and tracks, classifies songs based on mood and genre, and provides interactive insights through a dashboard.



\---



\## 🚀 Features



\* Spotify OAuth authentication

\* Access and analyze user playlists

\* Extract track metadata including artist, album, release year, genre, and duration

\* Automatic genre-based playlist organization

\* Mood classification using a Machine Learning model

\* Mood categories including Happy, Sad, Angry, Chill, Energetic, Romantic, and Rap

\* Interactive music analytics dashboard

\* Playlist and track analysis

\* Audio feature analysis

\* User mood overrides with metadata persistence

\* Rating and filtering capabilities

\* Data visualization using interactive charts



\---



\## 🧠 Machine Learning



The project uses a trained machine learning model to classify songs into different mood categories based on Spotify audio features.



\### Audio Features Used



\* Danceability

\* Energy

\* Key

\* Loudness

\* Mode

\* Speechiness

\* Acousticness

\* Instrumentalness

\* Liveness

\* Valence

\* Tempo



The trained model is stored as:



```text

mood\_model.pkl

```



The training process is available in:



```text

train\_mood\_model.py

```



\---



\## 🛠️ Technologies Used



\* Python

\* Streamlit

\* Spotipy

\* Spotify Web API

\* Scikit-learn

\* Pandas

\* Joblib

\* Plotly



\---



\## 📂 Project Structure



```text

slm/

│

├── spotify\_en\_newmood.py      # Main Streamlit application

├── spotify\_utils.py           # Spotify utility functions

├── train\_mood\_model.py        # ML model training

├── mood\_model.pkl             # Trained mood classification model

├── spotify\_mood\_data.csv      # Dataset

├── requirements.txt           # Project dependencies

├── .env.example               # Environment variable template

└── README.md

```



\---



\## ⚙️ Installation



\### 1. Clone the repository



```bash

git clone <repository-url>

cd slm

```



\### 2. Create a virtual environment



```bash

python -m venv venv

```



\### 3. Activate the virtual environment



\#### Windows



```bash

venv\\Scripts\\activate

```



\### 4. Install dependencies



```bash

pip install -r requirements.txt

```



\### 5. Configure environment variables



Create a `.env` file based on `.env.example`:



```env

SPOTIFY\_CLIENT\_ID=your\_spotify\_client\_id

SPOTIFY\_CLIENT\_SECRET=your\_spotify\_client\_secret

SPOTIFY\_REDIRECT\_URI=http://localhost:8501

```



\### 6. Run the application



```bash

streamlit run spotify\_en\_newmood.py

```



\---



\## 📊 Dataset



The project uses a music dataset containing Spotify track information and audio features for training the mood classification model.



The dataset includes features such as:



\* Danceability

\* Energy

\* Valence

\* Tempo

\* Loudness

\* Acousticness

\* Speechiness



\---



\## ⚠️ Spotify API Access Note



This project was originally developed using the Spotify Web API to access user playlists and music library data.



Recent changes to Spotify's developer access policies may require an eligible Spotify Premium developer account for certain API-dependent functionality. Therefore, the Spotify integration may require additional account eligibility to run successfully.



The core project implementation, machine learning model, dataset, and application source code are included in this repository.



\---



\## 🔮 Future Enhancements



\* Replace the existing mood classification model with modern deep learning approaches

\* Content-based music recommendation system

\* Similar song detection

\* Personalized music recommendations

\* Smart playlist generation

\* Playlist quality analysis and optimization

\* Music clustering based on audio features

\* Explainable music recommendations

\* Support for additional music APIs

\* Advanced user analytics



\---



\## 👤 Author



\*\*Amulya\*\*



\---



⭐ If you found this project interesting, consider giving it a star!



