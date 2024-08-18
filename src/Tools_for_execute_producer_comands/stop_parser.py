from src.databases.mongodb import client_mongodb


def stop_parser():
    parser_process = client_mongodb.get_entry(client_mongodb.collection_for_parser_configs, 'uniq_key', client_mongodb.uniq_key)['parser_process']
    if parser_process is None:
        return 'ОК: Парсер не работает'
    else:
        parser_process.kill()
