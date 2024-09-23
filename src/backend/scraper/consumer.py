import json
from typing import TYPE_CHECKING

# from os import path
# import sys
# sys.path.append(path.abspath(path.join(path.dirname(__file__), "..")))
from .config.env import MQ_ROUTING_KEY_SCRAPER
from .config.rmq_config import get_connection

from .utils import sync
from .repository import UserRepository

if TYPE_CHECKING:
    from pika.adapters.blocking_connection import BlockingChannel
    from pika.spec import Basic, BasicProperties


@sync
async def process_new_message(
    ch: "BlockingChannel",
    method: "Basic.Deliver",
    properties: "BasicProperties",
    body: bytes,
):
    data = json.loads(body.decode('utf-8'))

    if properties.content_type == "user_info":
        data = data[0]
        user = await UserRepository.add(data)

    ch.basic_ack(delivery_tag=method.delivery_tag)


def consume_messages(channel: "BlockingChannel") -> None:
    channel.basic_consume(
        queue=MQ_ROUTING_KEY_SCRAPER,
        on_message_callback=process_new_message,
        auto_ack=True,
    )
    channel.start_consuming()


def main():
    with get_connection() as connection:
        with connection.channel() as channel:
            channel.queue_declare(queue=MQ_ROUTING_KEY_SCRAPER)
            consume_messages(channel=channel)


if __name__ == "__main__":
    main()