from fetch import save_transactions
from db import json2db
from config_loader import email_file, transactions_file

if __name__ == "__main__":
    json2db(save_transactions(email_file, transactions_file))