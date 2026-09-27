FROM apache/airflow:2.10.0

USER airflow

RUN pip install --no-cache-dir \
    yfinance \
    pandas \
    psycopg2-binary \
    python-dotenv \
    loguru