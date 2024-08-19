from src.Tools_for_replie_mesages.replie_engine import ReplierEngine
from src.databases.mongodb import client_mongodb
import asyncio
import os
import logging
from logging import basicConfig
basicConfig(filename='../../data/replier.log', filemode='w', level=logging.DEBUG, format='[%(levelname)s] - %(funcName)s - %(message)s')
logger = logging.getLogger()


def main():
    try:
        logger.info('START ENTRY_POINT')
        replier_engine = ReplierEngine(19567654, 'gkadnfnsdkbd')
        client_mongodb.update_status_of_parser('OK: Парсер работает')
        logger.info('Парсер работает')
        asyncio.get_event_loop().run_until_complete(replier_engine.central_processing_of_register_tasks())
    finally:
        logger.info('Парсер перестал работать')
        client_mongodb.update_pid_of_parser(None)
        client_mongodb.update_status_of_parser('OK: Парсер не работает :(')


if __name__ == '__main__':
    main()