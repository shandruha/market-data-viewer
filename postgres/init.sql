DROP TABLE IF EXISTS price_history;
DROP TABLE IF EXISTS tickers;

CREATE TABLE tickers (id SERIAL PRIMARY KEY, name VARCHAR(200));

CREATE TABLE IF NOT EXISTS price_history (
    date_time TIMESTAMP,
    ticker_id INT,
    price REAL,
    CONSTRAINT fk_tickers
        FOREIGN KEY(ticker_id)
            REFERENCES tickers(id)
);

INSERT INTO tickers (id, name)
SELECT i + 1 AS id, 'ticker_' || TO_CHAR(i, 'fm00') AS name
FROM generate_series(0, 99) i;