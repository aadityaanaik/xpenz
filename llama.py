import requests

OLLAMA_URL = "http://10.0.0.112:11434/api/generate"

def categorize(merchant_name: str) -> str:
    prompt = f"""
You are a financial assistant in the US that categorizes merchant names into categories. Categories include generic dapartments that will help me keep a track of where I am spending. You can only use the below categories (strictly). If it does not fit in the below put it in 'Others':
Groceries & Utilities
Rent & Mortgage
Healthcare
Gas & EV Charging
Insurance
Cabs
Public Transport
Food & Dining
Clothing & Accessories
Electronics & Gadgets
Home Goods & Furniture
Personal Care & Beauty
Streaming Services
Movies, Games & Events
Books, Music & Apps
Flights & Airlines
Hotels & Lodging
Car Rentals
Gifts
Charity Donations
Others

Now categorize: {merchant_name} and only give me the category name and nothing else."""

    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        return result.get("response", "").strip()
    except requests.RequestException as e:
        print(f"Error communicating with Ollama: {e}")
        return "Unknown"