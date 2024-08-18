from src.Tools_for_replie_mesages.replie_engine import ReplierEngine
from src.databases.mongodb import client_mongodb
import asyncio


def main():
    try:
        replier_engine = ReplierEngine(19567654, 'gkadnfnsdkbd')
        client_mongodb.add_data_in_entry(client_mongodb.collection_for_parser_configs, 'status_check', 'OK: Парсер работает', 'uniq_key', client_mongodb.uniq_key)
        asyncio.get_event_loop().run_until_complete(replier_engine.central_processing_of_register_tasks())
    finally:
        client_mongodb.update_process_parser(None)
        client_mongodb.add_data_in_entry(client_mongodb.collection_for_parser_configs, 'status_check', 'OK: Парсер не работает', 'uniq_key', client_mongodb.uniq_key)