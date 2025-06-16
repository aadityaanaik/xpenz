# main.py
import fetch
import db
from config import EMAIL_CONFIG, DB_CONFIG

if __name__ == "__main__":
    fetch.fetch_emails(
        EMAIL_CONFIG["EMAIL"],
        EMAIL_CONFIG["EMAILPASS"],
        EMAIL_CONFIG["SENDER"]
    )

    fetch.filter_json("emails.json")

    db.json2db(
        "transactions.json",
        DB_CONFIG["DBNAME"],
        DB_CONFIG["DBUSER"],
        DB_CONFIG["DBPASS"],
        DB_CONFIG["DBHOST"],
        DB_CONFIG["DBPORT"]
    )