# main.py - 메인 실행 파일

import random
from datetime import datetime

from stock import get_stock_summary
from news import get_news_summary
from telegram_sender import send_message

WEEKDAYS = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]

QUOTES = [
    "오늘도 작은 한 걸음이 큰 변화를 만듭니다. 꾸준함이 최고의 전략이에요.",
    "시장은 단기적으로 투표 기계지만, 장기적으로는 저울입니다. — 벤저민 그레이엄",
    "불확실한 날일수록 원칙이 빛납니다. 오늘도 흔들리지 마세요.",
    "감사한 마음으로 하루를 시작하면 좋은 것들이 보이기 시작합니다.",
    "어제보다 1%만 더 나아지면 됩니다. 오늘도 그걸로 충분해요.",
    "기회는 준비된 사람에게 옵니다. 오늘의 공부가 내일의 기회입니다.",
    "두려움이 클수록 기회도 큽니다. 용기 있게 오늘을 마주하세요.",
    "당신이 심는 씨앗이 무엇인지가 수확을 결정합니다.",
    "좋은 하루는 좋은 아침에서 시작됩니다. 오늘 하루도 멋지게!",
    "인내는 쓰지만 그 열매는 달다. — 장 자크 루소",
    "실패는 포기할 때만 실패입니다. 다시 일어서는 한 과정일 뿐이에요.",
    "오늘 할 수 있는 일에 최선을 다하면, 내일이 더 가벼워집니다.",
    "복리의 마법은 시간과 인내에서 나옵니다. 오늘도 묵묵히 나아가세요.",
    "작은 것에 감사하는 사람이 큰 것도 얻습니다.",
    "지금 이 순간에 집중하세요. 과거도 미래도 아닌, 오늘이 전부입니다.",
]


def build_message() -> str:
    now = datetime.now()
    date_str = f"{now.year}년 {now.month}월 {now.day}일 {WEEKDAYS[now.weekday()]}"
    quote = random.choice(QUOTES)

    stock = get_stock_summary()
    news  = get_news_summary()

    divider = "─" * 20

    return "\n".join([
        f"📅 {date_str} 굿모닝 🌅",
        divider,
        stock,
        divider,
        news,
        divider,
        f"💬 {quote}",
    ])


def main():
    message = build_message()
    send_message(message)


if __name__ == "__main__":
    main()
