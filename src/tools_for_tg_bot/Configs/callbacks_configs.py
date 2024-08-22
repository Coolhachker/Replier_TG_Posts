from dataclasses import dataclass


@dataclass
class CallbacksNames:
    start_parser: str = 'start_parser'
    stop_parser: str = 'stop_parser'
    check_parser: str = 'check_parser'
    add_or_delete_channels: str = 'add_or_delete_channels'
    change_parameters: str = 'change_parameters'
    add_channel: str = 'add_channel'
    delete_channel: str = 'delete_channel'