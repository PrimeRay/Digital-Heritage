import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://etm_user:00000000@localhost/elderly_time_manager')
    SQLALCHEMY_TRACK_MODIFICATIONS = False