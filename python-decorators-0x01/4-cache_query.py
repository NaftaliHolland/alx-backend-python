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

query_cache = {}

def cache_query(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get("query")
        if query is None:
            raise ValueError("query cannot be null")

        value = query_cache.get(query)
        if value is None:
            print("We are hitting the database now")
            value = func(*args, **kwargs)
            query_cache[query] = value

        return value

    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

users = fetch_users_with_cache(query="SELECT * FROM users")


# I will change the cache to really see this working.
users_again = fetch_users_with_cache(query="SELECT * FROM users")
