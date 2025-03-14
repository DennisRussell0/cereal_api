# Contains Flask configuration settings, including the SQLite database path

import os

# Define the base directory and database file path
basedir = os.path.abspath(os.path.dirname(__file__))  # Get the absolute path of the current directory
db_path = os.path.join(basedir, "instance", "cereals.db")  # Define the relative path for the database file

class Config:
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "fallback_secret_key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable modification tracking for performance improvements
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{db_path}"  # Define the database URI (SQLite in this case)
