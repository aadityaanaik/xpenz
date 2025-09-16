# db.py

import psycopg2
import logging
from config_loader import db_name,db_user,db_pass,db_host,db_port, sql_insert_txn, sql_latest_date
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def get_connection(dbname, user, password, host, port):
    logging.info("Connecting to the database...")
    try:
        conn = psycopg2.connect(
            dbname = dbname,
            user = user,
            password = password,
            host = host,
            port = port
        )
        logging.info("Successfully connected to the database.")
        return conn
    except Exception as e:
        logging.error(f"Failed to connect to the database: {e}")
        raise

def insert_category(conn, sql_insert_merch_cat, data):
    with conn.cursor() as cur:
        # Execute the SQL command with a tuple of values
        merchant = data['original_merchant']
        company = data['refined_merchant_name']
        category = data['category']
        cur.execute(sql_insert_merch_cat, (merchant, company, category))

        # Check cur.rowcount to see if a row was actually inserted
        if cur.rowcount > 0:
            logging.info(f"Successfully inserted category for merchant: {merchant}")
        else:
            logging.info(f"Merchant '{merchant}' already exists. No new category inserted.")

    conn.commit()

def insert_transactions(record, dbname, user, password, host, port):
    conn = None
    try:
        conn = get_connection(dbname, user, password, host, port)
        cur = conn.cursor()
        cur.execute(sql_insert_txn, record)
        logging.info(f"Inserted transaction into the database.")
        conn.commit()
        cur.close()
    except Exception as e:
        logging.error(f"Error inserting record: {record}\n {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()
            logging.info("Database connection closed.")

def record_to_db(record):
    logging.info(f"Inserting {record} into {db_name}")
    try:
        insert_transactions(record, db_name, db_user, db_pass, db_host, db_port)
    except Exception as e:
        logging.error(f"Unexpected error: {e}")


def get_latest_date(dbname, user, password, host, port):

    latest_date = None
    try:
        with get_connection(dbname, user, password, host, port) as conn:
            with conn.cursor() as cur:
                cur.execute(sql_latest_date)

                record = cur.fetchone()  # Fetches the first row of the result

                if record:
                    latest_date = datetime.strptime(str(record[0]), '%Y-%m-%d').strftime('%d-%b-%Y')
                    logging.info(f"Successfully extracted latest date: {latest_date}")

    except Exception as e:
        logging.error(f"Error getting latest date: {e}")

    return latest_date