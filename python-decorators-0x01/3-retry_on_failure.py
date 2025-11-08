import functools
import sqlite3
import time


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

def retry_on_failure(retries=3, delay=2):
    def retry_wrapper(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            conn = kwargs.get("conn")
            if conn is None:
                raise ValueError("connect has to be passed")

            retry_count = 0
            while retry_count < retries:
                try:
                    with conn:
                        return func(*args, **kwargs)

                except Exception as e:
                    retry_count += 1
                    if retry_count == retries:
                        print(f"Failed to execute after {retries} tries")
                        raise

                    print(f"Failed: {e}, retrying in {delay} seconds")
                    time.sleep(delay)

            raise
        return wrapper

    return retry_wrapper


@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")

    return cursor.fetchall()


users = fetch_users_with_retry()

print(users)
