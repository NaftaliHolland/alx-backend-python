import sqlite3


class ExecuteQuery(object):
    def __init__(self, db_name, query, param):
        self.conn = sqlite3.connect(db_name)
        self.query = query
        self.param = param

    def __enter__(self):
        cursor = self.conn.cursor()

        cursor.execute(self.query, self.param)
        return cursor.fetchall()

    def __exit__(self, type, value, traceback):
        self.conn.close()

with ExecuteQuery('users.db', 'SELECT * FROM users WHERE age > ?', (25,)) as result:
    print(result)
