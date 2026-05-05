"""Technical analysis engine — indicators, signals, and scoring."""
import json
import math
from datetime import datetime, timezone
from pathlib import Path

import numpy as np


def sma(prices: list[float], period: int) -> list[float | None]:
    result = [None] * len(prices)
    for i in range(period - 1, len(prices)):
        result[i] = sum(prices[i - period + 1:i + 1]) / period
    return result


def ema(prices: list[float], period: int) -> list[float | None]:
    result = [None] * len(prices)
    k = 2 / (period + 1)
    window_sum = sum(prices[:period])
    result[period - 1] = window_sum / period
    for i in range(period, len(prices)):
        result[i] = prices[i] * k + result[i - 1] * (1 - k)
    return result


def macd(prices: list[float], fast: int = 12, slow: int = 26, signal: int = 9):
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


def rsi(prices: list[float], period: int = 14) -> list[float | None]:
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


def bollinger_bands(prices: list[float], period: int = 20, num_std: float = 2.0):
    mid = sma(prices, period)
    upper = [None] * len(prices)
    lower = [None] * len(prices)
    for i in range(period - 1, len(prices)):
        if mid[i] is not None:
            slice_prices = prices[i - period + 1:i + 1]
            std = math.sqrt(sum((p - mid[i]) ** 2 for p in slice_prices) / period)
            upper[i] = mid[i] + num_std * std
            lower[i] = mid[i] - num_std * std
    return upper, mid, lower


def atr(highs: list[float], lows: list[float], closes: list[float], period: int = 14) -> list[float | None]:
    tr = [None] * len(highs)
    for i in range(1, len(highs)):
        hl = highs[i] - lows[i]
        hc = abs(highs[i] - closes[i - 1])
        lc = abs(lows[i] - closes[i - 1])
        tr[i] = max(hl, hc, lc)
    result = [None] * len(tr)
    if len(tr) <= period:
        return result
    result[period - 1] = sum(tr[1:period]) / period
    for i in range(period, len(tr)):
        if result[i - 1] is not None:
            result[i] = (result[i - 1] * (period - 1) + tr[i]) / period
    return result


def volume_profile(prices: list[float], volumes: list[float], bins: int = 20) -> dict:
    if not prices or len(prices) != len(volumes):
        return {}
    min_p, max_p = min(prices), max(prices)
    if min_p == max_p:
        return {"poc_price": prices[-1], "volume_by_price": {}}
    bucket_size = (max_p - min_p) / bins
    buckets = [0.0] * bins
    for p, v in zip(prices, volumes):
        idx = min(int((p - min_p) / bucket_size), bins - 1)
        buckets[idx] += v
    max_bucket_idx = max(range(bins), key=lambda i: buckets[i])
    poc_price = min_p + (max_bucket_idx + 0.5) * bucket_size
    return {
        "poc_price": round(poc_price, 2),
        "max_volume": round(buckets[max_bucket_idx], 0),
    }


def momentum(prices: list[float], period: int = 20) -> list[float | None]:
    result = [None] * len(prices)
    for i in range(period, len(prices)):
        if prices[i - period] != 0:
            result[i] = (prices[i] - prices[i - period]) / prices[i - period] * 100
    return result


