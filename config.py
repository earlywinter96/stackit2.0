# StackIt - Q&A Platform using Flask + PostgreSQL
# Step-by-step setup starting here.

# First, we set up the Flask project directory structure
# Folder structure:
# stackit/
# ├── app/
# │   ├── __init__.py
# │   ├── models.py
# │   ├── routes.py
# │   ├── templates/
# │   ├── static/
# ├── config.py
# ├── run.py
# ├── requirements.txt
# └── README.md

# Step 1: Create virtual environment and install dependencies
# Run these commands in terminal:
# python3 -m venv venv
# source venv/bin/activate  (on macOS/Linux)
# pip install flask flask_sqlalchemy psycopg2-binary flask-login
# pip freeze > requirements.txt

# Step 2: Create config.py to hold database URI and app config

# config.py
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))  # ✅ Load from .env

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    # ✅ Use in-memory SQLite to avoid file system issues
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///:memory:'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
