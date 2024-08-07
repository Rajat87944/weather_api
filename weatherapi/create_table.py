# create_tables.py
import os
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from models.weather import Base


DATABASE_URL = os.getenv('DATABASE_URL') or \
    'postgresql://postgres:%s@localhost:5432/socal_media' % quote_plus("Rajat@123")
engine = create_engine(DATABASE_URL)
# Create all tables
Base.metadata.create_all(bind=engine)

print("Tables created successfully.")