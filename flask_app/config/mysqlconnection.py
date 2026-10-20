import pymysql.cursors
import os
from dotenv import load_dotenv

load_dotenv()

class MySQLConnection:

    def __init__(self, db):
        self.connection = pymysql.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=db,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )

    def query_db(self, query, data=None):
        with self.connection.cursor() as cursor:
            cursor.execute(query, data or ())

            if query.strip().upper().startswith('SELECT'):
                return cursor.fetchall()

            if query.strip().upper().startswith('INSERT'):
                return cursor.lastrowid

            return cursor.rowcount > 0

    def close(self):
        self.connection.close()

def connectToMySQL(db):
    return MySQLConnection(db)
