import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGODB_URI = os.getenv(
    "MONGODB_URI",
    "mongodb://localhost:27017/"
)

DATABASE_NAME = os.getenv(
    "MONGODB_DATABASE",
    "digital_library"
)

client = MongoClient(
    MONGODB_URI,
    serverSelectionTimeoutMS=5000
)


def get_database():
    """Return the digital library database."""
    return client[DATABASE_NAME]


def test_connection():
    """Check whether MongoDB is reachable."""
    try:
        client.admin.command("ping")
        print("MongoDB connection successful!")

        db = get_database()
        print(f"Database selected: {db.name}")

        return True

    except Exception as error:
        print(f"MongoDB connection failed: {error}")
        return False