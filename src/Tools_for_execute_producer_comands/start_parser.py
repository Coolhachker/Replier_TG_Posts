from src.databases.mongodb import client_mongodb
import subprocess


def start_parser():
    parser_process = client_mongodb.get_entry(client_mongodb.collection_for_parser_configs, 'uniq_key', client_mongodb.uniq_key)['parser_process']
    if parser_process is None:
        client_mongodb.update_process_parser(subprocess.Popen['python3', '../Tools_for_replie_mesages/entry_point.py'])
    else:
        return 'OK: Парсер уже работает'