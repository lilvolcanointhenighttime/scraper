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

RMQ_HOST = environ["RMQ_HOST"]
RMQ_PORT = environ["RMQ_PORT"]

RMQ_USER = environ["RMQ_USER"]
RMQ_PASSWORD = environ["RMQ_PASSWORD"]

MQ_EXCHANGE = environ["MQ_EXCHANGE"]
MQ_ROUTING_KEY_SCRAPER = environ["MQ_ROUTING_KEY_SCRAPER"]
MQ_ROUTING_KEY_OAUTH = environ["MQ_ROUTING_KEY_OAUTH"]