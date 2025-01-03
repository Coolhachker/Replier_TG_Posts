import pika
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties
from typing import Any
from src.databases.mongodb import client_mongodb
from src.Tools_for_execute_producer_comands.executer import execute_producer_commands
from src.rabbitmq_tools.queue_dataclass import Queue
import json
from src.tools_for_tg_bot.Configs.hosts import Hosts
import logging
from logging import basicConfig
basicConfig(filename='data/replier.log', filemode='w', level=logging.DEBUG, format='[%(levelname)s] - %(funcName)s - %(message)s')
logger = logging.getLogger()


class Consumer:
    def __init__(self, host):
        self.parameters = pika.ConnectionParameters(heartbeat=60, host=host)
        self.connection = pika.BlockingConnection(self.parameters)
        self.channel = self.connection.channel()

        self.queue = Queue.parser_queue
        self.queue_callback = Queue.callback_queue
        self.parser_tasks_queue = Queue.parser_task_queue
        self.ping_queue = Queue.ping_queue
        self.exchange = ''

        self.declare_queue()

        self.consume()
        self.channel.start_consuming()

    def declare_queue(self):
        self.channel.queue_declare(queue=self.queue, durable=True)
        self.channel.queue_declare(queue=self.queue_callback, durable=True)
        self.channel.queue_declare(queue=self.parser_tasks_queue, durable=True)
        self.channel.queue_declare(queue=self.ping_queue, durable=True)

    def callback(self, channel: BlockingChannel, method: Basic.Deliver, properties: BasicProperties, body: Any):
        self.confirm_the_request(channel, method, properties, body)

    def consume(self):
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=self.queue, on_message_callback=self.callback)
        self.channel.basic_consume(queue=self.parser_tasks_queue, on_message_callback=self.callback_on_task_commands)
        self.channel.basic_consume(queue=self.ping_queue, on_message_callback=self.callback_on_ping_request)
        self.channel.start_consuming()

    def confirm_the_request(self, channel: BlockingChannel, method: Basic.Deliver, properties: BasicProperties, body: bytes):
        result = execute_producer_commands(body.decode())
        logger.info(f'Получил сообщение: {body.decode()}')
        status_of_parser: str = client_mongodb.get_status_of_parser()
        channel.basic_publish(
            exchange=self.exchange,
            routing_key=properties.reply_to,
            body=status_of_parser.encode() if result is None else result.encode(),
        )
        channel.basic_ack(delivery_tag=method.delivery_tag)

    def callback_on_task_commands(self, channel: BlockingChannel, method: Basic.Deliver, properties: BasicProperties, body: Any):
        data = json.loads(body.decode())
        logger.info(f'Получил сообщение: {data}')
        result = execute_producer_commands(command=data['command'], dict_of_data=data)
        logger.info(f'Результат работы: {result}')
        channel.basic_publish(
            exchange=self.exchange,
            routing_key=properties.reply_to,
            body=result.encode() if result is not None else ''.encode()
        )
        channel.basic_ack(delivery_tag=method.delivery_tag)

    def callback_on_ping_request(self, channel: BlockingChannel, method: Basic.Deliver, properties: BasicProperties, body: Any):
        channel.basic_publish(
            exchange=self.exchange,
            routing_key=properties.reply_to,
            body='pong'.encode()
        )
        channel.basic_ack(delivery_tag=method.delivery_tag)

    def publish(self, body: bytes):
        self.channel.basic_publish(self.exchange, routing_key=self.queue_callback, body=body)

    def reconnect(self):
        self.connection = pika.BlockingConnection(self.parameters)
        self.channel = self.connection.channel()


consumer = Consumer(Hosts.rabbitmq)
