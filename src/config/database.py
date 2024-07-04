from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from ..models import Model
from os import environ

DB_NAME = environ["DB_NAME"]
DB_USER = environ["DB_USER"]
DB_PASSWORD = environ["DB_PASSWORD"]
DB_HOST = environ["DB_HOST"]
DB_PORT = environ["DB_PORT"]

engine = create_async_engine(
    f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/"
)
new_session = async_sessionmaker(engine, expire_on_commit=False)

async def create_tables():
    async with engine.begin() as conn:
       await conn.run_sync(Model.metadata.create_all)

async def drop_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)