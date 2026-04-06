import requests
from config import TELEGRAM_BOT_TOKEN

BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"


def send_message(chat_id, text):
    r = requests.post(
        f"{BASE_URL}/sendMessage",
        data={
            "chat_id": chat_id,
            "text": text
        },
        timeout=20
    )
    r.raise_for_status()


def send_photo(chat_id, image_bytes):
    r = requests.post(
        f"{BASE_URL}/sendPhoto",
        data={"chat_id": chat_id},
        files={"photo": image_bytes},
        timeout=60
    )
    r.raise_for_status()
