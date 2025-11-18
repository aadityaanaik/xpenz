xpenz

xpenz is a handy Python tool for keeping track of your spending. It automatically grabs your transactions, saves them, and even sorts them into categories for you. The best part? It uses a smart Large Language Model (LLM) to figure out what you bought, so you don't have to do it all by hand!

🌟 What's Inside?

Pulls Your Transactions: It automatically connects to your bank (or wherever) and downloads your transaction history.

Saves Everything: It keeps all your transactions safe and sound in a database.

Smart Sorting (with an LLM!): This is the really cool part. It uses a brainy AI (from llama.py) to read the messy transaction descriptions and automatically sort them into clean categories like "Groceries," "Gas," or "Bills."

Easy Config: It's simple to manage all your API keys and database settings in one place.

Ready for Automation: There's a dag folder, which means it's all set up to be automated with something like Airflow if you're into that.

🛠️ How It's Put Together

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


🚀 Let's Get This Going!

Want to get this running on your own machine? Just follow these steps.

1. What You'll Need

Python (version 3.9 or newer)

Pip (which usually comes with Python)

2. How to Install

Grab the code:

git clone [https://github.com/aadityaanaik/xpenz.git](https://github.com/aadityaanaik/xpenz.git)
cd xpenz


Install all the bits and pieces:
We really suggest using a virtual environment to keep things tidy.

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
.\venv\Scripts\activate

# Install the required packages
pip install -r requirements.txt


3. Setting It Up

(Heads up: This is just an example of how it probably works)

First, make a config file (like config.yaml or .env).

Inside that file, you'll need to paste in your database info, any API keys for your bank, and the API key for the LLM (llama.py).

# Example config.yaml
database:
  type: "sqlite"
  path: "xpenz.db"

plaid_api:
  client_id: "YOUR_CLIENT_ID"
  secret: "YOUR_SECRET"

llm_api:
  model: "llama3-8b"
  api_key: "YOUR_LLM_API_KEY"


Make sure config_loader.py knows where to find your new config file.

4. Run It!

Just run the main script, and it'll fetch and sort all your expenses:

python main.py


🤝 Want to Help Out?

Contributions are totally welcome! If you have an idea or a fix, feel free to open an issue or send over a pull request.

Fork the Project

Create your Feature Branch (git checkout -b feature/AmazingFeature)

Commit your Changes (git commit -m 'Add some AmazingFeature')

Push to the Branch (git push origin feature/AmazingFeature)

Open a Pull Request

📄 The Legal Stuff

This is shared under the MIT License. Check out the LICENSE file for all the details.
