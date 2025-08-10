# db.py

import psycopg2
import logging
from config_loader import db_name,db_user,db_pass,db_host,db_port, sql_insert_txn

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

def insert_transactions(record, dbname, user, password, host, port):
    conn = None
    try:
        conn = get_connection(dbname, user, password, host, port)
        cur = conn.cursor()
        query = sql_insert_txn
        # for record in data:
        values = (
                record["datetime"],
                record["amount"],
                record["merchant"],
                record["card"],
                record["category"],
                record["type"]
            )
        cur.execute(query, values)
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