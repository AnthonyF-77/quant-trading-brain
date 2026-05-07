"""Chart generation module — Plotly-based interactive charts for quant analysis."""
import json
import math
import os
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

VAULT_PATH = Path(os.environ.get("OBSIDIAN_VAULT_PATH", str(Path(__file__).parent.parent.parent)))
CHART_DIR = VAULT_PATH / "sources" / "01_Markets" / "charts"
CHART_DIR.mkdir(parents=True, exist_ok=True)


def sma(prices: list, period: int) -> list:
    result = [None] * len(prices)
    for i in range(period - 1, len(prices)):
        result[i] = sum(prices[i - period + 1:i + 1]) / period
    return result


def ema(prices: list, period: int) -> list:
    result = [None] * len(prices)
    k = 2 / (period + 1)
    result[period - 1] = sum(prices[:period]) / period
    for i in range(period, len(prices)):
        result[i] = prices[i] * k + result[i - 1] * (1 - k)
    return result


def macd(prices: list, fast: int = 12, slow: int = 26, signal: int = 9):
    e_fast = ema(prices, fast)
    e_slow = ema(prices, slow)
    macd_line = [None] * len(prices)
    for i in range(slow - 1, len(prices)):
        if e_fast[i] is not None and e_slow[i] is not None:
            macd_line[i] = e_fast[i] - e_slow[i]
    signal_line = ema([x if x is not None else 0 for x in macd_line], signal)
    histogram = [None] * len(prices)
    for i in range(slow + signal - 2, len(prices)):
        if macd_line[i] is not None and signal_line[i] is not None:
            histogram[i] = macd_line[i] - signal_line[i]
    return macd_line, signal_line, histogram


