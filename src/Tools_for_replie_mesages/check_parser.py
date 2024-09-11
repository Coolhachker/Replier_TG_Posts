from src.databases.mongodb import client_mongodb
import asyncio
import re


def command_check_parser():
    channels_to_post_the_posts = client_mongodb.get_channels_url('to')
    string_for_send_to_user: str = ''
    running_tasks = [task.get_name() for task in asyncio.all_tasks()]
    for channel in channels_to_post_the_posts:
        string_for_send_to_user += channel + ' ' + '->' + ' '
        for task in running_tasks:
            if re.search(channel, task):
                string_for_send_to_user += '✅︎ Работает\n'
                break
        else:
            string_for_send_to_user += '❌️ Не работает\n'
    return string_for_send_to_user
