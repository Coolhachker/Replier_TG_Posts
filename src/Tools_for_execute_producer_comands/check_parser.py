from src.databases.mongodb import client_mongodb


def check_parser():
    status_of_parser = client_mongodb.get_status_of_parser()
    return status_of_parser if status_of_parser != '' else 'OK: Парсер не работает'