import sqlite3

class DatabaseConnection(object):
    def __init__(self, db_name):
        # Create database connection
        #print("Opening connection")
        self.conn = sqlite3.connect(db_name)
    def __enter__(self):
        return self.conn

    def __exit__(self, type, value, traceback):
        #print("Closing connection")
        self.conn.close()


with DatabaseConnection('users.db') as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    print(results)


