# db.py

import psycopg2
import logging
from config_loader import db_name, db_user, db_pass, db_host, db_port
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

SQL_INSERT_TXN = (
    "INSERT INTO txn (datetime, card, merchant, amount, type) "
    "VALUES (%(datetime)s, %(card)s, %(merchant)s, %(amount)s, %(type)s) "
    "ON CONFLICT ON CONSTRAINT unique_txn_record DO NOTHING"
)
SQL_INSERT_MERCH_CAT = (
    "INSERT INTO merch_cat (merchant, company, category) "
    "VALUES (%s, %s, %s) ON CONFLICT (merchant) DO NOTHING"
)
SQL_DISTINCT_MERCHANTS = "SELECT DISTINCT merchant FROM txn"
SQL_EXISTING_MERCH_CAT = "SELECT DISTINCT merchant FROM merch_cat"
SQL_LATEST_DATE = "SELECT DATE(MAX(datetime)) FROM txn"


def get_connection():
    logging.info("Connecting to the database...")
    try:
        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_pass,
            host=db_host,
            port=db_port
        )
        logging.info("Successfully connected to the database.")
        return conn
    except Exception as e:
        logging.error(f"Failed to connect to the database: {e}")
        raise


def insert_transaction(conn, record):
    with conn.cursor() as cur:
        cur.execute(SQL_INSERT_TXN, record)
        if cur.rowcount > 0:
            logging.info(f"Inserted transaction: {record.get('merchant')} {record.get('amount')}")
        else:
            logging.info("Duplicate transaction skipped.")
    conn.commit()


def insert_category(conn, data):
    merchant = data['original_merchant']
    with conn.cursor() as cur:
        cur.execute(SQL_INSERT_MERCH_CAT, (merchant, data['refined_merchant_name'], data['category']))
        if cur.rowcount > 0:
            logging.info(f"Inserted category for merchant: {merchant}")
        else:
            logging.info(f"Merchant '{merchant}' already exists. Skipped.")
    conn.commit()


def fetch_merchants(conn, query):
    with conn.cursor() as cur:
        cur.execute(query)
        return {row[0] for row in cur.fetchall()}


def get_latest_date():
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute(SQL_LATEST_DATE)
            record = cur.fetchone()
            if record and record[0]:
                latest = datetime.strptime(str(record[0]), '%Y-%m-%d').strftime('%d-%b-%Y')
                logging.info(f"Latest transaction date: {latest}")
                return latest
    except Exception as e:
        logging.error(f"Error getting latest date: {e}")
    finally:
        if conn:
            conn.close()
    return None
