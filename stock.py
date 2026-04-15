# stock.py - 미국 증시 데이터 수집

import time
import requests
import pandas as pd
import yfinance as yf

# ── 관심 종목 (자유롭게 수정) ──────────────────────────────────────
WATCHLIST = ["AAPL", "TSLA", "NVDA", "AMZN", "MSFT"]

# ── 섹터 ETF ──────────────────────────────────────────────────────
SECTOR_ETFS = [
    ("QQQ",  "빅테크"),
    ("SOXX", "반도체"),
    ("XLE",  "에너지"),
    ("XLF",  "금융"),
    ("XLV",  "헬스케어"),
]

# ── 주요 지수 ─────────────────────────────────────────────────────
INDICES = [
    ("^DJI",  "다우존스"),
    ("^IXIC", "나스닥"),
    ("^GSPC", "S&P500"),
]

SP500_WIKI = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"


# ── 유틸 ─────────────────────────────────────────────────────────

def _emoji(change: float) -> str:
    return "📈" if change >= 0 else "📉"


def _sign(val: float) -> str:
    return "+" if val >= 0 else ""


def _batch_pct(tickers: list[str], retries: int = 3) -> dict[str, float]:
    """여러 티커를 한 번에 다운로드해 등락률 딕셔너리 반환"""
    for attempt in range(retries):
        try:
            data = yf.download(
                tickers, period="2d", group_by="ticker",
                auto_adjust=True, progress=False, threads=True,
            )
            result = {}
            for t in tickers:
                try:
                    close = data[(t, "Close")].dropna()
                    if len(close) < 2:
                        continue
                    pct = (close.iloc[-1] - close.iloc[-2]) / close.iloc[-2] * 100
                    result[t] = float(pct)
                except Exception:
                    pass
            if result:
                return result
        except Exception:
            pass
        if attempt < retries - 1:
            time.sleep(2)
    return {}


def _single_hist(ticker: str, retries: int = 3):
    for attempt in range(retries):
        try:
            hist = yf.Ticker(ticker).history(period="2d")
            if len(hist) >= 2:
                return hist
        except Exception:
            pass
        if attempt < retries - 1:
            time.sleep(2)
    return None


# ── 섹션 1: 주요 지수 ─────────────────────────────────────────────

def _section_indices() -> str:
    lines = ["📊 미국 증시 (전일 종가)"]
    for ticker, name in INDICES:
        hist = _single_hist(ticker)
        if hist is None:
            lines.append(f"  {name}: 데이터 없음")
            continue
        prev  = hist["Close"].iloc[-2]
        close = hist["Close"].iloc[-1]
        chg   = close - prev
        pct   = chg / prev * 100
        lines.append(
            f"{_emoji(chg)} {name}: {close:,.0f} "
            f"({_sign(chg)}{chg:,.0f} / {_sign(pct)}{pct:.2f}%)"
        )
    return "\n".join(lines)


# ── 섹션 2: S&P500 상위/하위 5개 ──────────────────────────────────

def _get_sp500_tickers() -> list[str]:
    r = requests.get(SP500_WIKI, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
    tbl = pd.read_html(r.text, flavor="lxml")[0]
    return tbl["Symbol"].str.replace(".", "-", regex=False).tolist()


def _section_movers() -> str:
    try:
        tickers = _get_sp500_tickers()
        pct_map = _batch_pct(tickers)
        if not pct_map:
            return "🏆 S&P500 등락 상위/하위\n  데이터 없음"

        ranked = sorted(pct_map.items(), key=lambda x: x[1], reverse=True)
        top5   = ranked[:5]
        bot5   = ranked[-5:][::-1]

        lines = ["🏆 S&P500 당일 등락"]
        lines.append("  ▲ 상승 TOP 5")
        for t, pct in top5:
            lines.append(f"    📈 {t}: {_sign(pct)}{pct:.2f}%")
        lines.append("  ▼ 하락 TOP 5")
        for t, pct in bot5:
            lines.append(f"    📉 {t}: {pct:.2f}%")
        return "\n".join(lines)
    except Exception as e:
        return f"🏆 S&P500 등락 상위/하위\n  불러오기 실패: {e}"


# ── 섹션 3: 관심 종목 ─────────────────────────────────────────────

def _section_watchlist() -> str:
    pct_map = _batch_pct(WATCHLIST)
    lines = ["👀 관심 종목"]

    for ticker in WATCHLIST:
        hist = _single_hist(ticker)
        if hist is None or ticker not in pct_map:
            lines.append(f"  {ticker}: 데이터 없음")
            continue
        prev  = hist["Close"].iloc[-2]
        close = hist["Close"].iloc[-1]
        chg   = close - prev
        pct   = pct_map[ticker]
        lines.append(
            f"  {_emoji(chg)} {ticker}: ${close:,.2f} "
            f"({_sign(chg)}{chg:.2f} / {_sign(pct)}{pct:.2f}%)"
        )
    return "\n".join(lines)


# ── 섹션 4: 섹터 ETF ──────────────────────────────────────────────

def _section_etfs() -> str:
    tickers = [t for t, _ in SECTOR_ETFS]
    pct_map = _batch_pct(tickers)
    lines = ["🗂 섹터 ETF 동향"]

    for ticker, name in SECTOR_ETFS:
        if ticker not in pct_map:
            lines.append(f"  {name}({ticker}): 데이터 없음")
            continue
        pct = pct_map[ticker]
        lines.append(f"  {_emoji(pct)} {name}({ticker}): {_sign(pct)}{pct:.2f}%")
    return "\n".join(lines)


# ── 메인 ─────────────────────────────────────────────────────────

def get_stock_summary() -> str:
    divider = "─" * 20
    sections = [
        _section_indices(),
        divider,
        _section_movers(),
        divider,
        _section_watchlist(),
        divider,
        _section_etfs(),
    ]
    return "\n".join(sections)