def rsi(prices: list, period: int = 14) -> list:
    result = [None] * len(prices)
    gains, losses = [], []
    for i in range(1, len(prices)):
        delta = prices[i] - prices[i - 1]
        gains.append(max(delta, 0))
        losses.append(abs(min(delta, 0)))
    if len(gains) < period:
        return result
    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period
    for i in range(period, len(gains)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period
        if avg_loss == 0:
            result[i + 1] = 100
        else:
            rs = avg_gain / avg_loss
            result[i + 1] = 100 - (100 / (1 + rs))
    return result


def plot_candlestick_with_indicators(
    ticker: str,
    data: dict,
    title: str = "",
    save_png: bool = True,
    save_html: bool = True,
) -> dict:
    """Generate full technical analysis chart: candlestick + volume + MA + MACD + RSI."""
    prices = data.get("close") or data.get("price", [])
    if not prices or len(prices) < 30:
        return {"error": "Insufficient data"}

    dates = data.get("timestamps", [None] * len(prices))
    if isinstance(dates[0], str):
        try:
            parsed_dates = []
            for d in dates:
                try:
                    parsed_dates.append(datetime.fromisoformat(d.replace("Z", "+00:00").replace("+00:00", "")))
                except Exception:
                    parsed_dates.append(d)
            dates = parsed_dates
        except Exception:
            dates = list(range(len(prices)))
    else:
        dates = list(range(len(prices)))

    highs = data.get("high", prices)
    lows = data.get("low", prices)
    opens = data.get("open", prices)
    volumes = data.get("volume_list", [1] * len(prices))
    current_price = data.get("current_price", prices[-1])

    ma5 = sma(prices, 5)
    ma10 = sma(prices, 10)
    ma20 = sma(prices, 20)
    ma50 = sma(prices, 50)
    ma200 = sma(prices, 200) if len(prices) >= 200 else [None] * len(prices)

    macd_line, signal_line, histogram = macd(prices)
    rsi_vals = rsi(prices, 14)

    # Determine chart title
    if not title:
        title = f"{ticker} — Technical Analysis ({datetime.now().strftime('%Y-%m-%d')})"

    fig = make_subplots(
        rows=4, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.04,
        row_heights=[0.5, 0.15, 0.2, 0.15],
        subplot_titles=("", "Volume", "MACD", "RSI(14)"),
    )

    # 1. Candlestick chart
    fig.add_trace(
        go.Candlestick(
            x=list(range(len(dates))),
            open=opens, high=highs, low=lows, close=prices,
            name="Price",
            increasing_line_color="#26a69a",
            decreasing_line_color="#ef5350",
        ),
        row=1, col=1,
    )

    # Moving averages
    ma_configs = [
        (ma5, "#FF6B6B", "MA5"),
        (ma10, "#4ECDC4", "MA10"),
        (ma20, "#45B7D1", "MA20"),
        (ma50, "#96CEB4", "MA50"),
        (ma200, "#FFEAA7", "MA200"),
    ]
    for ma, color, name in ma_configs:
        fig.add_trace(
            go.Scatter(
                x=list(range(len(ma))),
                y=ma,
                mode="lines",
                name=name,
                line=dict(color=color, width=1.2),
                opacity=0.8,
            ),
            row=1, col=1,
        )

    # 2. Volume bars (colored by price direction)
    colors = ["#26a69a" if prices[i] >= opens[i] else "#ef5350" for i in range(len(prices))]
    fig.add_trace(
        go.Bar(
            x=list(range(len(volumes))),
            y=volumes,
            marker_color=colors,
            name="Volume",
            opacity=0.7,
        ),
        row=2, col=1,
    )

    # 3. MACD
    macd_colors = ["#26a69a" if h and h >= 0 else "#ef5350" for h in histogram]
    fig.add_trace(
        go.Bar(
            x=list(range(len(histogram))),
            y=[h if h else 0 for h in histogram],
            marker_color=macd_colors,
            name="MACD Hist",
            opacity=0.8,
        ),
        row=3, col=1,
    )
    fig.add_trace(
        go.Scatter(x=list(range(len(macd_line))), y=macd_line,
                   mode="lines", name="MACD", line=dict(color="#2196F3", width=1.5)),
        row=3, col=1,
    )
    fig.add_trace(
        go.Scatter(x=list(range(len(signal_line))), y=signal_line,
                   mode="lines", name="Signal", line=dict(color="#FF9800", width=1.2)),
        row=3, col=1,
    )

    # 4. RSI
    rsi_colors = ["#26a69a" if r and r < 50 else "#ef5350" for r in rsi_vals]
    fig.add_trace(
        go.Scatter(
            x=list(range(len(rsi_vals))),
            y=rsi_vals,
            mode="lines",
            name="RSI",
            line=dict(color="#9C27B0", width=1.5),
            fill='tozeroy',
            fillcolor='rgba(156,39,176,0.05)',
        ),
        row=4, col=1,
    )
    # RSI reference lines
    for h_line, color in [(70, "#ef5350"), (30, "#26a69a"), (50, "#666666")]:
        fig.add_hline(y=h_line, line_dash="dash", line_color=color,
                      opacity=0.5, row=4, col=1)

    # Layout
    fig.update_layout(
        title=dict(text=title, font=dict(size=16)),
        xaxis_rangeslider_visible=False,
        template="plotly_dark",
        height=900,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(t=60, b=40),
    )
    fig.update_xaxes(showgrid=True, gridcolor="rgba(255,255,255,0.05)", row=4, col=1)
    fig.update_yaxes(showgrid=True, gridcolor="rgba(255,255,255,0.05)")

    outputs = {}
    slug = ticker.replace("/", "_")

    if save_html:
        html_path = CHART_DIR / f"{slug}_candle.html"
        fig.write_html(str(html_path))
        outputs["html"] = str(html_path)

    if save_png:
        png_path = CHART_DIR / f"{slug}_candle.png"
        try:
            fig.write_image(str(png_path), width=1400, height=900, scale=2)
            outputs["png"] = str(png_path)
        except Exception as e:
            outputs["png_error"] = str(e)

    outputs["ticker"] = ticker
    outputs["chart_type"] = "candlestick_with_indicators"
    return outputs


def plot_multi_asset_comparison(
    tickers_data: list[dict],
    title: str = "Normalized Price Comparison",
    save_png: bool = True,
    save_html: bool = True,
) -> dict:
    """Plot multiple assets normalized to 100 for comparison."""
    fig = go.Figure()

    colors = ["#26a69a", "#ef5350", "#2196F3", "#FF9800", "#9C27B0",
              "#4ECDC4", "#FFEAA7", "#96CEB4", "#FF6B6B", "#45B7D1"]

    for i, item in enumerate(tickers_data):
        ticker = item["ticker"]
        prices = item.get("close") or item.get("price", [])
        if not prices:
            continue
        normalized = [p / prices[0] * 100 for p in prices]
        color = colors[i % len(colors)]

        fig.add_trace(go.Scatter(
            x=list(range(len(normalized))),
            y=normalized,
            mode="lines",
            name=ticker,
            line=dict(color=color, width=2),
        ))

    fig.add_hline(y=100, line_dash="dash", line_color="rgba(255,255,255,0.3)")
    fig.update_layout(
        title=dict(text=title, font=dict(size=16)),
        template="plotly_dark",
        height=500,
        xaxis_title="Trading Days",
        yaxis_title="Normalized Price (Day 1 = 100)",
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        margin=dict(t=60, b=40),
    )
    fig.update_xaxes(showgrid=True, gridcolor="rgba(255,255,255,0.05)")
    fig.update_yaxes(showgrid=True, gridcolor="rgba(255,255,255,0.05)")

    outputs = {}
    slug = "_".join(item["ticker"].replace("/", "_") for item in tickers_data[:3]) + "_compare"
    if save_html:
        html_path = CHART_DIR / f"{slug}.html"
        fig.write_html(str(html_path))
        outputs["html"] = str(html_path)
    if save_png:
        png_path = CHART_DIR / f"{slug}.png"
        try:
            fig.write_image(str(png_path), width=1400, height=500, scale=2)
            outputs["png"] = str(png_path)
        except Exception as e:
            outputs["png_error"] = str(e)

    outputs["chart_type"] = "multi_asset_comparison"
    return outputs


def plot_factor_comparison(
    results: list[dict],
    factor: str = "volatility_20d",
    title: str = "",
    save_png: bool = True,
    save_html: bool = True,
) -> dict:
    """Plot factor comparison across multiple tickers as horizontal bar chart."""
    valid = [(r["ticker"], r.get("factors", {}).get(factor, 0)) for r in results if r.get("factors", {}).get(factor)]
    if not valid:
        return {"error": f"No data for factor: {factor}"}

    valid.sort(key=lambda x: x[1], reverse=True)
    tickers = [v[0] for v in valid]
    values = [v[1] for v in valid]

    colors = ["#26a69a" if v > 0 else "#ef5350" for v in values]

    fig = go.Figure(go.Bar(
        x=tickers,
        y=values,
        marker_color=colors,
        text=[f"{v:.1f}" for v in values],
        textposition="outside",
    ))
    fig.update_layout(
        title=dict(text=title or f"Factor Comparison: {factor}", font=dict(size=16)),
        template="plotly_dark",
        height=400,
        showlegend=False,
        margin=dict(t=60, b=60),
        yaxis_title=factor,
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridcolor="rgba(255,255,255,0.05)")

    outputs = {}
    slug = f"factor_{factor}"
    if save_html:
        html_path = CHART_DIR / f"{slug}.html"
        fig.write_html(str(html_path))
        outputs["html"] = str(html_path)
    if save_png:
        png_path = CHART_DIR / f"{slug}.png"
        try:
            fig.write_image(str(png_path), width=1200, height=400, scale=2)
            outputs["png"] = str(png_path)
        except Exception as e:
            outputs["png_error"] = str(e)

    outputs["chart_type"] = "factor_comparison"
    outputs["factor"] = factor
    return outputs


def plot_momentum_chart(
    results: list[dict],
    save_png: bool = True,
    save_html: bool = True,
) -> dict:
    """Plot 20d vs 60d momentum scatter for multiple tickers."""
    data20 = [(r["ticker"], r.get("factors", {}).get("momentum_20d", 0)) for r in results]
    data60 = {r["ticker"]: r.get("factors", {}).get("momentum_60d", 0) for r in results}

    tickers = [d[0] for d in data20 if d[1] is not None]
    mom20 = [d[1] for d in data20 if d[1] is not None]
    mom60 = [data60.get(t, 0) for t in tickers]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=mom20,
        y=mom60,
        mode="markers+text",
        text=tickers,
        textposition="top center",
        marker=dict(size=12, color=mom20, colorscale="RdYlGn", showscale=True),
    ))
    fig.add_vline(x=0, line_dash="dash", line_color="rgba(255,255,255,0.3)")
    fig.add_hline(y=0, line_dash="dash", line_color="rgba(255,255,255,0.3)")

    fig.update_layout(
        title=dict(text="20-Day vs 60-Day Momentum Scatter", font=dict(size=16)),
        template="plotly_dark",
        height=500,
        xaxis_title="20-Day Momentum (%)",
        yaxis_title="60-Day Momentum (%)",
        showlegend=False,
        margin=dict(t=60, b=60),
    )
    fig.update_xaxes(showgrid=True, gridcolor="rgba(255,255,255,0.05)")
    fig.update_yaxes(showgrid=True, gridcolor="rgba(255,255,255,0.05)")

    outputs = {}
    if save_html:
        html_path = CHART_DIR / "momentum_scatter.html"
        fig.write_html(str(html_path))
        outputs["html"] = str(html_path)
    if save_png:
        png_path = CHART_DIR / "momentum_scatter.png"
        try:
            fig.write_image(str(png_path), width=1000, height=500, scale=2)
            outputs["png"] = str(png_path)
        except Exception as e:
            outputs["png_error"] = str(e)

    outputs["chart_type"] = "momentum_scatter"
    return outputs


