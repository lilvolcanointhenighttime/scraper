from dotenv import load_dotenv
from os import environ

load_dotenv()

DB_NAME = environ["DB_NAME"]
DB_USER = environ["DB_USER"]
DB_PASSWORD = environ["DB_PASSWORD"]
DB_HOST = environ["DB_HOST"]
DB_PORT = environ["DB_PORT"]
DB_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/"