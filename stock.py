# stock.py - 미국 증시 데이터 수집

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

# ── S&P500 주요 150개 (Wikipedia 매번 조회 대신 하드코딩) ──────────
# 시가총액 상위 + 섹터별 대표주 위주 — 변동성 큰 종목이 모버에 잘 잡힘
SP500_TICKERS = [
    # 빅테크
    "AAPL","MSFT","NVDA","AMZN","GOOGL","GOOG","META","TSLA","AVGO","ORCL",
    "ADBE","CRM","INTC","AMD","QCOM","TXN","NOW","SNOW","PANW","CRWD",
    # 금융
    "BRK-B","JPM","V","MA","BAC","WFC","GS","MS","AXP","BLK",
    "SCHW","C","USB","PNC","TFC","COF","ICE","CME","CB","MMC",
    # 헬스케어
    "LLY","UNH","JNJ","ABBV","MRK","TMO","ABT","DHR","AMGN","BMY",
    "GILD","ISRG","SYK","ELV","HUM","CVS","CI","BSX","VRTX","REGN",
    # 소비재/유통
    "WMT","HD","COST","MCD","NKE","SBUX","TGT","LOW","TJX","BKNG",
    "MAR","HLT","ABNB","EBAY","ETSY","ROST","DG","DLTR","YUM","CMG",
    # 에너지
    "XOM","CVX","COP","EOG","SLB","MPC","PSX","VLO","OXY","PXD",
    # 산업재
    "CAT","DE","BA","HON","UNP","RTX","LMT","GE","MMM","EMR",
    "ETN","PH","ROK","ITW","GD","NOC","HII","TDG","CARR","OTIS",
    # 통신/미디어
    "NFLX","DIS","CMCSA","T","VZ","TMUS","WBD","PARA","EA","TTWO",
    # 유틸리티/부동산
    "NEE","DUK","SO","D","AEP","EXC","PLD","AMT","EQIX","CCI",
    # 기타 성장주
    "UBER","LYFT","ABNB","DASH","COIN","HOOD","DDOG","SNOW","MDB","ZS",
    "GTLB","BILL","HUBS","TTD","APP","RBLX","U","MELI","SE","GRAB",
]


