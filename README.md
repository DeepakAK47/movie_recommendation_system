# Movie Recommendation System

A content-based movie recommendation web app built with Python and Streamlit. Select a movie from the list and the app returns five movies with similar content, together with their posters.

**Live application:** <https://movie-recommendation-system-4hvz.onrender.com/>

## What this project does

The recommender uses information about each movie, such as its genres, keywords, cast, and crew, to measure how similar movies are to one another. The similarity calculation is performed before deployment and saved as model artifacts, so the Streamlit app can make recommendations quickly without retraining the model every time it starts.

When a user clicks **Recommend**, the app:

1. Finds the selected movie in the saved movie index.
2. Reads its similarity scores.
3. Sorts the movies by similarity.
4. Removes the selected movie and keeps the five closest matches.
5. Requests poster images from the TMDB API.
6. Displays the recommended titles and posters in the Streamlit interface.

If a TMDB poster cannot be loaded, the app displays a placeholder image instead.

## Project workflow

The recommendation model was prepared from the TMDB 5000 movie and credits datasets:

1. Load the movie and credits data from `data/`.
2. Merge both datasets using the movie title.
3. Select useful recommendation features, including genres, keywords, cast, crew, title, and overview.
4. Remove or handle rows with missing overview data.
5. Extract relevant names and the director from the JSON-like cast, crew, genre, and keyword fields.
6. Combine the selected features into a single text field.
7. Normalize multi-word names so related tokens are represented consistently.
8. Apply stemming to reduce related words to a common form.
9. Convert the combined text into numerical vectors.
10. Use cosine similarity to calculate relationships between movies.
11. Save the processed movie data, title index, and similarity matrix in `models/`.
12. Load those saved artifacts in the Streamlit application.

The exploratory work and preprocessing are recorded in [`notebooks/exploration.ipynb`](D:/AIML/projects/movie_recommendation_system/notebooks/exploration.ipynb).

## Repository structure

```text
movie_recommendation_system/
├── app/
│   └── app.py                    # Streamlit user interface and recommendation logic
├── data/
│   ├── movies.csv                # Movie metadata
│   └── credits.csv              # Cast and crew metadata
├── models/
│   ├── movie_indices.pkl         # Movie title-to-row index mapping
│   ├── movies.pkl                # Processed movie metadata
│   └── similarity_matrix.pkl     # Precomputed movie similarity scores
├── notebooks/
│   ├── exploration.ipynb         # Data exploration and model preparation
│   └── movies.pkl                # Notebook-generated data artifact
├── requirements.txt              # Python dependencies
├── procfile                      # Render start command
└── setup.sh                      # Streamlit server configuration for deployment
```

## Run the application locally

### 1. Clone the repository

```bash
git clone https://github.com/DeepakAK47/movie_recommendation_system.git
cd movie_recommendation_system
```

### 2. Create and activate a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure poster requests (optional)

The app reads the TMDB API key from the `TMDB_API_KEY` environment variable. Recommendations still work without the key, but poster requests will use the fallback image.

PowerShell:

```powershell
$env:TMDB_API_KEY = "your_tmdb_api_key"
```

macOS or Linux:

```bash
export TMDB_API_KEY="your_tmdb_api_key"
```

Do not commit API keys or other secrets to the repository.

### 5. Start Streamlit

```bash
python -m streamlit run app/app.py
```

Open the local URL shown in the terminal, usually <http://localhost:8501>.

## Deployment

The project is configured for Render:

- `procfile` starts Streamlit on the port supplied by Render and listens on all interfaces.
- `setup.sh` writes the Streamlit server configuration used during deployment.
- Add `TMDB_API_KEY` as a secret environment variable in the Render service settings if poster images are required.

The deployment start command is:

```text
streamlit run app/app.py --server.port $PORT --server.address 0.0.0.0
```

## Technology stack

- Python
- Streamlit
- Pandas and NumPy
- Cosine similarity and precomputed pickle artifacts
- Requests with retry handling for TMDB poster requests
- Render for deployment

## Notes

- The application currently returns five recommendations for each selected movie.
- The saved files in `models/` are required for the app to start.
- The source CSV files are used for exploration and model preparation; the deployed app reads the saved model artifacts.
- TMDB poster images are fetched at runtime and are not stored in this repository.
