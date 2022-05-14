import psycopg2
from utils.db import get_connection


if __name__ == '__main__':
    with get_connection('md_admin', 'md_password') as conn:
        cursor = conn.cursor()

        cursor.execute('DROP TABLE IF EXISTS price_history')
        cursor.execute('DROP TABLE IF EXISTS tickers')
        cursor.execute('DROP ROLE IF EXISTS data_generator')
        cursor.execute('DROP ROLE IF EXISTS app')

        cursor.execute('CREATE TABLE tickers (id SERIAL PRIMARY KEY, name VARCHAR(200))')
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS price_history (
                date_time TIMESTAMP, 
                ticker_id INT, 
                price REAL,
                CONSTRAINT fk_tickers
                    FOREIGN KEY(ticker_id) 
	                    REFERENCES tickers(id)
            )
        """)

        cursor.execute("CREATE USER data_generator WITH PASSWORD 'data_generator'")
        cursor.execute('GRANT SELECT, INSERT, UPDATE, DELETE ON price_history, tickers TO data_generator')

        cursor.execute("CREATE USER app WITH PASSWORD 'app'")
        cursor.execute('GRANT SELECT ON price_history, tickers TO app')

        try:
            for i in range(100):
                cursor.execute(
                    'INSERT INTO tickers VALUES (%s, %s) ON CONFLICT(id) DO NOTHING',
                    (i + 1, 'ticker_{:02d}'.format(i))
                )
            conn.commit()
            print('Done')
        except psycopg2.Error as e:
            print('Error: ' + str(e))
            conn.rollback()
