import typing
from functools import lru_cache
from mysql.connector import connect
import mysql
import logging
from src.tools_for_tg_bot.Configs.hosts import Hosts
logger = logging.getLogger()


class MysqlDB:
    def __init__(self):
        self.connection, self.cursor = self.connect_to_db()
        self.create_table()

    def connect_to_db(self):
        try:
            connection = connect(
                host=Hosts.mysql_db,
                user='root',
                password='root1234567890',
                auth_plugin='mysql_native_password',
                database='PARSER_REPLIES_USERS'
            )
            logger.info('Успешное подключение')
            return connection, connection.cursor(buffered=True)
        except mysql.connector.errors.ProgrammingError:
            connection = connect(
                host=Hosts.mysql_db,
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

    def add_entry_in_trusted_users(self, user_nickname: str):
        self.cursor.executemany("""INSERT INTO trusted_users(user_nickname, chat_id) VALUES(%s, %s)""", [(user_nickname, None)])
        self.connection.commit()

    def get_chat_id_of_trusted_users(self) -> typing.List[str]:
        self.cursor.execute('SELECT chat_id FROM trusted_users')
        trusted_users = [user[0] for user in client_mysqldb.cursor.fetchall()]
        return trusted_users

    def get_nicknames_of_trusted_user(self):
        self.cursor.execute(f'SELECT user_nickname FROM trusted_users')
        nickname = [user[0] for user in client_mysqldb.cursor.fetchall()]
        return nickname

    @lru_cache(maxsize=128)
    def add_chat_id_in_trusted_users(self, nickname: str, chat_id) -> None:
        self.cursor.executemany("""UPDATE trusted_users SET chat_id = %s WHERE user_nickname = %s""", [(chat_id, nickname)])
        self.connection.commit()
        return None

    def delete_admin_from_db(self, user_nickname: str):
        self.cursor.execute(f"""DELETE FROM trusted_users WHERE user_nickname = '{user_nickname}' """)
        self.connection.commit()


client_mysqldb = MysqlDB()


