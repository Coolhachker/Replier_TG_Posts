from src.Tools_for_replie_mesages.commands_for_tasks import CommandsForTask
from src.rabbitmq_tools.producer import producer
import json


def start_channel(channel: str):
    data_for_send = {'command': CommandsForTask.start_task, 'channel': channel}
    result = producer.publish(json.dumps(data_for_send), queue=producer.parser_tasks_queue)
    return result
