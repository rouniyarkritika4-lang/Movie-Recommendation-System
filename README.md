# 🎬 CineMatch — Movie Recommendation System

An AI/ML-powered content-based movie recommendation system built with **Python, scikit-learn, FastAPI, and Streamlit**. It suggests similar movies using **TF-IDF vectorization + Cosine Similarity** on movie overviews, genres, and taglines, then enriches every result with live posters, ratings, and details from **The Movie Database (TMDB) API**.

**Version:** 3.0 (API) | **Python:** 3.11.9 | **Status:** ✅ Deployed

## 🌐 Live Demo

**Frontend (Streamlit):** [movie-recommendation-system-kaaw2pifc8y8ofxpexnvyv.streamlit.app](https://movie-recommendation-system-kaaw2pifc8y8ofxpexnvyv.streamlit.app/)
**Backend (FastAPI, Render):** `https://movie-recommendation-system-t1c6.onrender.com`

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://movie-recommendation-system-kaaw2pifc8y8ofxpexnvyv.streamlit.app/)

✨ No installation needed to try the hosted version — just open the Streamlit link in your browser.
**Note:** the backend is hosted on Render's free tier, so the first request after a period of inactivity may take 30–60 seconds to "wake up."

---

## 🚀 Features

- **Content-based recommendations** — finds movies similar to a chosen title using TF-IDF + Cosine Similarity over each movie's overview, genres, and tagline.
- **Live movie search** — search TMDB directly by title with an autocomplete-style dropdown of matches.
- **Rich movie details page** — poster, backdrop, rating, release year, runtime, language, genre tags, and overview.
- **"Similar Movies" panel** — combines local TF-IDF recommendations with live TMDB posters; falls back to genre-based discovery if a title isn't in the local dataset.
- **Browsable home feed** — Trending, Popular, Hit Movies (Top Rated), Now Playing, and Coming Soon rows, pulled live from TMDB.
- **Genre discovery** — browse popular movies filtered by genre.
- **Trailer shortcut** — one-click link to search the movie's trailer on YouTube.
- **Custom dark UI** — a purple/dark "CineMatch" themed interface built with Streamlit + custom CSS (no default Streamlit sidebar).
- **Resilient API layer** — every TMDB/network call is wrapped so a failure degrades gracefully instead of crashing the app.

---

## 📂 Complete Project Structure

```
Movie-Recommendation-System/
│
├── 🐍 main.py                     # FastAPI backend — serves recommendations & TMDB data
├── 🐍 app.py                      # Streamlit frontend — CineMatch UI
├── 📓 movies.ipynb                # Full ML pipeline: cleaning, TF-IDF, cosine similarity
├── 📋 requirements.txt            # Python dependencies
├── 📄 runtime.txt / .python-version  # Python version pin (3.11.9) for deployment
├── 🔒 .env                        # TMDB_API_KEY (not committed — see Setup)
├── 📖 README.md                   # This file
│
├── 📁 data/
│   └── movies_metadata.csv        # Raw TMDB movies metadata dataset (~45,000 movies)
│
├── 📁 model/                      # Serialized ML artifacts (tracked via Git LFS)
│   ├── df.pkl                     # Cleaned DataFrame (title, tags, lemmatized_title, ...)
│   ├── tfidf.pkl                  # Fitted TfidfVectorizer
│   ├── tfidf_matrix.pkl           # TF-IDF sparse matrix for all movies
│   └── indices.pkl                # Lookup: lemmatized title → row index in df
│
└── 📁 streamlit/
    └── Config.toml                # Streamlit configuration
```

## 📋 File Descriptions

| File | Purpose | Type |
|---|---|---|
| `main.py` | FastAPI app: loads the pickled model at startup, exposes recommendation & TMDB proxy endpoints | Python / API |
| `app.py` | Streamlit app: search, home feed, movie details, and "similar movies" UI | Python / Frontend |
| `movies.ipynb` | End-to-end notebook — data cleaning, NLP preprocessing, TF-IDF fitting, cosine similarity, and pickling the model artifacts | Jupyter Notebook |
| `requirements.txt` | Pinned Python dependencies for both the API and the Streamlit app | Configuration |
| `data/movies_metadata.csv` | Source dataset (title, overview, genres, tagline, popularity, vote_average, etc.) | Data File |
| `model/df.pkl` | Preprocessed movie table used at inference time to map indices back to titles | Serialized Data |
| `model/tfidf.pkl` | The fitted `TfidfVectorizer` (vocabulary + IDF weights) | Serialized Model |
| `model/tfidf_matrix.pkl` | Precomputed TF-IDF vectors for every movie (sparse matrix) | Serialized Model |
| `model/indices.pkl` | Maps a lemmatized movie title to its row index for fast lookup | Serialized Data |
| `.env` | Holds the `TMDB_API_KEY` used by `main.py` to call the TMDB API | Config (secret) |

---

## 🧠 Machine Learning Pipeline

The full pipeline is documented step-by-step in **`movies.ipynb`**.

### 1. Data Loading & Cleaning
- Loads `movies_metadata.csv` (~45,000 movies).
- Drops duplicate rows.
- Keeps only the columns needed for recommendations: `title`, `overview`, `genres`, `tagline`, `vote_average`, `popularity`.
- Drops rows with a missing `title`.
- Fills missing `overview` and `tagline` values with empty strings so no row is dropped unnecessarily.

### 2. Feature Extraction
- `genres` arrives as a stringified list of dicts (e.g. `"[{'id': 28, 'name': 'Action'}, ...]"`). This is parsed with `ast.literal_eval` and flattened into a plain space-separated genre string (e.g. `"Action Adventure Fantasy Science Fiction"`).

### 3. Building the "Tags" Field
A single combined text field is created per movie:

```python
df['tags'] = df['overview'] + " " + df['genres'] + " " + df['tagline']
```

This `tags` string is what the model actually compares between movies.

### 4. NLP Text Preprocessing
Using **NLTK**, each `tags` string is:
1. Lowercased
2. Stripped of punctuation/numbers (regex, letters + spaces only)
3. Stripped of English stopwords
4. Lemmatized (`WordNetLemmatizer`)

Movie titles are separately lemmatized (without stopword/punctuation removal) into a `lemmatized_title` column, which becomes the lookup key for recommendations.

### 5. Vectorization — TF-IDF
```python
tfidf = TfidfVectorizer(max_features=50000, ngram_range=(1, 2), stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['tags'])
```
- **Unigrams + bigrams** (`ngram_range=(1,2)`) so the model captures short phrases, not just single words.
- Capped at **50,000 features** to keep the vocabulary manageable.

### 6. Similarity — Cosine Similarity
For a given movie, its TF-IDF vector is compared against every other movie's vector:

```python
similarity_score = cosine_similarity(tfidf_matrix[idx], tfidf_matrix).flatten()
similar_idx = similarity_score.argsort()[::-1][1:n+1]
```

The top **N** movies with the highest cosine similarity (excluding the movie itself) are returned as recommendations.

### 7. Persisting the Model
The trained artifacts are serialized with `pickle` so the API can load them instantly without retraining:

```python
pickle.dump(tfidf_matrix, open('tfidf_matrix.pkl', 'wb'))
pickle.dump(indices, open('indices.pkl', 'wb'))
df.to_pickle('df.pkl')
pickle.dump(tfidf, open('tfidf.pkl', 'wb'))
```

These four files live in `model/` and are loaded once, at startup, by the FastAPI backend.

---

## 🏗️ Application Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                        SYSTEM ARCHITECTURE                      │
├────────────────────────────────────────────────────────────────┤
│                                                                  │
│   Jupyter Notebook (movies.ipynb)                               │
│     ├─ Clean & preprocess movies_metadata.csv                   │
│     ├─ Build TF-IDF matrix                                      │
│     └─ Export df.pkl / tfidf.pkl / tfidf_matrix.pkl / indices.pkl│
│                        ↓                                        │
│   FastAPI Backend (main.py)                                     │
│     ├─ Loads all .pkl artifacts on startup                      │
│     ├─ /recommend/tfidf   → local content-based recommendations │
│     ├─ /movie/search      → details + TF-IDF recs + genre recs  │
│     ├─ /tmdb/search       → live TMDB keyword search             │
│     ├─ /home              → trending / popular / top rated etc. │
│     ├─ /discover          → browse by genre                      │
│     └─ /movie/id/{id}     → full TMDB movie details              │
│                        ↓  (HTTP/JSON)                            │
│   Streamlit Frontend (app.py) — "CineMatch"                     │
│     ├─ Search bar + autocomplete dropdown                       │
│     ├─ Home feed (Trending / Popular / Top Rated / ...)         │
│     ├─ Movie details page (poster, genres, overview, trailer)   │
│     └─ "Similar Movies" row (TF-IDF → genre fallback)           │
│                        ↓                                        │
│   TMDB API (external) — posters, ratings, live search, discover │
│                                                                  │
└────────────────────────────────────────────────────────────────┘
```

**Why split TF-IDF (local) and TMDB (live) data?** The local dataset (`movies_metadata.csv`) gives fast, offline content-based similarity, but it doesn't have posters or up-to-date info. TMDB is queried live to attach posters, ratings, and metadata to whatever the TF-IDF model recommends — the two are stitched together in `/movie/search`.

---

## ⚙️ Installation & Setup

### Prerequisites
- **Python 3.11.9** (pinned in `runtime.txt` / `.python-version`)
- **pip**
- **Git** (with [Git LFS](https://git-lfs.com/) — the `data/*.csv` and `model/*.pkl` files are tracked via LFS)
- A **free TMDB API key** — [themoviedb.org/settings/api](https://www.themoviedb.org/settings/api)

### 1. Clone the repository

```bash
git lfs install
git clone https://github.com/rouniyarkritika4-lang/Movie-Recommendation-System.git
cd Movie-Recommendation-System
```

> If the files in `model/` or `data/` look like small text pointers instead of real data, run `git lfs pull`.

### 2. Create a virtual environment

**Linux/macOS**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows (PowerShell)**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Key packages:**
- `fastapi`, `uvicorn`, `httpx`, `python-dotenv` — API backend
- `pandas`, `numpy`, `scipy`, `scikit-learn`, `joblib` — ML / data layer
- `streamlit` — frontend

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
TMDB_API_KEY=your_tmdb_api_key_here
```

The API will refuse to start without this key (`main.py` raises a `RuntimeError` at import time if it's missing).

### 5. Run the backend (FastAPI)

```bash
uvicorn main:app --reload --port 8000
```

- API docs (Swagger UI): `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`

### 6. Run the frontend (Streamlit)

In a second terminal:

```bash
export API_BASE=http://localhost:8000        # Windows: set API_BASE=http://localhost:8000
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

> By default `app.py` points `API_BASE` at the deployed Render backend, so if you skip step 5–6's env var, the local Streamlit app will still work against the hosted API.

---

## 🎯 Usage Guide

1. **Search** — type a movie title (e.g. "batman", "avenger", "love") in the search bar.
2. **Pick a result** — choose the exact movie from the dropdown of TMDB matches.
3. **View details** — see the poster, backdrop, rating, runtime, language, genres, and overview.
4. **Watch trailer** — click "🎬 Watch Trailer" to jump to a YouTube search for it.
5. **Browse similar movies** — scroll the "🔎 Similar Movies" row, generated first from the TF-IDF model, falling back to TMDB genre-based discovery if no local match exists.
6. **Explore the home feed** — use the left sidebar to switch between Trending, Popular, Hit Movies, Now Playing, and Coming Soon.

---

## 🔌 API Reference

All endpoints are served from `main.py`. Interactive docs are auto-generated at `/docs`.

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Health check |
| `GET` | `/home?category=popular&limit=24` | Home feed (`trending`, `popular`, `top_rated`, `upcoming`, `now_playing`) |
| `GET` | `/genres` | List of TMDB genres |
| `GET` | `/discover?genre_id=28&limit=30` | Popular movies for a given genre |
| `GET` | `/tmdb/search?query=batman` | Raw TMDB keyword search (multiple results) |
| `GET` | `/movie/id/{tmdb_id}` | Full TMDB details for one movie |
| `GET` | `/recommend/genre?tmdb_id=...&limit=18` | Genre-based recommendations for a TMDB movie |
| `GET` | `/recommend/tfidf?title=avatar&top_n=10` | Local TF-IDF content-based recommendations |
| `GET` | `/movie/search?query=avatar` | **Bundle**: TMDB details + TF-IDF recommendations + genre recommendations |

Example:
```bash
curl "http://localhost:8000/recommend/tfidf?title=avatar&top_n=5"
```
```json
[
  {"title": "Aliens", "score": 0.31},
  {"title": "Guardians of the Galaxy", "score": 0.27},
  ...
]
```

---

## ⚠️ Limitations

- **Cold-start problem** — a movie not present in `movies_metadata.csv` (or with a title TMDB and the local dataset disagree on) has no TF-IDF recommendations; the app falls back to TMDB genre-based discovery instead.
- **Text-only similarity** — recommendations are based purely on overview/genre/tagline text, not on user ratings, watch history, or collaborative signals (no personalization).
- **Static dataset** — the local dataset is a snapshot; new releases won't have TF-IDF recommendations until the notebook is re-run and the pickles are regenerated.
- **TMDB rate limits & downtime** — since posters, search, and live details all depend on the TMDB API, an outage or rate limit there will degrade the browsing experience (recommendations still work locally).
- **Free-tier hosting** — the Render-hosted backend may sleep after inactivity, causing a slow first request.

---

## 🐛 Troubleshooting

**`RuntimeError: TMDB_API_KEY missing`**
→ Create a `.env` file in the project root with `TMDB_API_KEY=your_key_here`, then restart `uvicorn`.

**Streamlit shows "Could not connect to the movie server."**
→ Make sure the FastAPI backend is running and that `API_BASE` points to the correct URL (`http://localhost:8000` for local dev).

**Model files look tiny / `pickle.load` fails**
→ You likely don't have Git LFS installed. Run `git lfs install && git lfs pull` in the repo.

**`ModuleNotFoundError`**
→ Confirm your virtual environment is activated, then re-run `pip install -r requirements.txt`.

**Port already in use**
→ Run the API on another port: `uvicorn main:app --reload --port 8001`, and update `API_BASE` accordingly.

**First request to the live demo is very slow**
→ Expected — the Render free tier spins down the backend after inactivity. Subsequent requests will be fast.

---

## 📈 Future Improvements

- [ ] Add collaborative filtering (user ratings) for a hybrid recommender
- [ ] Personalized recommendations based on watch/search history
- [ ] Cache TMDB responses server-side to reduce API calls and latency
- [ ] Scheduled retraining pipeline to keep the TF-IDF model current with new releases
- [ ] Add automated tests for the recommendation endpoints
- [ ] User accounts with watchlists and ratings

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add some feature"`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📜 License

This project is open source. Add a `LICENSE` file (e.g. MIT) if you'd like to formalize reuse terms.

---

## 🙋 Author

**Kritika Rouniyar**
GitHub: [@rouniyarkritika4-lang](https://github.com/rouniyarkritika4-lang)

## 🙏 Acknowledgements

- [TMDB](https://www.themoviedb.org/) for the movie dataset, images, and live API
- [scikit-learn](https://scikit-learn.org/) for `TfidfVectorizer` and `cosine_similarity`
- [NLTK](https://www.nltk.org/) for stopword removal and lemmatization
