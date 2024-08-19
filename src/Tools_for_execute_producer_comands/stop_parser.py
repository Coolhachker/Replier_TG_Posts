from src.databases.mongodb import client_mongodb
import subprocess


def stop_parser():
    parser_process = client_mongodb.get_entry(client_mongodb.collection_for_parser_configs, 'uniq_key', client_mongodb.uniq_key)['pid_of_parser']
    if parser_process is None:
        return 'ОК: Парсер не работает'
    else:
        subprocess.run(['kill', parser_process])
