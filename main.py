from fetch import email_to_record, get_emails

if __name__ == "__main__":
    contents=get_emails()
    email_to_record(contents)