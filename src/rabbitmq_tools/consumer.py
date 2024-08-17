import pika
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties
from typing import Any
from src.databases.mongodb import client_mongodb


class Consumer:
    def __init__(self, host):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        self.channel = self.connection.channel()

        self.queue = 'parser'
        self.queue_callback = 'parser_callback'
        self.exchange = ''

        self.declare_queue()

        self.consume()

    def declare_queue(self):
        self.channel.queue_declare(queue=self.queue, durable=True)
        self.channel.queue_declare(queue=self.queue_callback, durable=True)

    def callback(self, channel: BlockingChannel, method: Basic.Deliver, properties: BasicProperties, body: Any):
        self.confirm_the_request(channel, method, properties, body)

    def consume(self):
        self.channel.basic_consume(queue=self.queue, on_message_callback=self.callback)
        self.channel.start_consuming()

    def confirm_the_request(self, channel: BlockingChannel, method: Basic.Deliver, properties: BasicProperties, body: bytes):
        status_of_parser: str = client_mongodb.get_status_of_parser()
        channel.basic_publish(
            exchange=self.exchange,
            routing_key=properties.reply_to,
            body=status_of_parser.encode(),
        )
        channel.basic_ack(delivery_tag=method.delivery_tag)

    def publish(self, body: bytes):
        self.channel.basic_publish(self.exchange, routing_key=self.queue_callback, body=body)


consumer = Consumer('localhost')
