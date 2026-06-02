import json
import os

import redis
from fastapi import FastAPI, HTTPException, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest

from database import get_connection


app = FastAPI(
    title="Real-Time Crypto Analytics API",
    description="FastAPI service for real-time crypto streaming analytics",
    version="1.0.0",
)

REQUEST_COUNT = Counter(
    "api_requests_total",
    "Total API requests",
    ["endpoint"]
)

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True
)


@app.get("/")
def root():
    REQUEST_COUNT.labels(endpoint="/").inc()
    return {
        "message": "Real-Time Crypto Streaming Analytics API",
        "status": "running"
    }


@app.get("/health")
def health_check():
    REQUEST_COUNT.labels(endpoint="/health").inc()

    try:
        conn = get_connection()
        conn.close()

        redis_client.ping()

        return {
            "status": "healthy",
            "database": "connected",
            "redis": "connected"
        }
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get("/prices/latest")
def get_latest_prices():
    REQUEST_COUNT.labels(endpoint="/prices/latest").inc()

    cached_data = redis_client.get("latest_prices")
    if cached_data:
        return json.loads(cached_data)

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT DISTINCT ON (symbol)
            symbol, currency, price, event_time, source, processed_at
        FROM crypto_prices
        ORDER BY symbol, processed_at DESC;
    """

    cursor.execute(query)
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    result = [
        {
            "symbol": row[0],
            "currency": row[1],
            "price": row[2],
            "event_time": str(row[3]),
            "source": row[4],
            "processed_at": str(row[5]),
        }
        for row in rows
    ]

    redis_client.setex("latest_prices", 10, json.dumps(result))
    return result


@app.get("/prices/{symbol}")
def get_price_history(symbol: str, limit: int = 20):
    REQUEST_COUNT.labels(endpoint="/prices/{symbol}").inc()

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT symbol, currency, price, event_time, source, processed_at
        FROM crypto_prices
        WHERE symbol = %s
        ORDER BY processed_at DESC
        LIMIT %s;
    """

    cursor.execute(query, (symbol.lower(), limit))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    if not rows:
        raise HTTPException(status_code=404, detail="Symbol not found")

    return [
        {
            "symbol": row[0],
            "currency": row[1],
            "price": row[2],
            "event_time": str(row[3]),
            "source": row[4],
            "processed_at": str(row[5]),
        }
        for row in rows
    ]


@app.get("/analytics/top-movers")
def get_top_movers():
    REQUEST_COUNT.labels(endpoint="/analytics/top-movers").inc()

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        WITH ranked_prices AS (
            SELECT
                symbol,
                price,
                processed_at,
                ROW_NUMBER() OVER (
                    PARTITION BY symbol ORDER BY processed_at DESC
                ) AS latest_rank,
                ROW_NUMBER() OVER (
                    PARTITION BY symbol ORDER BY processed_at ASC
                ) AS earliest_rank
            FROM crypto_prices
        ),
        latest AS (
            SELECT symbol, price AS latest_price
            FROM ranked_prices
            WHERE latest_rank = 1
        ),
        earliest AS (
            SELECT symbol, price AS earliest_price
            FROM ranked_prices
            WHERE earliest_rank = 1
        )
        SELECT
            latest.symbol,
            earliest.earliest_price,
            latest.latest_price,
            ROUND(
                ((latest.latest_price - earliest.earliest_price) / earliest.earliest_price * 100)::numeric,
                4
            ) AS change_percentage
        FROM latest
        JOIN earliest ON latest.symbol = earliest.symbol
        ORDER BY change_percentage DESC;
    """

    cursor.execute(query)
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return [
        {
            "symbol": row[0],
            "earliest_price": row[1],
            "latest_price": row[2],
            "change_percentage": float(row[3]),
        }
        for row in rows
    ]


@app.get("/analytics/average-price/{symbol}")
def get_average_price(symbol: str):
    REQUEST_COUNT.labels(endpoint="/analytics/average-price/{symbol}").inc()

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT
            symbol,
            AVG(price) AS average_price,
            MIN(price) AS min_price,
            MAX(price) AS max_price,
            COUNT(*) AS total_records
        FROM crypto_prices
        WHERE symbol = %s
        GROUP BY symbol;
    """

    cursor.execute(query, (symbol.lower(),))
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Symbol not found")

    return {
        "symbol": row[0],
        "average_price": float(row[1]),
        "min_price": row[2],
        "max_price": row[3],
        "total_records": row[4],
    }