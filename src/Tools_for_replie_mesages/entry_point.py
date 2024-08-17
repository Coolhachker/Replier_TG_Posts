from src.Tools_for_replie_mesages.replie_engine import ReplierEngine
from src.databases.mongodb import client_mongodb
import asyncio

replier_engine = ReplierEngine(19567654, 'gkadnfnsdkbd')
main_task = asyncio.create_task(replier_engine.central_processing_of_register_tasks())


def main():
    try:
        replier_engine.client_session.start()
        client_mongodb.add_data_in_entry(client_mongodb.collection_for_parser_configs, 'status_check', 'OK: Парсер работает', 'uniq_key', client_mongodb.uniq_key)
        asyncio.get_event_loop().run_until_complete(main_task)
    finally:
        client_mongodb.add_data_in_entry(client_mongodb.collection_for_parser_configs, 'status_check', 'OK: Парсер не работает', 'uniq_key', client_mongodb.uniq_key)