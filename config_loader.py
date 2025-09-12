import json

# Load config
with open('config.json', 'r') as f:
    config = json.load(f)

# Access EMAIL_CONFIG
email_id = config['EMAIL_CONFIG']['EMAIL']
email_pass = config['EMAIL_CONFIG']['EMAIL_PASS']
senders_config = config['EMAIL_CONFIG']['SENDER']

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
email_file = config['FILE_CONFIG']['EMAIL_FILE']
transactions_file = config['FILE_CONFIG']['TRANSACTIONS_FILE']

# Access PROMPTS_CONFIG
prompt_email_info = config['PROMPT_CONFIG']['EMAIL_INFO']
merch_category_info = config['PROMPT_CONFIG']['MERCH_CATEGORY_INFO']

# Access QUERY_CONFIG
sql_insert_txn = config['QUERY_CONFIG']['INSERT_TXN']
sql_insert_merch_cat = config['QUERY_CONFIG']['INSERT_MERCH_CAT']
sql_existing_merchants = config['QUERY_CONFIG']['SELECT_EXISTING_MERCH_CAT']
sql_distinct_merchant_txn_date = config['QUERY_CONFIG']['SELECT_DISTINCT_MERCH_TXN_DATE']
sql_distinct_merchant_txn = config['QUERY_CONFIG']['SELECT_DISTINCT_MERCH_TXN']
sql_latest_date = config['QUERY_CONFIG']['SELECT_LATEST_DATE']

print(f"Connecting to DB at {db_host}:{db_port} as {db_user}")
print(f"LLaMA running at {llama_host}:{llama_port}")