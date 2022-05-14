import os
import psycopg2


def get_connection(user, password):
    return psycopg2.connect(
        dbname='market_data',
        user=user,
        password=password,
        host=os.getenv("DATABASE_URL", "localhost")
    )