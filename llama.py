import requests
import json
import logging
from config_loader import llama_host, llama_port, prompt_email_info, merch_category_info

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
        return response.json().get("response", "").strip()
    except requests.RequestException as e:
        logging.error(f"Error communicating with LLAMA: {e}")
        return "{}"


def get_info(subject, body) -> str:
    prompt = prompt_email_info.format(email_subject=subject, email_body=body)
    return process_prompt(prompt)


def get_categories_batch(merchants: list) -> list:
    """Send a list of merchant names in one LLM call. Returns a list of category dicts."""
    prompt = merch_category_info.format(merchants=json.dumps(merchants))
    response = process_prompt(prompt)

    start = response.find('[')
    end = response.rfind(']')
    if start == -1 or end == -1 or start >= end:
        raise ValueError(f"No JSON array found in LLM response: {response[:200]}")

    return json.loads(response[start:end + 1])
