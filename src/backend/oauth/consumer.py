import aiohttp
import json
from typing import TYPE_CHECKING

# from os import path
# import sys
# sys.path.append(path.abspath(path.join(path.dirname(__file__), "..")))
from .config.rmq_config import get_connection
from .config.env import MQ_ROUTING_KEY_OAUTH, DOMAIN_NGINX, USE_K8S

from .utils import async_query_post, sync
from .producer import produce_message

if TYPE_CHECKING:
    from pika.adapters.blocking_connection import BlockingChannel
    from pika.spec import Basic, BasicProperties


@sync
async def process_new_message(
    ch: "BlockingChannel",
    method: "Basic.Deliver",
    properties: "BasicProperties",
    body: bytes,
) -> None:
    data = json.loads(body)

    aiohttp_clientsession = aiohttp.ClientSession()

    if properties.content_type == "user_info":
        params = {
            "token": data
        }
        if USE_K8S:
            current_user = await async_query_post(session=aiohttp_clientsession, url=f"http://fastapi-oauth:8800/api/oauth/cookie/rmq-me", params=params)
        else:
            current_user = await async_query_post(session=aiohttp_clientsession, url=f"http://{DOMAIN_NGINX}/api/oauth/cookie/rmq-me", params=params)
        produce_message(channel=ch, method="user_info", body=json.dumps(current_user))

    ch.basic_ack(delivery_tag=method.delivery_tag)


def consume_messages(channel: "BlockingChannel") -> None:
    channel.basic_consume(
        queue=MQ_ROUTING_KEY_OAUTH,
        on_message_callback=process_new_message,
        auto_ack=True,
    )
    channel.start_consuming()


def main():
    with get_connection() as connection:
        with connection.channel() as channel:
            channel.queue_declare(queue=MQ_ROUTING_KEY_OAUTH)
            consume_messages(channel=channel)


if __name__ == "__main__":
    main()