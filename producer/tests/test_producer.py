import sys
from pathlib import Path

PRODUCER_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PRODUCER_ROOT))

from crypto_producer import build_events


def test_build_events_normalizes_coingecko_prices():
    price_data = {
        "bitcoin": {"usd": 61000.25},
        "ethereum": {"usd": 3300.75},
    }

    events = build_events(price_data)

    assert len(events) == 2
    assert events[0]["symbol"] == "bitcoin"
    assert events[0]["currency"] == "usd"
    assert events[0]["price"] == 61000.25
    assert events[0]["source"] == "coingecko"
    assert "event_time" in events[0]
