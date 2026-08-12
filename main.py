from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Movie Ticket Booking API")

# --- Data Models ---

class Movie(BaseModel):
    id: int
    title: str
    genre: str
    duration_minutes: int

class Showtime(BaseModel):
    id: int
    movie_id: int
    date_time: str
    seats: dict[str, bool]    

# --- In-Memory Data ---

movies: list[dict] = [
    {"id": 1, "title": "The Matrix", "genre": "Sci-Fi", "duration_minutes": 136},
    {"id": 2, "title": "Inception", "genre": "Sci-Fi", "duration_minutes": 148},
    {"id": 3, "title": "The Dark Knight", "genre": "Action", "duration_minutes": 152},
]

showtimes: list[dict] = [
    {
        "id": 1,
        "movie_id": 1,
        "date_time": "2026-07-25 19:00",
        "seats": {f"{row}{num}": True for row in "AB" for num in range(1, 6)},
    },
    {
        "id": 2,
        "movie_id": 2,
        "date_time": "2026-07-25 21:00",
        "seats": {f"{row}{num}": True for row in "AB" for num in range(1, 6)},
    },
]

# --- Helper Functions ---

def find_showtime(showtime_id: int) -> dict | None:
    for showtime in showtimes:
        if showtime["id"] == showtime_id:
            return showtime
    return None

# --- Movie Endpoints ---

@app.get("/movies", response_model=list[Movie])
def get_movies():
    return movies

@app.get("/movies/{movie_id}", response_model=Movie)
def get_movie(movie_id: int):
    for movie in movies:
        if movie["id"] == movie_id:
            return movie
    raise HTTPException(status_code=404, detail="Movie not found")


# --- Showtime Endpoints ---

@app.get("/showtimes", response_model=list[Showtime])
def get_showtimes():
    return showtimes

@app.get("/showtimes/{showtime_id}", response_model=Showtime)
def get_showtime(showtime_id: int):
    showtime = find_showtime(showtime_id)
    if not showtime:
        raise HTTPException(status_code=404, detail="Showtime not found")
    return showtime