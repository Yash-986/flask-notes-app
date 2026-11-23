import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")

    if not SECRET_KEY:
        raise RuntimeError("SECRET_KEY environment variable is required")

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///notes.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
