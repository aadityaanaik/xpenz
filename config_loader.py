import json

# Load config
with open('config.json', 'r') as f:
    config = json.load(f)

# Access EMAIL_CONFIG
email_id = config['EMAIL_CONFIG']['EMAIL']
email_pass = config['EMAIL_CONFIG']['EMAILPASS']
senders = config['EMAIL_CONFIG']['SENDER']

# Access DB_CONFIG
db_host = config['DB_CONFIG']['DBHOST']
db_user = config['DB_CONFIG']['DBUSER']
db_pass = config['DB_CONFIG']['DBPASS']
db_name = config['DB_CONFIG']['DBNAME']
db_port = config['DB_CONFIG']['DBPORT']

# Access LLAMA_CONFIG
llama_host = config['LLAMA_CONFIG']['LLAMA_HOST']
llama_port = config['LLAMA_CONFIG']['LLAMA_PORT']

# Access FILE_CONFIG
email_file = config['EMAIL_CONFIG']['EMAIL_FILE']
transactions_file = config['TRANSACTIONS_CONFIG']['TRANSACTIONS_FILE']

# Example usage
print(f"Connecting to DB at {db_host}:{db_port} as {db_user}")
print(f"LLaMA running at {llama_host}:{llama_port}")