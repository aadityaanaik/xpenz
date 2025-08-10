from fetch import email_to_record, get_emails
from config_loader import email_file, transactions_file

if __name__ == "__main__":
    contents=get_emails()
    email_to_record(contents)