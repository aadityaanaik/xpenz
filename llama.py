import requests
import logging
import json
from config_loader import llama_host,llama_port, prompt_email_info, merch_category_info

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

LLAMA_URL = f"http://{llama_host}:{llama_port}/api/generate"

def process_prompt(prompt):
    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(LLAMA_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        return result.get("response", "").strip()
    except requests.RequestException as e:
        logging.error(f"Error communicating with LLAMA: {e}")
        return "{}"

def get_info(subject, body) -> str:
    prompt = prompt_email_info.format(
    email_subject=subject,
    email_body=body)
    return process_prompt(prompt)

def get_category(merchants_to_categorize):
    prompt = merch_category_info.format(
        merchant_list_json=json.dumps(merchants_to_categorize)
    )
    return process_prompt(prompt)