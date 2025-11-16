import functools
import sqlite3

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            conn = sqlite3.connect('users.db')
            #print("Connection opened")
            kwargs["conn"] = conn
            return func(*args, **kwargs)

        finally:
            conn.close()
            #print("Connection closed")

    return wrapper

def transactional(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = kwargs.get("conn")
        if conn is None:
            raise ValueError("connection has to be passed")
        try:
            with conn:
                return func(*args, **kwargs)

        except Exception as e:
            print(f"Transaction failed: {e}")
            raise e

    return wrapper


@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))

update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
