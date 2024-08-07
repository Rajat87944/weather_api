from fastapi import FastAPI
from routes.weather import router as weather_router
from database import Base, engine

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Fast API",
    version="0.1.0"
)

app.include_router(weather_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Weather API!"}
