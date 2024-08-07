from pydantic import BaseModel
from typing import Optional
class WeatherDataCreate(BaseModel):
    city: str
    

class WeatherDataResponse(BaseModel):
    city: str
    description: str
    temperature: float
    feels_like :float
    temp_min = float
    temp_max = float
    pressure = int
    humidity = int
    visibility = int
    wind_speed = float
    wind_deg = int
    clouds = int
    # dt = Column(DateTime, default=datetime.utcnow)

    class Config:
        orm_mode = True
