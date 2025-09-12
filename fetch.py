import re
import json
import imaplib
import email
import logging

from db import record_to_db, get_latest_date
from datetime import date, timedelta
from llama import get_info
from email.header import decode_header
from config_loader import email_id, email_pass, senders_config, db_name, db_user, db_pass, db_host, db_port
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def save_file(path,data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def email_to_record(emails):
    for email in emails:
        body = email["body"]
        subject = email["subject"]
        sender = re.search(r'<([^>]+)>', email["sender"]).group(1).lower()
        logging.info(f"Processing email via LLAMA: {email}")
        item=json.loads(get_info(subject ,body))
        logging.info("Email processed successfully!")

        item['datetime'] = email["timestamp"]
        item['card'] = senders_config[sender]['card']
        print(item)
        try:
            record_to_db(item)
        except Exception as e:
            logging.error(e)
            return 1
    return 0

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


def get_search_criteria(senders_config, since_date):
    pair_criteria = [
        f'(FROM "{sender}" SUBJECT "{details["subject"]}")'
        for sender, details in senders_config.items()
    ]

    if not pair_criteria:
        return ""  # No valid criteria to build a query from

    if len(pair_criteria) == 1:
        combined_criteria = pair_criteria[0]
    else:
        combined_criteria = pair_criteria[-1]
        for criterion in reversed(pair_criteria[:-1]):
            combined_criteria = f'(OR {criterion} {combined_criteria})'

    # The final query combines the sender/subject logic with the date
    final_query_parts = [combined_criteria]
    if since_date:
        final_query_parts.append(f'SINCE {since_date}')

    return ' '.join(final_query_parts)

def get_emails():
    logging.info("Connecting to Gmail IMAP server...")
    imap = imaplib.IMAP4_SSL("imap.gmail.com")

    try:
        imap.login(email_id, email_pass)
        logging.info("Logged in successfully.")
    except imaplib.IMAP4.error as e:
        logging.error(f"Login failed: {e}")
        return []

    imap.select("inbox")
    latest_date = get_latest_date(db_name, db_user, db_pass, db_host, db_port)
    # yesterday = (date.today()- timedelta(days=1)).strftime('%d-%b-%Y')
    logging.error(f"Latest Date: {latest_date}")
    search_criteria = get_search_criteria(senders_config, latest_date)
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

        sender = msg['From']
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

        soup = BeautifulSoup(body, "lxml")
        text_with_spaces = soup.get_text(separator=" ", strip=True)
        lines = (line.strip() for line in text_with_spaces.splitlines())
        clean_body = '\n'.join(line for line in lines if line)
        clean_body = clean_body.replace('\u200c', '').replace('\xa0', ' ')

        email_list.append({
            "timestamp": timestamp,
            "sender": sender,
            "subject": subject,
            "body": clean_body.strip()
        })

    imap.logout()
    logging.info(f"Fetched {len(email_list)} emails.")

    return email_list