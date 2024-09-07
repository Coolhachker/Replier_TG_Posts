import asyncio
from src.Tools_for_replie_mesages.replie_engine import replier_engine
from src.databases.mongodb import client_mongodb
import logging
from logging import basicConfig
from src.rabbitmq_tools.producer_commands import Commands

basicConfig(filename='data/replier.log', filemode='w', level=logging.DEBUG, format='[%(levelname)s] - %(funcName)s - %(message)s')
logger = logging.getLogger()


def main():
    try:
        logger.info('START ENTRY_POINT')
        replier_engine.client_session.start()
        event_loop = asyncio.get_event_loop()
        client_mongodb.update_status_of_parser('OK: Парсер работает')
        client_mongodb.set_command_entry()
        client_mongodb.set_command_in_parser_commands(Commands.TURN_ON_COMMAND)

        logger.info('Парсер работает')

        event_loop.run_until_complete(replier_engine.parser_conductor())
    finally:
        logger.info('Парсер перестал работать')
        client_mongodb.update_pid_of_parser(None)
        client_mongodb.update_status_of_parser('OK: Парсер не работает :(')


if __name__ == '__main__':
    main()