from fastapi import FastAPI

# Create the FastAPI application
app = FastAPI(title="Movie Ticket Booking API")

# Define a root endpoint that returns a greeting
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}