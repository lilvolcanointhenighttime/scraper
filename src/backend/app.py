from contextlib import asynccontextmanager
from fastapi import FastAPI
import aiohttp
from .routers import hh_router
from .config.database import create_tables, drop_tables
from fastapi.middleware.cors import CORSMiddleware



aiohttp_clientsession: aiohttp.ClientSession = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global aiohttp_clientsession
    aiohttp_clientsession = aiohttp.ClientSession()
    await create_tables()
    yield
    await aiohttp_clientsession.close()
    # await drop_tables()



app = FastAPI(title="Scraping", lifespan=lifespan, root_path="/api")

origins = ["*"]

app.add_middleware(
    CORSMiddleware, 
    allow_origins=['null'],
    allow_credentials=True, 
    allow_methods=['*'], 
    allow_headers=['*'])


app.include_router(hh_router)




