#!/usr/bin/env python3
"""
Quant Trading Brain — Market Scanner
Scans US stocks, A-shares, and Crypto, ranks by factors, outputs actionable analysis.
"""
import json
import sys
import os
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).parent.parent))

from market_data.fetch import fetch_us_stock, fetch_a_share, fetch_crypto
from analysis.technical import analyze, compute_factors, score_against_research

UNIVERSE = {
    "us_etf": ["SPY", "QQQ", "IWM", "DIA", "XLE", "XLF", "XLK", "XLV", "XLY",
                "TLT", "HYG", "LQD", "BND", "GLD", "EEM"],
    "us_stock": ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA", "AMD", "INTC", "JPM", "GS", "BAC",
                  "V", "MA", "PYPL", "COIN", "SQ", "HOOD"],
    "a_share": ["000001.SZ", "000002.SZ", "000333.SZ", "000858.SZ",
                 "600036.SH", "600519.SH", "600887.SH", "601318.SH",
                 "601398.SH", "603259.SH", "688041.SH", "688981.SH"],
    "crypto": ["BTC/USDT", "ETH/USDT", "SOL/USDT", "BNB/USDT", "XRP/USDT",
               "DOGE/USDT", "ADA/USDT", "AVAX/USDT", "DOT/USDT", "LINK/USDT"],
}


def scan_universe(tickers: list[tuple], max_items: int = 10) -> list[dict]:
    """Scan a list of tickers, return scored results."""
    results = []
    for ticker, market, source_fn, extra in tickers:
        try:
            data = source_fn(ticker, **extra)
            if not data or "error" in data:
                continue
            ta = analyze(ticker, data)
            factors = compute_factors(data)
            research = score_against_research(ticker, ta, factors)
            ta["factors"] = factors
            ta["research_enhanced"] = research
            results.append(ta)
        except Exception as e:
            print(f"  Error {ticker}: {e}", file=sys.stderr)
    return sorted(results, key=lambda x: x.get("score", 0), reverse=True)[:max_items]


def build_report(market: str, results: list[dict], top_n: int = 5) -> dict:
    if not results:
        return {"market": market, "error": "No data"}

    strong_buys = [r for r in results if r["overall_signal"] == "STRONG_BUY"]
    buys = [r for r in results if r["overall_signal"] == "BUY"]
    sells = [r for r in results if r["overall_signal"] == "SELL"]
    strong_sells = [r for r in results if r["overall_signal"] == "STRONG_SELL"]
    neutrals = [r for r in results if r["overall_signal"] == "NEUTRAL"]

    top_buys = strong_buys[:top_n] if strong_buys else buys[:top_n]

    report = {
        "market": market,
        "scanned_count": len(results),
        "summary": {
            "strong_buy_count": len(strong_buys),
            "buy_count": len(buys),
            "neutral_count": len(neutrals),
            "sell_count": len(sells),
            "strong_sell_count": len(strong_sells),
        },
        "top_picks": [
            {
                "ticker": r["ticker"],
                "signal": r["overall_signal"],
                "score": r["score"],
                "price": r["current_price"],
                "interpretation": r["interpretation"],
                "key_signals": [s["description"] for s in r["signals"][:3]],
                "factors": {k: v for k, v in r.get("factors", {}).items() if v is not None},
            }
            for r in top_buys
        ],
        "all_results": [
            {
                "ticker": r["ticker"],
                "signal": r["overall_signal"],
                "score": r["score"],
                "price": r["current_price"],
                "indicators": r.get("indicators", {}),
            }
            for r in results
        ],
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    return report


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Quant Trading Brain Scanner")
    parser.add_argument("--market", choices=["us", "a-share", "crypto", "all"], default="all")
    parser.add_argument("--top", type=int, default=5, help="Top N picks to show")
    parser.add_argument("--output", choices=["json", "text"], default="text")
    args = parser.parse_args()

    tickers_to_scan = []

    if args.market in ("us", "all"):
        tickers_to_scan += [(t, "US", fetch_us_stock, {"period": "3mo"}) for t in UNIVERSE["us_etf"] + UNIVERSE["us_stock"]]

    if args.market in ("a-share", "all"):
        tickers_to_scan += [(t, "A-share", fetch_a_share, {"period": "3mo"}) for t in UNIVERSE["a_share"]]

    if args.market in ("crypto", "all"):
        tickers_to_scan += [(t, "Crypto", fetch_crypto, {"period": "3mo"}) for t in UNIVERSE["crypto"]]

    print(f"Scanning {len(tickers_to_scan)} assets...", file=sys.stderr)
    results = scan_universe(tickers_to_scan, max_items=30)

    if args.market == "all":
        for market_name, market_results in [
            ("US", [r for r in results if r.get("market") == "US"]),
            ("A-Share", [r for r in results if r.get("market") == "A-share"]),
            ("Crypto", [r for r in results if r.get("market") == "Crypto"]),
        ]:
            if not market_results:
                continue
            report = build_report(market_name, market_results, top_n=args.top)
            if args.output == "json":
                print(json.dumps(report, indent=2, default=str))
            else:
                print_report(report)
    else:
        market_map = {"us": "US", "a-share": "A-Share", "crypto": "Crypto"}
        report = build_report(market_map.get(args.market, args.market), results, top_n=args.top)
        if args.output == "json":
            print(json.dumps(report, indent=2, default=str))
        else:
            print_report(report)


def print_report(report: dict):
    print(f"\n{'='*60}")
    print(f"  {report['market']} 市场扫描报告 — {report['timestamp'][:10]}")
    print(f"{'='*60}")
    print(f"扫描数量: {report['scanned_count']}")
    s = report["summary"]
    print(f"信号分布: 强力买入={s['strong_buy_count']} | 买入={s['buy_count']} | 中性={s['neutral_count']} | 卖出={s['sell_count']} | 强力卖出={s['strong_sell_count']}")
    print(f"{'-'*60}")
    for pick in report.get("top_picks", []):
        print(f"\n  [{pick['signal']}] {pick['ticker']} @ ${pick['price']}")
        print(f"    综合评分: {pick['score']}")
        print(f"    解读: {pick['interpretation']}")
        for sig in pick.get("key_signals", []):
            print(f"    • {sig}")
        factors = pick.get("factors", {})
        if factors:
            factor_str = " | ".join(f"{k}={v}" for k, v in list(factors.items())[:4])
            print(f"    因子: {factor_str}")
    print(f"\n{'='*60}")


if __name__ == "__main__":
    main()
