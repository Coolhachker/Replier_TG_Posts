import pika
from typing import Any, Optional, Union
import re
from src.exceptions.castom_exceptions import Exceptions
from src.rabbitmq_tools.queue_dataclass import Queue


class Producer:
    def __init__(self, host):
        parameters = pika.ConnectionParameters(heartbeat=120, host=host)

        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

        self.exchange = ''
        self.queue = 'parser'
        self.callback_queue = 'parser_callback'
        self.parser_tasks_queue = Queue.parser_task_queue

        self.declare_queue()
        self.consume_the_response()

        self.response: Optional[str] = None
        self.info_response: Union[str, None] = None

    def declare_queue(self):
        self.channel.queue_declare(queue=self.queue, durable=True)
        self.channel.queue_declare(queue='parser_callback', durable=True)
        self.channel.queue_declare(queue=self.parser_tasks_queue, durable=True)

    def publish(self, message: Any, properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent), queue=None):
        self.channel.basic_publish(
            exchange=self.exchange,
            routing_key=self.queue if queue is None else queue,
            body=message.encode(),
            properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent, reply_to=self.callback_queue)
        )

        while self.response is None:
            self.connection.process_data_events(time_limit=180)
        else:
            response = self.response
            self.response = None
            return response

    def close_connection(self):
        self.channel.close()

    def consume_the_response(self):
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True
        )

    def on_response(self, channel, method, properties, body: bytes):
        if re.search(r'INFO', body.decode()):
            self.info_response = body.decode()
        elif re.search(r'ERROR', body.decode()):
            raise Exceptions.UnSuccessfulResponseRMQ(f'Ошибка: {body.decode()}')
        else:
            self.response = body.decode()


producer = Producer('localhost')

