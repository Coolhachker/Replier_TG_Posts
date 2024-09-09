from src.databases.mongodb import client_mongodb
# import subprocess
import os


def stop_parser():
    parser_process = client_mongodb.get_entry(client_mongodb.collection_for_parser_configs, 'uniq_key', client_mongodb.uniq_key)['pid_of_parser']
    if parser_process is None:
        return 'ОК: Парсер не работает'
    else:
        client_mongodb.update_pid_of_parser(None)
        client_mongodb.update_status_of_parser('OK: Парсер не работает :(')
        os.system(f'kill {parser_process}')
        # subprocess.run(['pkill', str(parser_process)])
