import mysql.connector


class DataBase:

    def __init__(self, host, user, password, database, charset, collation):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            charset=charset,
            collation=collation
        )
        self.cursor = self.connection.cursor(
            dictionary=True)

    def execute_query(self, query, param=None):
        self.cursor.execute(query, param)
        if query.strip().startswith("SELECT"):
            self.cursor.fetchall()
        self.connection.commit()

    def fetch_all(self, query, param=None):
        self.cursor.execute(query, param)
        return self.cursor.fetchall()

    def fetch_one(self, query, param=None):
        self.cursor.execute(query, param)
        return self.cursor.fetchone()

    def close(self):
        self.cursor.close()
        self.connection.close()
