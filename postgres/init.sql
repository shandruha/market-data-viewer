DROP TABLE IF EXISTS price_history;
DROP TABLE IF EXISTS tickers;

DROP ROLE IF EXISTS data_generator;
DROP ROLE IF EXISTS app;

CREATE TABLE tickers (id SERIAL PRIMARY KEY, name VARCHAR(200));
CREATE TABLE IF NOT EXISTS price_history (
    date_time TIMESTAMP,
    ticker_id INT,
    price REAL,
    CONSTRAINT fk_tickers
        FOREIGN KEY(ticker_id)
            REFERENCES tickers(id)
);

CREATE USER data_generator WITH PASSWORD 'data_generator';
GRANT SELECT, INSERT, UPDATE, DELETE ON price_history, tickers TO data_generator;

CREATE USER app WITH PASSWORD 'app';
GRANT SELECT ON price_history, tickers TO app;