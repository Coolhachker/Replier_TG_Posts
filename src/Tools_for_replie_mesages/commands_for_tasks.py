from dataclasses import dataclass


@dataclass
class CommandsForTask:
    start_task: str = 'start_task'
    stop_task: str = 'stop_task'
