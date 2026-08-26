project link : https://movie-recommendation-system-4hvz.onrender.com/
# Architecture for Movie Recommendation System

movie_recommendation_project/
│
├── venv/                    
├── data/
│   ├── tmdb_5000_movies.csv
│   └── tmdb_5000_credits.csv
├── notebooks/                
│   └── exploration.ipynb
│--- recommender(virtual environment)
|--- .gitignore
|--- .gitattributes(storing the LFS on github)
├── app/                       
│   └── app.py
├── models/                    
│   └── similarity_matrix.pkl
├── requirements.txt
└── README.md

# Work flow of project

1. Use imdb datasets of 5000 movies(crredit.csv and movies.csv)
2. merging both the data on the behalf of the title
3. Use movie_id, tittle, overview, generes, keyward, cast, crew column for EDA
4.  remove null values form overview
5.  Extracting the name and directors name from the keywards, cast, crew, generes
6.  make a common column name tag to merge all the above features
7.  remove space between two word of the name name also remove spacing
8.  apply stemming to remove same meaning word
9.  use vectorization to convert all the text to vector
10.  use cosine_similarity vector to find the relation between two word
11.  use render platform in deployment
