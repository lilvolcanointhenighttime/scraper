from contextlib import asynccontextmanager
from fastapi import FastAPI
import aiohttp
from .routers import github_router, cookie_router
from .config.database import create_tables, drop_tables
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
# from starlette.middleware.cors import CORSMiddleware


aiohttp_clientsession: aiohttp.ClientSession = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global aiohttp_clientsession
    aiohttp_clientsession = aiohttp.ClientSession()
    await create_tables()
    yield
    await aiohttp_clientsession.close()
    # await drop_tables()



app = FastAPI(title="OAuth", lifespan=lifespan, root_path="/api/oauth")

origins = ["https://github.com",
           "https://github.com/",
           "http://localhost:80",
           "http://localhost:80/",
           "http://localhost",
           "http://localhost/",
           ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Access-Control-Allow-Origin", "Access-Control-Allow-Credentials", "Access-Control-Allow-Headers"],
)
# app.add_middleware(HTTPSRedirectMiddleware)


app.include_router(github_router)
app.include_router(cookie_router)




