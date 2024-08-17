import pika
from typing import Any, Optional
import re
from src.exceptions.castom_exceptions import Exceptions


class Producer:
    def __init__(self, host):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        self.channel = self.connection.channel()

        self.exchange = ''
        self.queue = 'parser'
        self.callback_queue = 'parser_callback'

        self.declare_queue()
        self.consume_the_response()

        self.response: Optional[str] = None

    def declare_queue(self):
        self.channel.queue_declare(queue=self.queue, durable=True)
        self.channel.queue_declare(queue='parser_callback', durable=True)

    def publish(self, message: Any, properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent)):
        self.channel.basic_publish(
            exchange=self.exchange,
            routing_key=self.queue,
            body=message.encode(),
            properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent, reply_to=self.callback_queue)
        )

        while self.response is None:
            self.connection.process_data_events(time_limit=180)

        response = self.response
        self.response = None
        return response

    def close_connection(self):
        self.channel.close()

    def consume_the_response(self):
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True
        )

    def on_response(self, channel, method, properties, body: bytes):
        if re.search(r'INFO', body.decode()):
            pass
        elif re.search(r'ERROR', body.decode()):
            raise Exceptions.UnSuccessfulResponseRMQ(f'Ошибка: {body.decode()}')
        else:
            self.response = body.decode()


producer = Producer('localhost')

