import aiohttp

from jose import jwt, JWTError
from datetime import datetime, timezone

from fastapi import HTTPException, status, Depends

from .config.env import SECRET_KEY, ALGORITHM
from .jwt import get_token, get_auth_data
from .repository import UserRepository


async def async_query_post(session: aiohttp.ClientSession, url: str, headers: dict = {}, params: dict = {}) -> dict:
    async with session.post(headers=headers, url=url, params=params) as response:
        data = await response.json()
        return data
    
async def async_query_get(session: aiohttp.ClientSession, url: str, headers: dict = {}, params: dict = {}) -> dict:
    async with session.get(headers=headers, url=url, params=params) as response:
        data = await response.json()
        return data

async def get_current_user(token: str = Depends(get_token)):
    try:
        auth_data = get_auth_data()
        payload = jwt.decode(token, auth_data['secret_key'], algorithms=[auth_data['algorithm']])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен не валидный!')

    expire = payload.get('exp')
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен истек')

    user_id = payload.get('sub')
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Не найден ID пользователя')
    user_id = {"id": int(user_id)}

    user = await UserRepository.filter(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')

    return user