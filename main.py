from uuid import uuid4

from fastapi import FastAPI, HTTPException, status
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

class BookingRequest(BaseModel):
    showtime_id: int
    seat_label: str
    customer_name: str

class BookingResponse(BaseModel):
    booking_id: str
    showtime_id: int
    seat_label: str
    customer_name: str
    status: str
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

bookings: list[dict] = []
# --- Helper Functions ---

def find_showtime(showtime_id: int) -> dict | None:
    for showtime in showtimes:
        if showtime["id"] == showtime_id:
            return showtime
    return None

def find_booking(booking_id: str) -> dict | None:
    for booking in bookings:
        if booking["booking_id"] == booking_id:
            return booking
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

# --- Booking Endpoints ---

@app.post("/bookings", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(request: BookingRequest):
    # Check that the showtime exists
    showtime = find_showtime(request.showtime_id)
    if not showtime:
        raise HTTPException(status_code=404, detail="Showtime not found")

    # Check that the seat label is valid
    if request.seat_label not in showtime["seats"]:
        raise HTTPException(status_code=400, detail=f"Seat {request.seat_label} does not exist for this showtime")
    if not showtime["seats"][request.seat_label]:
        raise HTTPException(status_code=409, detail=f"Seat {request.seat_label} is already booked for this showtime")
    # Mark the seat as unavailable
    showtime["seats"][request.seat_label] = False

        # Create the booking record
    booking = {
        "booking_id": str(uuid4()),
        "showtime_id": request.showtime_id,
        "seat_label": request.seat_label,
        "customer_name": request.customer_name,
        "status": "confirmed",
    }
    bookings.append(booking)

    return booking

@app.get("/bookings", response_model=list[BookingResponse])
def get_bookings():
    return bookings

@app.get("/bookings/{booking_id}", response_model=BookingResponse)
def get_booking(booking_id: str):
    booking = find_booking(booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking