from dataclasses import dataclass


@dataclass
class Queue:
    parser_queue: str = 'parser'
    callback_queue: str = 'parser_callback'