def analyze(ticker: str, data: dict) -> dict:
    """Run full technical analysis on market data."""
    prices = data.get("close") or data.get("price", [])
    if not prices or len(prices) < 30:
        return {"ticker": ticker, "error": "Insufficient data", "data": data}

    highs = data.get("high", prices)
    lows = data.get("low", prices)
    volumes = data.get("volume_list", [])
    current_price = data.get("current_price", prices[-1])

    ma5 = sma(prices, 5)
    ma10 = sma(prices, 10)
    ma20 = sma(prices, 20)
    ma50 = sma(prices, 50)
    ma200 = sma(prices, 200) if len(prices) >= 200 else [None] * len(prices)

    ema12 = ema(prices, 12)
    ema26 = ema(prices, 26)
    macd_line, signal_line, histogram = macd(prices)
    rsi_val = rsi(prices, 14)
    bb_upper, bb_mid, bb_lower = bollinger_bands(prices)
    atr_val = atr(highs, lows, prices, 14)
    mom20 = momentum(prices, 20)
    mom60 = momentum(prices, 60) if len(prices) >= 60 else [None] * len(prices)

    vol_profile = volume_profile(prices[-30:], volumes[-30:]) if volumes else {}

    last_ma20 = ma20[-1] if ma20 else None
    last_ma50 = ma50[-1] if ma50 else None
    last_ma200 = ma200[-1] if ma200 else None
    last_rsi = rsi_val[-1] if rsi_val else None
    last_macd = macd_line[-1] if macd_line else None
    last_signal = signal_line[-1] if signal_line else None
    last_mom = mom20[-1] if mom20 else None
    last_mom60 = mom60[-1] if mom60 else None
    last_bb_upper = bb_upper[-1] if bb_upper else None
    last_bb_lower = bb_lower[-1] if bb_lower else None

    signals = []
    score = 0

    # Trend signals
    if last_ma20 and last_ma50 and last_ma200:
        if last_ma20 > last_ma50 > last_ma200:
            signals.append(("strong_uptrend", "bullish", "MA20>MA50>MA200上升排列"))
            score += 2
        elif last_ma20 < last_ma50 < last_ma200:
            signals.append(("strong_downtrend", "bearish", "MA20<MA50<MA200下降排列"))
            score -= 2
        elif last_ma20 > last_ma50:
            signals.append(("mild_uptrend", "bullish", "MA20>MA50"))
            score += 1
        elif last_ma20 < last_ma50:
            signals.append(("mild_downtrend", "bearish", "MA20<MA50"))
            score -= 1

    # MACD signals
    if last_macd and last_signal:
        if last_macd > last_signal > 0:
            signals.append(("macd_bullish_cross", "bullish", "MACD在零轴上方金叉"))
            score += 1
        elif last_macd < last_signal < 0:
            signals.append(("macd_bearish_cross", "bearish", "MACD在零轴下方死叉"))
            score -= 1
        elif histogram and histogram[-1] and histogram[-1] > 0 and histogram[-2] and histogram[-2] < 0:
            signals.append(("macd_histogram_golden", "bullish", "MACD柱状图黄金交叉"))
            score += 1
        elif histogram and histogram[-1] and histogram[-1] < 0 and histogram[-2] and histogram[-2] > 0:
            signals.append(("macd_histogram_death", "bearish", "MACD柱状图死叉"))
            score -= 1

    # RSI signals
    if last_rsi:
        if last_rsi > 80:
            signals.append(("rsi_overbought", "bearish", f"RSI超买={last_rsi:.1f}"))
            score -= 1
        elif last_rsi < 20:
            signals.append(("rsi_oversold", "bullish", f"RSI超卖={last_rsi:.1f}"))
            score += 1
        elif last_rsi > 60:
            signals.append(("rsi_bullish_zone", "bullish", f"RSI强势区={last_rsi:.1f}"))
            score += 1
        elif last_rsi < 40:
            signals.append(("rsi_bearish_zone", "bearish", f"RSI弱势区={last_rsi:.1f}"))
            score -= 1

    # Bollinger Bands signals
    if last_bb_upper and last_bb_lower and last_bb_upper != last_bb_lower:
        band_width = last_bb_upper - last_bb_lower
        position = (current_price - last_bb_lower) / band_width if band_width > 0 else 0.5
        if position > 0.95:
            signals.append(("bb_upper_touch", "bearish", "触及布林带上轨"))
            score -= 1
        elif position < 0.05:
            signals.append(("bb_lower_touch", "bullish", "触及布林带下轨"))
            score += 1

    # Momentum signals
    if last_mom:
        if last_mom > 10:
            signals.append(("strong_momentum", "bullish", f"20日动量+{last_mom:.1f}%"))
            score += 1
        elif last_mom < -10:
            signals.append(("negative_momentum", "bearish", f"20日动量{last_mom:.1f}%"))
            score -= 1

    # Volume confirmation
    if volumes and len(volumes) >= 20:
        avg_vol = sum(volumes[-20:-1]) / 20
        today_vol = volumes[-1]
        if today_vol > avg_vol * 2:
            if score > 0:
                signals.append(("volume_surge_bullish", "bullish", f"成交量为平均2倍以上放量上涨"))
                score += 1
            elif score < 0:
                signals.append(("volume_surge_bearish", "bearish", f"成交量为平均2倍以上放量下跌"))
                score -= 1

    # Overall signal
    if score >= 3:
        overall = "STRONG_BUY"
        interpretation = "多个技术指标显示强势上涨信号"
    elif score >= 1:
        overall = "BUY"
        interpretation = "技术指标总体偏多"
    elif score <= -3:
        overall = "STRONG_SELL"
        interpretation = "多个技术指标显示强势下跌信号"
    elif score <= -1:
        overall = "SELL"
        interpretation = "技术指标总体偏空"
    else:
        overall = "NEUTRAL"
        interpretation = "技术指标中性，等待进一步信号"

    result = {
        "ticker": ticker,
        "market": data.get("market", "Unknown"),
        "current_price": current_price,
        "score": score,
        "overall_signal": overall,
        "interpretation": interpretation,
        "indicators": {
            "price": current_price,
            "ma5": round(ma5[-1], 2) if ma5[-1] else None,
            "ma10": round(ma10[-1], 2) if ma10[-1] else None,
            "ma20": round(ma20[-1], 2) if ma20[-1] else None,
            "ma50": round(ma50[-1], 2) if ma50[-1] else None,
            "ma200": round(ma200[-1], 2) if ma200[-1] else None,
            "rsi_14": round(last_rsi, 1) if last_rsi else None,
            "macd": round(last_macd, 4) if last_macd else None,
            "macd_signal": round(last_signal, 4) if last_signal else None,
            "momentum_20d": round(last_mom, 2) if last_mom else None,
            "momentum_60d": round(last_mom60, 2) if last_mom60 else None,
            "atr_14": round(atr_val[-1], 2) if atr_val and atr_val[-1] else None,
            "volume_profile_poc": vol_profile.get("poc_price"),
            "bb_upper": round(last_bb_upper, 2) if last_bb_upper else None,
            "bb_lower": round(last_bb_lower, 2) if last_bb_lower else None,
        },
        "signals": [{"type": s[0], "direction": s[1], "description": s[2]} for s in signals],
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    return result


def compute_factors(data: dict) -> dict:
    """Compute quantitative factors from market data."""
    prices = data.get("close") or data.get("price", [])
    if not prices or len(prices) < 60:
        return {}

    returns = [(prices[i] - prices[i - 1]) / prices[i - 1] for i in range(1, len(prices))]

    volatility_20d = float(np.std(returns[-20:]) * math.sqrt(252)) if len(returns) >= 20 else 0
    volatility_60d = float(np.std(returns[-60:]) * math.sqrt(252)) if len(returns) >= 60 else 0

    price = prices[-1]
    ma20 = sum(prices[-20:]) / 20 if len(prices) >= 20 else price
    ma60 = sum(prices[-60:]) / 60 if len(prices) >= 60 else price
    ma200 = sum(prices[-200:]) / 200 if len(prices) >= 200 else price

    mom_20d = (price - prices[-21]) / prices[-21] * 100 if len(prices) >= 21 else 0
    mom_60d = (price - prices[-61]) / prices[-61] * 100 if len(prices) >= 61 else 0
    mom_120d = (price - prices[-121]) / prices[-121] * 100 if len(prices) >= 121 else 0

    annual_return = (price / prices[0] - 1) * 100 if prices[0] > 0 else 0

    sharpe = (annual_return / volatility_20d) if volatility_20d > 0 else 0

    max_dd = 0
    peak = prices[0]
    for p in prices:
        if p > peak:
            peak = p
        dd = (p - peak) / peak * 100
        if dd < max_dd:
            max_dd = dd

    return {
        "annualized_return_3m": round(annual_return, 2),
        "volatility_20d": round(volatility_20d * 100, 2),
        "volatility_60d": round(volatility_60d * 100, 2),
        "momentum_20d": round(mom_20d, 2),
        "momentum_60d": round(mom_60d, 2),
        "momentum_120d": round(mom_120d, 2),
        "ma20_vs_price": round((price / ma20 - 1) * 100, 2),
        "ma60_vs_price": round((price / ma60 - 1) * 100, 2),
        "ma200_vs_price": round((price / ma200 - 1) * 100, 2) if ma200 != price else None,
        "sharpe_approx": round(sharpe, 2),
        "max_drawdown_3m": round(max_dd, 2),
    }


def score_against_research(ticker: str, ta_result: dict, factors: dict) -> dict:
    """Score a ticker against knowledge base research findings."""
    research_scores = []
    signals = ta_result.get("signals", [])

    # Momentum factor (research: momentum is well-documented)
    mom20 = factors.get("momentum_20d", 0)
    mom60 = factors.get("momentum_60d", 0)
    if mom60 > 15 and mom20 > 5:
        research_scores.append(("momentum_factor", "bullish", f"60日动量{mom60:.1f}%，符合Jegadeesh-Titman动量效应"))
    elif mom60 < -15 and mom20 < -5:
        research_scores.append(("negative_momentum", "bearish", f"60日强负动量{mom60:.1f}%，趋势可能持续"))

    # RSI check
    rsi = ta_result.get("indicators", {}).get("rsi_14")
    if rsi and rsi < 30:
        research_scores.append(("rsi_oversold_research", "bullish", f"RSI={rsi:.0f}超卖，历史反弹概率高(见 VGRSI 研究)"))
    elif rsi and rsi > 70:
        research_scores.append(("rsi_overbought_research", "caution", f"RSI={rsi:.0f}超买，注意回调风险"))

    # Volatility factor (research: low vol tends to mean-revert)
    vol = factors.get("volatility_20d", 0)
    if vol > 50:
        research_scores.append(("high_volatility", "caution", f"年化波动率{vol:.1f}%极高，杠杆ETF损耗风险大(Bianchi 2026)"))
    elif vol < 10:
        research_scores.append(("low_volatility", "bullish", f"年化波动率{vol:.1f}%低，低波动因子可能有效"))

    # Trend alignment
    ma20_vs_price = factors.get("ma20_vs_price", 0)
    if ma20_vs_price > 5 and ta_result.get("score", 0) > 0:
        research_scores.append(("trend_following", "bullish", f"价格>MA20 {ma20_vs_price:.1f}%，趋势跟踪策略有支撑(见 VGRSI 研究)"))

    return {"research_enhanced_signals": research_scores}


if __name__ == "__main__":
    import sys, json
    data = json.loads(sys.stdin.read())
    ticker = data.get("ticker", "UNKNOWN")
    result = analyze(ticker, data)
    factors = compute_factors(data)
    result["factors"] = factors
    enhanced = score_against_research(ticker, result, factors)
    result["research_enhanced"] = enhanced
    print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
