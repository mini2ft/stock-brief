# telegram_sender.py - 텔레그램 메시지 전송
# 로컬: .env 파일에서 읽음 / GitHub Actions: Repository Secrets에서 읽음

import os
import requests
from dotenv import load_dotenv

load_dotenv()


def send_message(text: str) -> None:
    token   = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    res = requests.post(url, json={"chat_id": chat_id, "text": text})
    res.raise_for_status()
