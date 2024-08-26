import asyncio
from src.exceptions.castom_exceptions import Exceptions
import re


async def check_on_tasks():
    if len([task for task in asyncio.all_tasks() if re.search('Task', task.get_name()) is False]) == 0:
        raise Exceptions.NoTasks('тасков нет')