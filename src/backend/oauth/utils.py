import aiohttp
# import pika
# import json
import functools
import asyncio

from jose import jwt, JWTError
from datetime import datetime, timezone

from fastapi import HTTPException, status, Depends

# from .config.rmq_config import get_connection
# from .config.env import MQ_EXCHANGE, MQ_ROUTING_KEY
from .jwt import get_token, get_auth_data
from .repository import UserRepository


def sync(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.get_event_loop().run_until_complete(f(*args, **kwargs))
    return wrapper

async def async_query_post(session: aiohttp.ClientSession, url: str, headers: dict = {}, params: dict = {}) -> dict:
    async with session.post(headers=headers, url=url, params=params) as response:
        data = await response.json()
        return data
    
async def async_query_get(session: aiohttp.ClientSession, url: str, headers: dict = {}, params: dict = {}) -> dict:
    async with session.get(headers=headers, url=url, params=params) as response:
        data = await response.json()
        return data

async def get_current_user(token: str = Depends(get_token)) -> dict:
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


# def publish_rmq(data: dict) -> None:
    
#     with get_connection() as connection:
#         with connection.channel() as channel:

#             exchange_name = MQ_EXCHANGE
#             routing_key = MQ_ROUTING_KEY

#             # This will create the exchange if it doesn't already exist.
#             channel.exchange_declare(exchange=exchange_name, exchange_type='topic', durable=True)
#             channel.basic_publish(exchange=exchange_name,
#                                 routing_key=routing_key,
#                                 body=json.dumps(data),
#                                 # Delivery mode 2 makes the broker save the message to disk.
#                                 # This will ensure that the message be restored on reboot even  
#                                 # if RabbitMQ crashes before having forwarded the message.
#                                 properties=pika.BasicProperties(
#                                     delivery_mode = 2,
#                                 ))
            