if __name__ == "__main__":
    import sys, argparse
    parser = argparse.ArgumentParser(description="Generate charts")
    parser.add_argument("--chart", choices=["candle", "compare", "factor", "momentum"], required=True)
    parser.add_argument("--ticker", help="Ticker for candle chart")
    parser.add_argument("--factor", default="volatility_20d", help="Factor name for factor chart")
    parser.add_argument("--output-dir", default=None)
    args = parser.parse_args()

    if args.output_dir:
        CHART_DIR = Path(args.output_dir)
        CHART_DIR.mkdir(parents=True, exist_ok=True)

    if args.chart == "candle":
        import json as _json
        data = _json.loads(sys.stdin.read())
        ticker = args.ticker or data.get("ticker", "UNKNOWN")
        result = plot_candlestick_with_indicators(ticker, data)
        print(_json.dumps(result, indent=2, default=str))
    elif args.chart == "compare":
        import json as _json
        data = _json.loads(sys.stdin.read())
        result = plot_multi_asset_comparison(data)
        print(_json.dumps(result, indent=2, default=str))
    elif args.chart == "factor":
        import json as _json
        data = _json.loads(sys.stdin.read())
        result = plot_factor_comparison(data, factor=args.factor)
        print(_json.dumps(result, indent=2, default=str))
    elif args.chart == "momentum":
        import json as _json
        data = _json.loads(sys.stdin.read())
        result = plot_momentum_chart(data)
        print(_json.dumps(result, indent=2, default=str))
