import json
import time
from datetime import datetime, timezone

import requests
from kafka import KafkaProducer

from config import (
    KAFKA_BOOTSTRAP_SERVERS,
    KAFKA_TOPIC,
    COINGECKO_URL,
    CRYPTO_IDS,
    VS_CURRENCY,
    FETCH_INTERVAL_SECONDS,
)


def create_kafka_producer():
    while True:
        try:
            producer = KafkaProducer(
                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                value_serializer=lambda value: json.dumps(value).encode("utf-8"),
                retries=5,
            )
            print("Kafka producer connected successfully.")
            return producer
        except Exception as error:
            print(f"Kafka connection failed: {error}")
            print("Retrying in 5 seconds...")
            time.sleep(5)


def fetch_crypto_prices():
    params = {
        "ids": CRYPTO_IDS,
        "vs_currencies": VS_CURRENCY,
    }

    response = requests.get(COINGECKO_URL, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def build_events(price_data):
    events = []
    event_time = datetime.now(timezone.utc).isoformat()

    for symbol, values in price_data.items():
        event = {
            "symbol": symbol,
            "currency": VS_CURRENCY,
            "price": values.get(VS_CURRENCY),
            "event_time": event_time,
            "source": "coingecko",
        }
        events.append(event)

    return events


def main():
    producer = create_kafka_producer()

    while True:
        try:
            price_data = fetch_crypto_prices()
            events = build_events(price_data)

            for event in events:
                producer.send(KAFKA_TOPIC, value=event)
                print(f"Sent event to Kafka: {event}")

            producer.flush()
            time.sleep(FETCH_INTERVAL_SECONDS)

        except Exception as error:
            print(f"Producer error: {error}")
            time.sleep(5)


if __name__ == "__main__":
    main()