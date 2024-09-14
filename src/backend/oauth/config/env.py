from dotenv import load_dotenv
from os import environ

load_dotenv()
DB_USER = environ["POSTGRES_USER"]
DB_PASSWORD = environ["POSTGRES_PASSWORD"]
DB_HOST = environ["POSTGRES_HOST"]
DB_PORT = environ["POSTGRES_PORT"]
DB_NAME = environ["POSTGRES_DB"]
DB_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

SECRET_KEY = environ["SECRET_KEY"]
ALGORITHM = environ["ALGORITHM"]

GITHUB_CLINET_ID = environ["GITHUB_CLINET_ID"]
GITHUB_CLINET_SECRET = environ["GITHUB_CLINET_SECRET"]