from fastapi import APIRouter
from starlette.responses import RedirectResponse

from .config.env import GITHUB_CLINET_ID, GITHUB_CLINET_SECRET
from .utils import async_query_post, async_query_get

github_router = APIRouter(prefix="/github-oauth", tags=["Auth"])

@github_router.get("/login")
async def github_login():
    return RedirectResponse(f"https://github.com/login/oauth/authorize?client_id={GITHUB_CLINET_ID}", status_code=302)

@github_router.get("/code")
async def github_code(code: str):
    from .app import aiohttp_clientsession

    params = {
        "client_id": GITHUB_CLINET_ID,
        "client_secret": GITHUB_CLINET_SECRET,
        "code": code
    }

    headers = {
        "Accept": "application/json"
    }

    response = await async_query_post(session=aiohttp_clientsession, headers=headers,url="https://github.com/login/oauth/access_token", params=params)

    access_token = response ["access_token"]
    headers.update({"Authorization": f"Bearer {access_token}"})

    response = await async_query_get(session=aiohttp_clientsession, headers=headers, url="https://api.github.com/user", params="")
    return response