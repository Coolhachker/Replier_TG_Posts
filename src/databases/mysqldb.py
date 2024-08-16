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
        self.cursor.execute('CREATE TABLE IF NOT EXISTS trusted_users(user_nickname TEXT)')
        self.cursor.execute('SELECT * FROM trusted_users')
        if len(self.cursor.fetchall()) == 0:
            self.cursor.executemany("""INSERT INTO trusted_users(user_nickname) VALUES(%s)""", [('CHT_VENDETTA', )])


client_mysqldb = MysqlDB()


