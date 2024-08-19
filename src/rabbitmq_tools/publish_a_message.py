import pika


class Publisher:
    def __init__(self, host):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        self.channel = self.connection.channel()

        self.exchange = ''

    def publish(self, message: bytes, queue: str):
        self.channel.basic_publish(self.exchange, routing_key=queue, body=message)


publisher = Publisher('localhost')