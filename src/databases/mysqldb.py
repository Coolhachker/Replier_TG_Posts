import typing
from functools import lru_cache
from mysql.connector import connect
import mysql
import logging
logger = logging.getLogger()


class MysqlDB:
    def __init__(self):
        self.connection, self.cursor = self.connect_to_db()
        self.create_table()

    def connect_to_db(self):
        try:
            connection = connect(
                host='localhost',
                user='root',
                password='root1234567890',
                auth_plugin='mysql_native_password',
                database='PARSER_REPLIES_USERS'
            )
            logger.info('Успешное подключение')
            return connection, connection.cursor(buffered=True)
        except mysql.connector.errors.ProgrammingError:
            connection = connect(
                host='localhost',
                user='root',
                password='root1234567890',
                auth_plugin='mysql_native_password',
            )
            cursor = connection.cursor()
            cursor.execute('CREATE DATABASE PARSER_REPLIES_USERS')
            connection.commit()
            self.connect_to_db()

    def create_table(self):
        # self.cursor.execute('DROP TABLE trusted_users')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS trusted_users(user_nickname TEXT, chat_id INT UNSIGNED)')
        self.cursor.execute('SELECT * FROM trusted_users')
        if len(self.cursor.fetchall()) == 0:
            self.cursor.executemany("""INSERT INTO trusted_users(user_nickname, chat_id) VALUES(%s, %s)""", [('CHT_VENDETTA', None)])
        self.connection.commit()

    def get_chat_id_of_trusted_users(self) -> typing.List[str]:
        self.cursor.execute('SELECT user_nickname FROM trusted_users')
        print(client_mysqldb.cursor.fetchall())
        breakpoint()
        trusted_users = [user[1] for user in client_mysqldb.cursor.fetchall()]
        return trusted_users

    @lru_cache(maxsize=128)
    def add_chat_id_in_trusted_users(self, nickname: str, chat_id) -> None:
        self.cursor.executemany("""UPDATE trusted_users SET chat_id = %s WHERE user_nickname = %s""", [(chat_id, nickname)])
        self.connection.commit()
        return None


client_mysqldb = MysqlDB()


