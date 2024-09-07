import pika
from pika import exceptions
from src.tools_for_tg_bot.Configs.hosts import Hosts


class Publisher:
    def __init__(self, host):
        self.parameters = pika.ConnectionParameters(heartbeat=60, host=host)
        self.connection = pika.BlockingConnection(self.parameters)
        self.channel = self.connection.channel()

        self.exchange = ''

    def publish(self, message: bytes, queue: str):
        try:
            self.channel.basic_publish(self.exchange, routing_key=queue, body=message)
        except (exceptions.StreamLostError, exceptions.ChannelWrongStateError):
            self.connection = pika.BlockingConnection(self.parameters)
            self.channel = self.connection.channel()
            self.publish(message, queue)


publisher = Publisher(Hosts.rabbitmq)