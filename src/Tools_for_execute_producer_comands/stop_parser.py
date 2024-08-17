from src.Tools_for_replie_mesages.entry_point import main
from src.Tools_for_replie_mesages.entry_point import main_task
import asyncio


def stop_parser():
    if main_task.done() is True:
        return 'ОК: Парсер не работает'
    else:
        main_task.cancel()
