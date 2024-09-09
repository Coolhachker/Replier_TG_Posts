from dataclasses import dataclass


@dataclass
class Commands:
    TURN_ON_COMMAND: str = 'TURN_ON'     # команда включает парсер
    TURN_OFF_COMMAND: str = 'TURN_OFF'   # команда выключает парсер
    ADD_OR_DELETE_CHANNELS_COMMAND: str = 'ADD_OR_DELETE_CHANNELS'   #команда добавляет или удаляет каналы в конфиг коллекции
    CHANGE_SETTINGS_COMMAND: str = "CHANGE_SETTINGS"     # команда изменяет настройки в конфиг коллекции
    CHECK_PARSER_COMMAND: str = 'CHECK_PARSER'
    GET_CHANNELS_COMMAND: str = 'GET_CHANNELS'