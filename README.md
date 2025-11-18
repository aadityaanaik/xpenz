# xpenz

xpenz is a handy Python tool for keeping track of your spending by automatically reading your email. It parses new transaction alerts, extracts the key details, saves them to a database, and even sorts them into categories for you. The best part? It uses a smart Large Language Model (LLM) to understand the emails and merchant names, so you don't have to do it all by hand!

## 🌟 What's Inside?

* **Pulls Transactions from Emails:** It securely connects to your email account (via IMAP), finds transaction alerts from banks like Chase, Amex, Citi, and Capital One, and parses them.
* **Smart Extraction (with an LLM!):** This is the core magic. It uses an LLM (via `llama.py`) with specific prompts to read the email subject and body and accurately extract the **amount**, **merchant**, and **transaction type (debit/credit)**.
* **Smart Categorization (with an LLM!):** After extracting a "messy" merchant name (e.g., "AMZN Mktp US"), it uses the LLM again to refine it to a clean name ("Amazon") and assign a clear category like "Shopping."
* **Saves Everything:** It stores all your transactions and categorized merchants in a **PostgreSQL database**.
* **Ready for Automation:** There's a `dag` folder, which means it's all set up to be automated with something like Airflow if you're into that.

---

## 🛠️ How It's Put Together

Here's a quick look at the main files and what they do:
/
├── dag/                  # Orchestration files (e.g., for Airflow)
├── .gitignore            # Git ignore file
├── LICENSE               # MIT License
├── README.md             # This file
├── categorize.py         # Logic for categorizing expenses
├── config_loader.py      # Loads configuration from environment or files
├── db.py                 # Database connection and query logic
├── fetch.py              # Fetches transaction data from sources
├── llama.py              # Handles interaction with the LLM for categorization
├── main.py               # Main entry point for the application
└── requirements.txt      # Python dependencies

---

## 🚀 Let's Get This Going!

Want to get this running on your own machine? Just follow these steps.

### 1. What You'll Need

* Python (version 3.9 or newer)
* A running **PostgreSQL database**
* A running **Llama instance** (like [Ollama](https://ollama.com/)) accessible on your network.
* A **Google App Password** for your email (if using Gmail). [How to create one](https://support.google.com/accounts/answer/185833).

### 2. How to Install

1.  Grab the code:
    ```sh
    git clone [https://github.com/aadityaanaik/xpenz.git](https://github.com/aadityaanaik/xpenz.git)
    cd xpenz
    ```

2.  Install all the bits and pieces:
    We really suggest using a virtual environment to keep things tidy.

    ```sh
    # Create a virtual environment
    python3 -m venv venv

    # Activate the virtual environment
    # On macOS/Linux:
    source venv/bin/activate
    # On Windows:
    .\venv\Scripts\activate

    # Install the required packages
    pip install -r requirements.txt
    ```

### 3. Setting It Up

You'll need to create a `config.json` file in the root directory. Copy the template below and fill in your own details.

**`config.json` Template:**

```json
{
    "EMAIL_CONFIG":
    {
        "EMAIL": "your-email@gmail.com",
        "EMAIL_PASS": "your-google-app-password",
        "SENDER": {
            "capitalone@notification.capitalone.com": {
              "card":"Capital One",
                "subject": "A new transaction was charged to your account"
            },
            "alerts@info6.citi.com": {
                "card":"Citi",
                "subject": "transaction was made on your Costco Anywhere account"
            },
            "americanexpress@welcome.americanexpress.com": {
                "card": "Amex",
                "subject": "Large Purchase Approved"
            },
            "no.reply.alerts@chase.com": {
                "card": "Chase",
                "subject": "transaction with"
            }
        }
    },
    "DB_CONFIG":
    {
        "DBNAME": "xpenz",
        "DBUSER": "your_db_user",
        "DBPASS": "your_db_password",
        "DBHOST": "your_db_host_ip",
        "DBPORT": "5432"
    },
    "LLAMA_CONFIG": {
        "LLAMA_PORT": "11434",
        "LLAMA_HOST": "your_llama_host_ip"
    },
    "QUERY_CONFIG": {
        "INSERT_TXN": "INSERT INTO txn (datetime, card, merchant, amount, type)\n    VALUES (%(datetime)s, %(card)s, %(merchant)s, %(amount)s, %(type)s)\n    ON CONFLICT ON CONSTRAINT unique_txn_record DO NOTHING",
        "INSERT_MERCH_CAT": "INSERT INTO merch_cat (merchant, company, category)\n            VALUES (%s, %s, %s) ON CONFLICT (merchant) DO NOTHING;",
        "SELECT_DISTINCT_MERCH_TXN": "SELECT DISTINCT merchant FROM txn",
        "SELECT_DISTINCT_MERCH_TXN_DATE": "SELECT DISTINCT merchant FROM txn WHERE datetime >= {since_date}",
        "SELECT_EXISTING_MERCH_CAT": "SELECT distinct merchant FROM merch_cat",
        "SELECT_LATEST_DATE": "SELECT DATE(MAX(datetime)) FROM txn"
    },
    "PROMPT_CONFIG": {
        "EMAIL_INFO": "You are an automated financial data extraction API. Your sole purpose is to analyze the subject and body of a financial email and extract key details into a structured JSON format... (prompt text) ...[SUBJECT]: {email_subject}\\\\n[BODY]: {email_body}\\\\n---END DATA---",
        "MERCH_CATEGORY_INFO": "Return ONLY one JSON object with structure ... (prompt text) ... Now, process this merchant: {merchant}"
    }
}
```
### Configuration Breakdown

* EMAIL_CONFIG:
EMAIL/EMAIL_PASS: Your email login credentials. Use an App Password for security.
SENDER: This is the rule set. It tells the app which emails to look for. It maps a sender's email and subject line text to a          specific card name (e.g., "Amex").

* DB_CONFIG: Your PostgreSQL database connection details.

* LLAMA_CONFIG: The host and port where your Llama (Ollama) instance is running.

* QUERY_CONFIG: The exact SQL queries the app uses. You probably don't need to change these unless you change the database schema.

* PROMPT_CONFIG: The powerful prompts that are sent to the LLM to extract data and categorize merchants.

4. Run It!
Just run the main script, and it'll connect to your email, fetch new transactions, and sort them into your database:

```Bash
python main.py
```

---

## 🤝 Want to Help Out?
Contributions are totally welcome! If you have an idea or a fix, feel free to open an issue or send over a pull request.
* Fork the Project

* Create your Feature Branch (git checkout -b feature/AmazingFeature)

* Commit your Changes (git commit -m 'Add some AmazingFeature')

* Push to the Branch (git push origin feature/AmazingFeature)

* Open a Pull Request

---

## 📄 The Legal Stuff
This is shared under the MIT License. Check out the LICENSE file for all the details.
