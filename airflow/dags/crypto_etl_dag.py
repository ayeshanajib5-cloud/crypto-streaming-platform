from datetime import datetime, timedelta

import psycopg2
import requests
from airflow import DAG
from airflow.operators.python import PythonOperator


POSTGRES_CONFIG = {
    "dbname": "crypto_db",
    "user": "crypto_user",
    "password": "crypto_password",
    "host": "postgres",
    "port": 5432,
}


default_args = {
    "owner": "ayesha",
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}


def check_api_health():
    response = requests.get("http://api:8000/health", timeout=10)
    response.raise_for_status()
    return response.json()


def check_database_records():
    conn = psycopg2.connect(**POSTGRES_CONFIG)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM crypto_prices;")
    count = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    if count == 0:
        raise ValueError("No crypto records found in PostgreSQL.")

    return f"Database has {count} crypto records."


def cleanup_old_records():
    conn = psycopg2.connect(**POSTGRES_CONFIG)
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM crypto_prices
        WHERE processed_at < NOW() - INTERVAL '7 days';
    """)

    deleted_rows = cursor.rowcount
    conn.commit()

    cursor.close()
    conn.close()

    return f"Deleted {deleted_rows} old records."


with DAG(
    dag_id="crypto_pipeline_validation",
    default_args=default_args,
    description="Validate crypto streaming pipeline health and clean old records",
    start_date=datetime(2026, 1, 1),
    schedule_interval="@hourly",
    catchup=False,
    tags=["crypto", "streaming", "etl"],
) as dag:

    api_health_check = PythonOperator(
        task_id="check_fastapi_health",
        python_callable=check_api_health,
    )

    database_record_check = PythonOperator(
        task_id="check_database_records",
        python_callable=check_database_records,
    )

    cleanup_task = PythonOperator(
        task_id="cleanup_old_records",
        python_callable=cleanup_old_records,
    )

    api_health_check >> database_record_check >> cleanup_task