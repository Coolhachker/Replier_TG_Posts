from dataclasses import dataclass


@dataclass
class Queue:
    parser_queue: str = 'parser'
    callback_queue: str = 'parser_callback'
    parser_task_queue: str = 'parser_task_queue'
    ping_queue: str = 'ping_queue'