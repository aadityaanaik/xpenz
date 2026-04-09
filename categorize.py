import json
import psycopg2
import logging
from llama import get_categories_batch
from db import get_connection, insert_category, fetch_merchants, SQL_DISTINCT_MERCHANTS, SQL_EXISTING_MERCH_CAT

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

ORC_OVERRIDE = {"refined_merchant_name": "ORCA", "category": "Transportation"}


def get_data_batch(merchants: list) -> list:
    overrides = [
        {**ORC_OVERRIDE, "original_merchant": m}
        for m in merchants if m[:3] == "ORC"
    ]
    to_llm = [m for m in merchants if m[:3] != "ORC"]

    results = overrides

    if to_llm:
        for attempt in range(1, 3):
            try:
                results = results + get_categories_batch(to_llm)
                break
            except (json.JSONDecodeError, ValueError) as e:
                logging.warning(f"Batch categorization failed (attempt {attempt}/2): {e}")
        else:
            logging.error("Failed to categorize merchants after 2 attempts. Skipping batch.")

    return results


def main():
    conn = None
    try:
        conn = get_connection()

        all_merchants = fetch_merchants(conn, SQL_DISTINCT_MERCHANTS)
        logging.info(f"Found {len(all_merchants)} unique merchants.")

        categorized = fetch_merchants(conn, SQL_EXISTING_MERCH_CAT)
        logging.info(f"Found {len(categorized)} already categorized.")

        to_categorize = list(all_merchants - categorized)

        if not to_categorize:
            logging.info("No new merchants to categorize. All up to date!")
            return

        logging.info(f"Categorizing {len(to_categorize)} new merchants in one batch...")
        results = get_data_batch(to_categorize)

        for data in results:
            try:
                insert_category(conn, data)
            except Exception as e:
                logging.error(f"Failed to insert category for '{data.get('original_merchant')}': {e}")

    except psycopg2.Error as e:
        logging.error(f"Database error: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
    finally:
        if conn:
            conn.close()
            logging.info("Database connection closed.")


if __name__ == "__main__":
    main()
