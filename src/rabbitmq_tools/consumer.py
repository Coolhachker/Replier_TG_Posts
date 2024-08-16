import pika
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties
from typing import Any


class Consumer:
    def __init__(self, host):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        self.channel = self.connection.channel()

        self.queue = 'parser'
        self.exchange = ''

        self.declare_queue()

        self.consume()

    def declare_queue(self):
        self.channel.queue_declare(queue=self.queue, durable=True)

    def callback(self, channel: BlockingChannel, method: Basic.Deliver, properties: BasicProperties, body: Any):
        print(type(method))
        print(type(properties))
        print(type(body))
        print(body)
        channel.basic_ack(delivery_tag=method.delivery_tag)

    def consume(self):
        self.channel.basic_consume(queue=self.queue, on_message_callback=self.callback)
        self.channel.start_consuming()


consumer = Consumer('localhost')
