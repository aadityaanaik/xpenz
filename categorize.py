import psycopg2
import psycopg2.extras
import logging
from datetime import date, timedelta
from llama import get_category
from db import get_connection
from config_loader import db_name,db_user,db_pass,db_host,db_port, sql_existing_merchants, sql_distinct_merchant_txn_date, sql_distinct_merchant_txn, sql_insert_merch_cat

def fetch_merchants(conn, query):
    with conn.cursor() as cur:
        cur.execute(query)
        results = cur.fetchall()
        return {row[0] for row in results}  # Return a set for efficient comparison

def bulk_insert_categories(conn, new_categories):
    with conn.cursor() as cur:
        psycopg2.extras.execute_values(cur, sql_insert_merch_cat, new_categories)
    conn.commit()
    logging.info(f"Successfully inserted or updated {len(new_categories)} merchant categories.")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
conn = None
try:
    conn = get_connection(db_name,db_user,db_pass,db_host,db_port)

    # 1. Get distinct merchants from recent transactions
    recent_merchants = []
    since_date = date.today() - timedelta(days=1)
    # recent_merchants = fetch_merchants(conn, sql_distinct_merchant_txn_date.format(since_date = since_date))
    recent_merchants.extend(fetch_merchants(conn, sql_distinct_merchant_txn))
    logging.info(f"Found {len(recent_merchants)} unique merchants since yesterday.")

    # 2. Get merchants that are already categorized
    categorized_merchants=[]
    categorized_merchants.extend(fetch_merchants(conn, sql_existing_merchants))
    logging.info(f"Found {len(categorized_merchants)} merchants that are already categorized.")

    # 3. Find the merchants that need categorization
    merchants_to_categorize = list(set(recent_merchants) - set(categorized_merchants))

    if not merchants_to_categorize:
        logging.info("No new merchants to categorize. All up to date!")
        exit(0)

    logging.info(f"Found {len(merchants_to_categorize)} new merchants to categorize.")

    # 4. Get categories from Llama and create a map
    new_categories = []
    for merchant in merchants_to_categorize:
        logging.info(f"Categorizing merchant: '{merchant}'...")
        category = get_category(merchant)
        new_categories.append((merchant, category))

    # 5. Insert new categories into the database
    if new_categories:
        bulk_insert_categories(conn, new_categories)

except psycopg2.Error as e:
    logging.error(f"Database error: {e}")
except Exception as e:
    logging.error(f"An unexpected error occurred: {e}")
finally:
    if conn:
        conn.close()
        logging.info("Database connection closed.")