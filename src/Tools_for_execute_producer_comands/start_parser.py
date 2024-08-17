import re
from src.databases.mongodb import client_mongodb
from src.Tools_for_replie_mesages.entry_point import main
from src.Tools_for_replie_mesages.entry_point import main_task


def start_parser():
    if main_task.done() is True:
        main()
    else:
        return 'OK: Парсер уже работает'