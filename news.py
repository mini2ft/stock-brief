# news.py - Google News RSS 수집 + 키워드 점수화

import feedparser

RSS_FEEDS = [
    "https://news.google.com/rss/search?q=미국증시&hl=ko&gl=KR&ceid=KR:ko",
    "https://news.google.com/rss/search?q=나스닥&hl=ko&gl=KR&ceid=KR:ko",
    "https://news.google.com/rss/search?q=연준+금리&hl=ko&gl=KR&ceid=KR:ko",
]

KEYWORDS_2 = ["연준", "금리", "나스닥", "다우", "S&P", "빅테크", "반도체"]
KEYWORDS_1 = ["증시", "주가", "환율", "인플레이션", "고용", "GDP"]

MAX_ARTICLES = 5


def _score(title: str) -> int:
    score = 0
    for kw in KEYWORDS_2:
        if kw in title:
            score += 2
    for kw in KEYWORDS_1:
        if kw in title:
            score += 1
    return score


def get_news_summary() -> str:
    seen_titles = set()
    articles = []  # (순서, 제목, 링크)

    order = 0
    for url in RSS_FEEDS:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            title = entry.get("title", "").strip()
            link  = entry.get("link", "").strip()
            if not title or not link or title in seen_titles:
                continue
            seen_titles.add(title)
            articles.append((order, title, link))
            order += 1

    if not articles:
        return "📰 오늘의 주요 뉴스\n뉴스를 불러오지 못했습니다."

    # 점수 내림차순, 동점이면 원래 순서(최신순) 유지
    scored = sorted(articles, key=lambda x: (-_score(x[1]), x[0]))
    top = scored[:MAX_ARTICLES]

    lines = ["📰 오늘의 주요 뉴스"]
    for i, (_, title, link) in enumerate(top, 1):
        lines.append(f"{i}. {title}\n   {link}")

    return "\n".join(lines)
