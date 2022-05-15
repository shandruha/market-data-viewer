from datetime import datetime
from random import random
from time import sleep
from utils.db import get_connection


def generate_movement():
    movement = -1 if random() < 0.5 else 1
    return movement


if __name__ == '__main__':
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute('SELECT id FROM tickers ORDER BY id')

        last_prices = {}
        for ticker_id, in cursor.fetchall():
            last_prices[ticker_id] = 0.0

        cursor.execute('''
            SELECT ticker_id, price 
            FROM price_history 
            WHERE date_time = (SELECT MAX(date_time) FROM price_history)
        ''')

        for ticker_id, price in cursor.fetchall():
            last_prices[ticker_id] = price

        while True:
            try:
                for ticker_id in last_prices.keys():
                    price = last_prices[ticker_id] + generate_movement()
                    cursor.execute(
                        'INSERT INTO price_history (date_time, ticker_id, price) VALUES (%s, %s, %s)',
                        (datetime.now(), ticker_id, price)
                    )
                    conn.commit()
                    last_prices[ticker_id] = price
            except Exception as e:
                print(e)
                conn.rollback()

            print(last_prices)
            sleep(1)