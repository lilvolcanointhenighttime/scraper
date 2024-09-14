from fastapi import APIRouter, Depends
from starlette.responses import RedirectResponse, Response

from .config.env import GITHUB_CLINET_ID, GITHUB_CLINET_SECRET
from .utils import async_query_post, async_query_get
from .jwt import create_access_token
from .repository import UserRepository
from .models import UserOrm
from .utils import get_current_user


cookie_router = APIRouter(prefix="/cookie", tags=["Cookie"])
github_router = APIRouter(prefix="/github-oauth", tags=["Github-OAuth"])

@cookie_router.get("/create")
async def create_cookie(id: int):
    access_token = create_access_token({"sub": str(id)})
    response = RedirectResponse(url="http://localhost/pages/login.html")
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return response

@cookie_router.post("/me/")
async def get_me(user_data: UserOrm = Depends(get_current_user)):
    return user_data

@cookie_router.post("/logout/")
async def logout_user(response: Response):
    response.delete_cookie(key="users_access_token")
    return {'message': 'Пользователь успешно вышел из системы'}


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
    print(response)
    access_token = response ["access_token"]
    headers.update({"Authorization": f"Bearer {access_token}"})

    response = await async_query_get(session=aiohttp_clientsession, headers=headers, url="https://api.github.com/user", params="")
    user = {
        "id": response["id"],
        "login": response["login"],
        "avatar_url": response["avatar_url"]
    }

    if await UserRepository.filter(params=user):
        pass
    else:
        await UserRepository.add(user)
    return RedirectResponse(f"http://localhost/api/oauth/cookie/create?id={user["id"]}")

