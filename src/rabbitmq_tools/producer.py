import pika
from typing import Any


class Producer:
    def __init__(self, host):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        self.channel = self.connection.channel()

        self.exchange = ''
        self.queue = 'parser'

        self.declare_queue()

    def declare_queue(self):
        self.channel.queue_declare(queue=self.queue, durable=True)

    def publish(self, message: Any, properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent)):
        self.channel.basic_publish(
            exchange=self.exchange,
            routing_key=self.queue,
            body=message.encode(),
            properties=properties
        )

    def close_connection(self):
        self.channel.close()


producer = Producer('localhost')
producer.publish('message')

