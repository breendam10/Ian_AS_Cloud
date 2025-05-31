# C:\Users\ianes\Desktop\AS Cloud\config.py

import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR / '.env')

class Config:
    ENV   = os.getenv('FLASK_ENV', 'production')
    DEBUG = ENV == 'development'

    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
