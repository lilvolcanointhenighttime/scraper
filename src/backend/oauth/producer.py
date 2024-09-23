import pika
from typing import TYPE_CHECKING

# from os import path
# import sys
# sys.path.append(path.abspath(path.join(path.dirname(__file__), "..")))
from .config.rmq_config import get_connection
from .config.env import MQ_EXCHANGE, MQ_ROUTING_KEY_SCRAPER

if TYPE_CHECKING:
    from pika.adapters.blocking_connection import BlockingChannel



def produce_message(channel: "BlockingChannel", method, body) -> None:
    properties = pika.BasicProperties(method)
    channel.basic_publish(
        exchange=MQ_EXCHANGE,
        routing_key=MQ_ROUTING_KEY_SCRAPER,
        properties=properties,
        body=body,
    )

def main():
    with get_connection() as connection:
        with connection.channel() as channel:
            produce_message(channel=channel)


if __name__ == "__main__":
    main()