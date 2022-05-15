import os
import psycopg2


def get_connection():
    with open(os.getenv('POSTGRES_PASSWORD_FILE'), 'r') as file:
        db_password = file.read()

    return psycopg2.connect(
        dbname=os.getenv('POSTGRES_DB'),
        user=os.getenv('POSTGRES_USER'),
        password=db_password,
        host=os.getenv('DATABASE_URL', 'localhost')
    )