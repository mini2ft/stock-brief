# news.py - 경제 뉴스 수집 (RSS)

import feedparser

RSS_FEEDS = [
    "https://www.hankyung.com/feed/economy",
    "https://rss.donga.com/economy.xml",
]

MAX_ARTICLES = 5


def get_news_summary() -> str:
    articles = []

    for url in RSS_FEEDS:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            title = entry.get("title", "").strip()
            link  = entry.get("link", "").strip()
            if title and link:
                articles.append((title, link))
            if len(articles) >= MAX_ARTICLES:
                break
        if len(articles) >= MAX_ARTICLES:
            break

    if not articles:
        return "📰 오늘의 주요 뉴스\n뉴스를 불러오지 못했습니다."

    lines = ["📰 오늘의 주요 뉴스"]
    for i, (title, link) in enumerate(articles, 1):
        lines.append(f"{i}. {title}\n   {link}")

    return "\n".join(lines)
