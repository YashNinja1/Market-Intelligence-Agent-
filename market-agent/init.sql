CREATE TABLE IF NOT EXISTS stocks (
    id          SERIAL PRIMARY KEY,
    symbol      VARCHAR(10) NOT NULL,
    company_name VARCHAR(100),
    price       NUMERIC(10, 2) NOT NULL,
    change      NUMERIC(10, 2),
    change_pct  VARCHAR(20),
    volume      BIGINT,
    fetched_at  TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS news (
    id              SERIAL PRIMARY KEY,
    symbol          VARCHAR(10) NOT NULL,
    company_name    VARCHAR(100),
    title           TEXT NOT NULL,
    source          VARCHAR(100),
    url             TEXT,
    summary         TEXT,
    sentiment       VARCHAR(20),
    sentiment_score NUMERIC(5, 4),
    published_at    VARCHAR(50),
    fetched_at      TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_stocks_symbol ON stocks(symbol);
CREATE INDEX IF NOT EXISTS idx_news_symbol ON news(symbol);