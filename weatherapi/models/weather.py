from sqlalchemy import Column, Integer, String, Float
from database import Base

class Weather(Base):
    __tablename__ = "weather"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String)
    description = Column(String)
    temperature = Column(Float)
    feels_like = Column(Float)
    temp_min = Column(Float)
    temp_max = Column(Float)
    pressure = Column(Integer)
    humidity = Column(Integer)
    visibility = Column(Integer)
    wind_speed = Column(Float)
    wind_deg = Column(Integer)
    clouds = Column(Integer)
