import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    return psycopg2.connect(
        host = os.getenv("DB_HOST"),
        database = os.getenv("DB_NAME"),
        port = os.getenv("DB_PORT"),
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASSWORD")
    )