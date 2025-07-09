# main.py
import fetch
import db
from config_loader import *

if __name__ == "__main__":
    fetch.fetch_emails()

    fetch.filter_json("emails.json")

    db.json2db("transactions.json")