import re
from datetime import date,timedelta
import json
import imaplib
import email
import logging
from llama import categorize
from email.header import decode_header
from config_loader import email_id, email_pass, senders

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def save_file(path,data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def save_transactions(email_path, transactions_path):
    save_emails(email_path)
    data = []
    with open(email_path, "r", encoding="utf-8") as f:
        contents = json.load(f)
    for content in contents:
        merchant_name = get_merchant(content)
        item = {
            "datetime": content['timestamp'],
            "amount": get_amt(content),
            "merchant": merchant_name,
            "category": categorize(merchant_name),
            "type": get_type(content)
        }
        if all(item.values()):  # filters out if any value is None or empty string
            data.append(item)
    save_file(transactions_path, data)
    return transactions_path

def get_amt(s):
    match = re.search(r'\$(\S+)', s['body'])
    return match.group(1) if match else None

def get_type(s):
    if "have a credit" in s['subject']:
        return "credit"
    if "transaction was charged" in s['subject']:
        return "debit"
    return "debit"

def get_merchant(s):
    match = None
    if(get_type(s) == "debit"):
        match = re.search(r'\bat (.*?) #', s['body'])
        if not match:
            match = re.search(r'\bat (.*?)(?:,|$)', s['body'])
    elif(get_type(s) == "credit"):
        match = re.search(r'\bfrom (.*?)(?:,|$)', s['subject'])

    return match.group(1) if match else None

def clean(text):
    """Decode and clean header values."""
    parts = decode_header(text)
    result = ''
    for part, enc in parts:
        if isinstance(part, bytes):
            result += part.decode(enc or 'utf-8', errors='ignore')
        else:
            result += part
    return result.strip()

def get_search_criteria(senders_array=None, since_date=None):
    if not senders_array:
        return f'(SINCE {since_date})'

    if not since_date:
        criteria = f'(FROM "{senders_array[-1]}")'
        for sender in reversed(senders_array[:-1]):
            criteria = f'(OR (FROM "{sender}") {criteria})'
        return f'(SINCE {since_date})'

    # Start with the last sender
    criteria = f'(FROM "{senders_array[-1]}" SINCE {since_date})'

    # Nest ORs backwards
    for sender in reversed(senders_array[:-1]):
        criteria = f'(OR (FROM "{sender}" SINCE {since_date}) {criteria})'

    return criteria

def save_emails(path):
    logging.info("Connecting to Gmail IMAP server...")
    imap = imaplib.IMAP4_SSL("imap.gmail.com")

    try:
        imap.login(email_id, email_pass)
        logging.info("Logged in successfully.")
    except imaplib.IMAP4.error as e:
        logging.error(f"Login failed: {e}")
        return []

    imap.select("inbox")
    yesterday = (date.today()- timedelta(days=1)).strftime('%d-%b-%Y')  # e.g., '15-Jun-2025'
    search_criteria = get_search_criteria(senders, yesterday)
    status, messages = imap.search(None, search_criteria)

    email_list = []
    if status != "OK":
        logging.warning("No messages found.")
        return []

    for num in messages[0].split():
        status, msg_data = imap.fetch(num, "(RFC822)")
        if status != "OK":
            logging.warning(f"Failed to fetch message {num}")
            continue

        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        subject = clean(msg["Subject"] or "")
        date_str = msg["Date"]
        try:
            date_obj = email.utils.parsedate_to_datetime(date_str)
            timestamp = date_obj.isoformat()
        except Exception:
            timestamp = ""

        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_dispo = str(part.get("Content-Disposition"))
                if content_type == "text/plain" and "attachment" not in content_dispo:
                    body_bytes = part.get_payload(decode=True)
                    if body_bytes:
                        body = body_bytes.decode(part.get_content_charset() or 'utf-8', errors='ignore')
                        break
        else:
            body_bytes = msg.get_payload(decode=True)
            if body_bytes:
                body = body_bytes.decode(msg.get_content_charset() or 'utf-8', errors='ignore')

        email_list.append({
            "timestamp": timestamp,
            "subject": subject,
            "body": body.strip()
        })

    imap.logout()
    logging.info(f"Fetched {len(email_list)} emails.")
    save_file(path, email_list)
    return None