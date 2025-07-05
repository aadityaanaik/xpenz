# db.py
import psycopg2
from psycopg2.extras import execute_values
import json
import logging

# Configure logging
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

def insert_transactions(data, dbname, user, password, host, port):
    conn = None
    try:
        conn = get_connection(dbname, user, password, host, port)
        cur = conn.cursor()

        query = """
            INSERT INTO transactions (datetime, amount, merchant, category, type)
            VALUES %s
            ON CONFLICT ON CONSTRAINT unique_transaction_entry DO NOTHING
        """

        values = [
            (
                record["datetime"],
                float(record["amount"]),
                record["merchant"],
                record["category"],
                record["type"]
            )
            for record in data
        ]

        execute_values(cur, query, values)
        conn.commit()
        logging.info(f"Inserted {len(values)} transactions into the database.")

        cur.close()
    except Exception as e:
        logging.error(f"Error inserting transactions: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()
            logging.info("Database connection closed.")

def json2db(file_name, dbname, user, password, host, port):
    try:
        with open(file_name, "r") as f:
            data = json.load(f)
            logging.info(f"Loaded {len(data)} records from {file_name}.")
        insert_transactions(data, dbname, user, password, host, port)
    except FileNotFoundError:
        logging.error(f"File not found: {file_name}")
    except json.JSONDecodeError as e:
        logging.error(f"Error parsing JSON file: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")