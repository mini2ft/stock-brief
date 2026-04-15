# telegram_sender.py - 텔레그램 메시지 전송
# 로컬: .env 파일에서 읽음 / GitHub Actions: Repository Secrets에서 읽음

import os
import requests
from dotenv import load_dotenv

load_dotenv()  # 로컬에서는 .env 로드, Actions에서는 이미 env에 주입되어 있어 무해


def send_message(text: str) -> None:
    """텔레그램 봇으로 메시지 전송"""
    # TODO: Telegram Bot API 호출 (sendMessage)
    # TODO: 전송 실패 시 에러 로깅
    pass
