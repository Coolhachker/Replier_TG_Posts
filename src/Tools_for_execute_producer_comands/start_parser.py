import time
from src.databases.mongodb import client_mongodb
import subprocess


def start_parser():
    parser_process = client_mongodb.get_entry(client_mongodb.collection_for_parser_configs, 'uniq_key', client_mongodb.uniq_key)['pid_of_parser']
    if parser_process is None:
        process = subprocess.run(['python3', '../Tools_for_replie_mesages/entry_point.py'])
        time.sleep(5)
    else:
        return 'OK: Парсер уже работает'