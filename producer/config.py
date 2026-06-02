import os
from dotenv import load_dotenv

load_dotenv()

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "crypto-prices")

COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"

CRYPTO_IDS = "bitcoin,ethereum,solana,cardano,dogecoin"
VS_CURRENCY = "usd"

FETCH_INTERVAL_SECONDS = 10