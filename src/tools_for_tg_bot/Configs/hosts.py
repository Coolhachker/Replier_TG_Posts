from dataclasses import dataclass


@dataclass
class Hosts:
    mongodb: str = '172.16.235.3'
    mysql_db: str = '172.16.235.2'
    rabbitmq: str = '172.16.235.7'
