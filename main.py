from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Movie Ticket Booking API")

# --- Data Models ---

class Movie(BaseModel):
    id: int
    title: str
    genre: str
    duration_minutes: int

# --- In-Memory Data ---

movies: list[dict] = [
    {"id": 1, "title": "The Matrix", "genre": "Sci-Fi", "duration_minutes": 136},
    {"id": 2, "title": "Inception", "genre": "Sci-Fi", "duration_minutes": 148},
    {"id": 3, "title": "The Dark Knight", "genre": "Action", "duration_minutes": 152},
]

# --- Movie Endpoints ---

@app.get("/movies", response_model=list[Movie])
def get_movies():
    return movies

@app.get("/movies/{movie_id}", response_model=Movie)
def get_movie(movie_id: int):
    for movie in movies:
        if movie["id"] == movie_id:
            return movie