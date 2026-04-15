# main.py - 메인 실행 파일
# 증시 데이터와 뉴스를 수집하여 텔레그램으로 전송

from stock import get_stock_summary
from news import get_news_summary
from telegram_sender import send_message


def main():
    # 1. 미국 증시 데이터 수집
    stock_report = get_stock_summary()

    # 2. 경제 뉴스 수집
    news_report = get_news_summary()

    # 3. 메시지 조합
    message = f"{stock_report}\n\n{news_report}"

    # 4. 텔레그램 전송
    send_message(message)


if __name__ == "__main__":
    main()