# ── 티커 → 회사명 매핑 ────────────────────────────────────────────
COMPANY_NAMES = {
    # 빅테크
    "AAPL": "Apple", "MSFT": "Microsoft", "NVDA": "Nvidia", "AMZN": "Amazon",
    "GOOGL": "Alphabet", "GOOG": "Alphabet", "META": "Meta", "TSLA": "Tesla",
    "AVGO": "Broadcom", "ORCL": "Oracle", "ADBE": "Adobe", "CRM": "Salesforce",
    "INTC": "Intel", "AMD": "AMD", "QCOM": "Qualcomm", "TXN": "Texas Instruments",
    "NOW": "ServiceNow", "SNOW": "Snowflake", "PANW": "Palo Alto", "CRWD": "CrowdStrike",
    # 금융
    "BRK-B": "Berkshire", "JPM": "JPMorgan", "V": "Visa", "MA": "Mastercard",
    "BAC": "Bank of America", "WFC": "Wells Fargo", "GS": "Goldman Sachs",
    "MS": "Morgan Stanley", "AXP": "Amex", "BLK": "BlackRock",
    "SCHW": "Schwab", "C": "Citigroup", "USB": "US Bancorp", "PNC": "PNC",
    "TFC": "Truist", "COF": "Capital One", "ICE": "ICE", "CME": "CME Group",
    "CB": "Chubb", "MMC": "Marsh McLennan",
    # 헬스케어
    "LLY": "Eli Lilly", "UNH": "UnitedHealth", "JNJ": "J&J", "ABBV": "AbbVie",
    "MRK": "Merck", "TMO": "Thermo Fisher", "ABT": "Abbott", "DHR": "Danaher",
    "AMGN": "Amgen", "BMY": "Bristol-Myers", "GILD": "Gilead", "ISRG": "Intuitive",
    "SYK": "Stryker", "ELV": "Elevance", "HUM": "Humana", "CVS": "CVS Health",
    "CI": "Cigna", "BSX": "Boston Scientific", "VRTX": "Vertex", "REGN": "Regeneron",
    # 소비재/유통
    "WMT": "Walmart", "HD": "Home Depot", "COST": "Costco", "MCD": "McDonald's",
    "NKE": "Nike", "SBUX": "Starbucks", "TGT": "Target", "LOW": "Lowe's",
    "TJX": "TJX", "BKNG": "Booking", "MAR": "Marriott", "HLT": "Hilton",
    "ABNB": "Airbnb", "EBAY": "eBay", "ETSY": "Etsy", "ROST": "Ross Stores",
    "DG": "Dollar General", "DLTR": "Dollar Tree", "YUM": "Yum Brands", "CMG": "Chipotle",
    # 에너지
    "XOM": "ExxonMobil", "CVX": "Chevron", "COP": "ConocoPhillips", "EOG": "EOG Resources",
    "SLB": "SLB", "MPC": "Marathon Pete.", "PSX": "Phillips 66",
    "VLO": "Valero", "OXY": "Occidental", "PXD": "Pioneer Natural",
    # 산업재
    "CAT": "Caterpillar", "DE": "John Deere", "BA": "Boeing", "HON": "Honeywell",
    "UNP": "Union Pacific", "RTX": "RTX", "LMT": "Lockheed", "GE": "GE",
    "MMM": "3M", "EMR": "Emerson", "ETN": "Eaton", "PH": "Parker Hannifin",
    "ROK": "Rockwell", "ITW": "Illinois Tool", "GD": "General Dynamics",
    "NOC": "Northrop", "HII": "Huntington", "TDG": "TransDigm",
    "CARR": "Carrier", "OTIS": "Otis",
    # 통신/미디어
    "NFLX": "Netflix", "DIS": "Disney", "CMCSA": "Comcast", "T": "AT&T",
    "VZ": "Verizon", "TMUS": "T-Mobile", "WBD": "Warner Bros.", "PARA": "Paramount",
    "EA": "EA", "TTWO": "Take-Two",
    # 유틸리티/부동산
    "NEE": "NextEra", "DUK": "Duke Energy", "SO": "Southern Co.", "D": "Dominion",
    "AEP": "AEP", "EXC": "Exelon", "PLD": "Prologis", "AMT": "American Tower",
    "EQIX": "Equinix", "CCI": "Crown Castle",
    # 기타 성장주
    "UBER": "Uber", "LYFT": "Lyft", "DASH": "DoorDash", "COIN": "Coinbase",
    "HOOD": "Robinhood", "DDOG": "Datadog", "MDB": "MongoDB", "ZS": "Zscaler",
    "GTLB": "GitLab", "BILL": "Bill.com", "HUBS": "HubSpot", "TTD": "Trade Desk",
    "APP": "AppLovin", "RBLX": "Roblox", "U": "Unity", "MELI": "MercadoLibre",
    "SE": "Sea Ltd.", "GRAB": "Grab",
}


def _company(ticker: str) -> str:
    """티커에 해당하는 회사명 반환. 없으면 빈 문자열."""
    return COMPANY_NAMES.get(ticker, "")


# ── 유틸 ─────────────────────────────────────────────────────────

def _emoji(change: float) -> str:
    return "📈" if change >= 0 else "📉"


def _sign(val: float) -> str:
    return "+" if val >= 0 else ""


def _batch_pct(tickers: list[str]) -> dict[str, float]:
    """여러 티커를 한 번에 다운로드해 등락률 딕셔너리 반환"""
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
        return result
    except Exception:
        return {}


def _single_hist(ticker: str, retries: int = 3):
    for attempt in range(retries):
        try:
            hist = yf.Ticker(ticker).history(period="2d")
            if len(hist) >= 2:
                return hist
        except Exception:
            pass
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

def _section_movers() -> str:
    try:
        pct_map = _batch_pct(SP500_TICKERS)
        if not pct_map:
            return "🏆 S&P500 등락 상위/하위\n  데이터 없음"

        ranked = sorted(pct_map.items(), key=lambda x: x[1], reverse=True)
        top5   = ranked[:5]
        bot5   = ranked[-5:][::-1]

        lines = ["🏆 S&P500 당일 등락"]
        lines.append("  ▲ 상승 TOP 5")
        for t, pct in top5:
            name = _company(t)
            label = f"{t} ({name})" if name else t
            lines.append(f"    📈 {label}: {_sign(pct)}{pct:.2f}%")
        lines.append("  ▼ 하락 TOP 5")
        for t, pct in bot5:
            name = _company(t)
            label = f"{t} ({name})" if name else t
            lines.append(f"    📉 {label}: {pct:.2f}%")
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
