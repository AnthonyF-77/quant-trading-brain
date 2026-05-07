#!/usr/bin/env python3
"""
Usage:
  python3 quant-chart.py --chart candle --ticker AAPL       # Single ticker candlestick chart
  python3 quant-chart.py --chart candle --ticker 000001.SZ  # A-share
  python3 quant-chart.py --chart candle --ticker BTC/USDT   # Crypto
  python3 quant-chart.py --chart compare --tickers AAPL,MSFT,NVDA  # Multi-asset comparison
  python3 quant-chart.py --chart factor --factor volatility_20d          # Factor bar chart
  python3 quant-chart.py --chart momentum                               # Momentum scatter
"""
import sys, os, json
from pathlib import Path

vault = Path(__file__).parent
os.environ.setdefault("OBSIDIAN_VAULT_PATH", str(vault))
sys.path.insert(0, str(vault / "scraper"))

from market_data.fetch import fetch_us_stock, fetch_a_share, fetch_crypto
from analysis.charts import (
    plot_candlestick_with_indicators,
    plot_multi_asset_comparison,
    plot_factor_comparison,
    plot_momentum_chart,
)
from analysis.technical import analyze, compute_factors, score_against_research


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Quant Brain Charts")
    parser.add_argument("--chart", choices=["candle", "compare", "factor", "momentum"], required=True)
    parser.add_argument("--ticker", help="Ticker for candle chart")
    parser.add_argument("--tickers", help="Comma-separated tickers for compare chart")
    parser.add_argument("--factor", default="volatility_20d",
                        help="Factor for factor chart (volatility_20d, momentum_20d, momentum_60d, sharpe_approx)")
    parser.add_argument("--market", default="us", choices=["us", "a-share", "crypto"])
    parser.add_argument("--period", default="3mo")
    parser.add_argument("--results-json", help="Path to scan results JSON to derive tickers")
    parser.add_argument("--output-dir", help="Override chart output directory")
    args = parser.parse_args()

    if args.output_dir:
        from analysis import charts as ch
        ch.CHART_DIR = Path(args.output_dir)
        ch.CHART_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Generating {args.chart} chart...")

    if args.chart == "candle":
        ticker = args.ticker
        if not ticker:
            print("Error: --ticker required for candle chart")
            sys.exit(1)

        if args.market == "us" or "/" not in ticker:
            data = fetch_us_stock(ticker, args.period)
        elif args.market == "a-share":
            data = fetch_a_share(ticker, args.period)
        else:
            data = fetch_crypto(ticker, period=args.period)

        if not data or "error" in data:
            print(f"Failed to fetch {ticker}: {data.get('error') if data else 'no data'}")
            sys.exit(1)

        result = plot_candlestick_with_indicators(ticker, data)
        print(json.dumps(result, indent=2, default=str))

    elif args.chart == "compare":
        if args.results_json:
            with open(args.results_json) as f:
                results = json.load(f)
            tickers_list = [(r["ticker"], r.get("market", "US")) for r in results.get("all_results", results)[:10]]
        elif args.tickers:
            tickers_list = [(t.strip(), "US") for t in args.tickers.split(",")]
        else:
            print("Error: --tickers or --results-json required")
            sys.exit(1)

        all_data = []
        for ticker, market in tickers_list:
            if market == "A-share" or ticker.startswith(("6", "0")):
                d = fetch_a_share(ticker, args.period)
            elif "/" in ticker:
                d = fetch_crypto(ticker, period=args.period)
            else:
                d = fetch_us_stock(ticker, args.period)
            if d and "error" not in d:
                all_data.append(d)
        if not all_data:
            print("No data fetched")
            sys.exit(1)

        result = plot_multi_asset_comparison(all_data)
        print(json.dumps(result, indent=2, default=str))

    elif args.chart == "factor":
        if args.results_json:
            with open(args.results_json) as f:
                results = json.load(f)
            scan_results = results.get("all_results", results) if isinstance(results, dict) else results
        else:
            print("Error: --results-json required for factor chart")
            sys.exit(1)

        ta_results = []
        for r in scan_results:
            ticker = r["ticker"]
            if "A-share" in r.get("market", "") or ticker.startswith(("6", "0", "8")):
                d = fetch_a_share(ticker, args.period)
            elif "/" in ticker:
                d = fetch_crypto(ticker, period=args.period)
            else:
                d = fetch_us_stock(ticker, args.period)
            if d and "error" not in d:
                ta = analyze(ticker, d)
                factors = compute_factors(d)
                ta["factors"] = factors
                ta_results.append(ta)

        if not ta_results:
            print("No data fetched")
            sys.exit(1)

        result = plot_factor_comparison(ta_results, factor=args.factor,
                                        title=f"Factor Comparison: {args.factor}")
        print(json.dumps(result, indent=2, default=str))

    elif args.chart == "momentum":
        if args.results_json:
            with open(args.results_json) as f:
                results = json.load(f)
            scan_results = results.get("all_results", results) if isinstance(results, dict) else results
        else:
            print("Error: --results-json required for momentum chart")
            sys.exit(1)

        ta_results = []
        for r in scan_results:
            ticker = r["ticker"]
            if "A-share" in r.get("market", "") or ticker.startswith(("6", "0", "8")):
                d = fetch_a_share(ticker, args.period)
            elif "/" in ticker:
                d = fetch_crypto(ticker, period=args.period)
            else:
                d = fetch_us_stock(ticker, args.period)
            if d and "error" not in d:
                ta = analyze(ticker, d)
                factors = compute_factors(d)
                ta["factors"] = factors
                ta_results.append(ta)

        if not ta_results:
            print("No data fetched")
            sys.exit(1)

        result = plot_momentum_chart(ta_results)
        print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
