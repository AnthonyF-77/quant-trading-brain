"""Unified market data fetcher — yfinance (US), akshare (A-share), CCXT (Crypto)."""
import os
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from pathlib import Path

VAULT_PATH = Path(os.environ.get("OBSIDIAN_VAULT_PATH", str(Path(__file__).parent.parent.parent)))


def fetch_us_stock(ticker: str, period: str = "3mo") -> dict | None:
    """Fetch US stock data via yfinance."""
    try:
        import yfinance as yf
        ticker_obj = yf.Ticker(ticker)
        hist = ticker_obj.history(period=period)
        info = ticker_obj.info
        if hist.empty:
            return None
        return {
            "ticker": ticker,
            "market": "US",
            "current_price": float(info.get("currentPrice") or info.get("regularMarketPrice") or hist["Close"].iloc[-1]),
            "previous_close": float(info.get("previousClose") or hist["Close"].iloc[-2]),
            "volume": int(hist["Volume"].iloc[-1]),
            "avg_volume_20d": float(hist["Volume"].rolling(20).mean().iloc[-1]),
            "high_52w": float(info.get("fiftyTwoWeekHigh", 0)),
            "low_52w": float(info.get("fiftyTwoWeekLow", 0)),
            "market_cap": info.get("marketCap"),
            "pe_ratio": info.get("trailingPE"),
            "dividend_yield": info.get("dividendYield"),
            "price": hist["Close"].tolist(),
            "volume_list": hist["Volume"].tolist(),
            "high": hist["High"].tolist(),
            "low": hist["Low"].tolist(),
            "open": hist["Open"].tolist(),
            "close": hist["Close"].tolist(),
            "timestamps": [str(t) for t in hist.index.tolist()],
            "sector": info.get("sector"),
            "industry": info.get("industry"),
            "beta": info.get("beta"),
            "source": "yfinance",
        }
    except Exception as e:
        return {"ticker": ticker, "market": "US", "error": str(e)}


def fetch_a_share(ticker: str, period: str = "3mo") -> dict | None:
    """Fetch A-share stock data via akshare."""
    try:
        import akshare as ak
        symbol = ticker.replace(".", "").replace("SH", "").replace("SZ", "")
        if not (symbol.startswith("6") or symbol.startswith("8") or symbol.startswith("9")):
            symbol = symbol.zfill(6)
        df = ak.stock_zh_a_hist(symbol=symbol, period="daily", adjust="qfq", start_date=(datetime.now().replace(month=datetime.now().month - 4)).strftime("%Y%m%d"))
        if df is None or df.empty:
            return None
        df = df.tail(90)
        return {
            "ticker": ticker,
            "market": "A-share",
            "current_price": float(df["收盘"].iloc[-1]),
            "previous_close": float(df["收盘"].iloc[-2]),
            "volume": int(df["成交量"].iloc[-1]),
            "price": df["收盘"].tolist(),
            "high": df["最高"].tolist(),
            "low": df["最低"].tolist(),
            "open": df["开盘"].tolist(),
            "close": df["收盘"].tolist(),
            "timestamps": df["日期"].tolist(),
            "source": "akshare",
        }
    except Exception as e:
        return {"ticker": ticker, "market": "A-share", "error": str(e)}


def fetch_crypto(symbol: str = "BTC/USDT", exchange: str = "binance", period: str = "3mo") -> dict | None:
    """Fetch crypto data via CCXT."""
    try:
        import ccxt
        exchange_id = exchange
        timeframe_map = {"1mo": "1M", "3mo": "1M", "1y": "1M", "7d": "1D", "1d": "1D"}
        tf = timeframe_map.get(period, "1D")
        exchange_class = getattr(ccxt, exchange_id)
        ex = exchange_class({"enableRateLimit": True})
        ohlcv = ex.fetch_ohlcv(symbol, tf, limit=90)
        if not ohlcv:
            return None
        closes = [x[4] for x in ohlcv]
        volumes = [x[5] for x in ohlcv]
        highs = [x[2] for x in ohlcv]
        lows = [x[3] for x in ohlcv]
        opens = [x[1] for x in ohlcv]
        return {
            "ticker": symbol,
            "market": "Crypto",
            "exchange": exchange,
            "current_price": closes[-1],
            "previous_close": closes[-2] if len(closes) > 1 else closes[-1],
            "volume_24h": volumes[-1],
            "price": closes,
            "high": highs,
            "low": lows,
            "open": opens,
            "close": closes,
            "volume_list": volumes,
            "timestamps": [datetime.fromtimestamp(x[0] / 1000, tz=timezone.utc).isoformat() for x in ohlcv],
            "source": "CCXT",
        }
    except Exception as e:
        return {"ticker": symbol, "market": "Crypto", "error": str(e)}


def screen_us_etf_universe() -> list[dict]:
    """Screen major US ETFs for technical signals."""
    tickers = [
        "SPY", "QQQ", "IWM", "DIA",
        "XLE", "XLF", "XLK", "XLV", "XLY", "XLP", "XLI", "XLB",
        "TLT", "HYG", "LQD", "BND",
        "GLD", "SLV", "USO",
        "EEM", "EWZ", "FXI",
    ]
    results = []
    for t in tickers:
        d = fetch_us_stock(t)
        if d and "error" not in d:
            results.append(d)
        time.sleep(0.3)
    return results


if __name__ == "__main__":
    import sys
    args = sys.argv[1:]

    if not args:
        print("Usage: python market_data.py <ticker> [market] [period]")
        print("Markets: us, a-share, crypto")
        print("Example: python market_data.py AAPL us 3mo")
        print("         python market_data.py 000001.SZ a-share 3mo")
        print("         python market_data.py BTC/USDT crypto 3mo")
        sys.exit(1)

    ticker = args[0]
    market = args[1] if len(args) > 1 else "us"
    period = args[2] if len(args) > 2 else "3mo"

    if market == "us":
        data = fetch_us_stock(ticker, period)
    elif market == "a-share":
        data = fetch_a_share(ticker, period)
    elif market == "crypto":
        data = fetch_crypto(ticker, period=period)
    else:
        print(f"Unknown market: {market}")
        sys.exit(1)

    if data:
        print(json.dumps(data, indent=2, ensure_ascii=False, default=str))
    else:
        print(f"Failed to fetch {ticker}")
        sys.exit(1)
