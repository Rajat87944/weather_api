from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models.weather import Weather
from schemas.weather import WeatherDataCreate, WeatherDataResponse
from database import get_db
import requests
import math
from config import OPENWEATHER_API_KEY


router = APIRouter()

def get_weather(city: str, api_key: str):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather_description = data["weather"][0]["description"]
        temperature = math.floor(data["main"]["temp"] - 273.15)  # Convert Kelvin to Celsius and floor the value
        feels_like = math.floor(data["main"].get("feels_like", 0) - 273.15)  # Convert Kelvin to Celsius and floor the value if available
        temp_min = math.floor(data["main"].get("temp_min", 0) - 273.15)  # Convert Kelvin to Celsius and floor the value if available
        temp_max = math.floor(data["main"].get("temp_max", 0) - 273.15)  # Convert Kelvin to Celsius and floor the value if available
        pressure = data["main"].get("pressure", None)
        humidity = data["main"].get("humidity", None)
        visibility = data.get("visibility", None)
        wind_speed = data["wind"].get("speed", None)
        wind_deg = data["wind"].get("deg", None)
        clouds = data["clouds"].get("all", None)
        
        return {
            "city": city,
            "description": weather_description,
            "temperature": temperature,
            "feels_like": feels_like,
            "temp_min": temp_min,
            "temp_max": temp_max,
            "pressure": pressure,
            "humidity": humidity,
            "visibility": visibility,
            "wind_speed": wind_speed,
            "wind_deg": wind_deg,
            "clouds": clouds
        }
    else:
        return {
            "error": f"Unable to retrieve weather data. Status code: {response.status_code}",
            "content": response.text
        }

@router.post("/weather/", response_model=WeatherDataResponse, tags=["Weather"])
def create_weather_data(weather_data: WeatherDataCreate, db: Session = Depends(get_db)):
    weather_info = get_weather(weather_data.city, OPENWEATHER_API_KEY)
    if "error" in weather_info:
        raise HTTPException(status_code=404, detail="Weather data not found")
    
    # Create a new Weather object and add it to the database
    weather_entry = Weather(
        city=weather_info["city"],
        description=weather_info["description"],
        temperature=weather_info["temperature"],
        feels_like=weather_info["feels_like"],
        temp_min=weather_info["temp_min"],
        temp_max=weather_info["temp_max"],
        pressure=weather_info["pressure"],
        humidity=weather_info["humidity"],
        visibility=weather_info["visibility"],
        wind_speed=weather_info["wind_speed"],
        wind_deg=weather_info["wind_deg"],
        clouds=weather_info["clouds"]
    )
    db.add(weather_entry)
    db.commit()
    db.refresh(weather_entry)
    return weather_entry
