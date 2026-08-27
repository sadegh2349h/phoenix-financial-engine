from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any
import json

from .backtest import BacktestResult


@dataclass(frozen=True)
class PerformanceScore:
    accuracy_pct: float
    return_pct: float
    benchmark_pct: float
    excess_return_pct: float
    max_drawdown_pct: float
    profit_factor: float
    trades: int
    confidence: str


def score(result: BacktestResult, benchmark_pct: float) -> PerformanceScore:
    # Accuracy is only meaningful when there are completed trades.
    accuracy = result.win_rate_pct if result.trades else 0.0
    confidence = "insufficient_sample" if result.trades < 10 else "normal"
    return PerformanceScore(
        accuracy_pct=round(accuracy, 2),
        return_pct=round(result.total_return_pct, 2),
        benchmark_pct=round(benchmark_pct, 2),
        excess_return_pct=round(result.total_return_pct - benchmark_pct, 2),
        max_drawdown_pct=round(result.max_drawdown_pct, 2),
        profit_factor=round(result.profit_factor, 4),
        trades=result.trades,
        confidence=confidence,
    )


def markdown_report(asset: str, evaluations: list[dict[str, Any]]) -> str:
    lines = [f"# PHOENIX Performance Report — {asset}", "", "| دوره | معاملات | دقت | بازده | معیار | مازاد | افت سرمایه | ضریب سود | اطمینان |", "|---|---:|---:|---:|---:|---:|---:|---:|---|"]
    for item in evaluations:
        s = item["score"]
        lines.append(
            f"| {item['window_days']} روز | {s.trades} | {s.accuracy_pct:.2f}% | {s.return_pct:.2f}% | {s.benchmark_pct:.2f}% | {s.excess_return_pct:.2f}% | {s.max_drawdown_pct:.2f}% | {s.profit_factor:.4f} | {s.confidence} |"
        )
    lines += ["", "> این گزارش برای ارزیابی گذشته است و تضمین عملکرد آینده نیست."]
    return "\n".join(lines)


def json_report(asset: str, evaluations: list[dict[str, Any]]) -> str:
    payload = {"asset": asset, "evaluations": []}
    for item in evaluations:
        payload["evaluations"].append({"window_days": item["window_days"], "score": asdict(item["score"])})
    return json.dumps(payload, ensure_ascii=False, indent=2)
