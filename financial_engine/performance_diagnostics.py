from __future__ import annotations

from dataclasses import dataclass

from .backtest import BacktestResult


@dataclass(frozen=True)
class PerformanceDiagnosis:
    verdict: str
    primary_weaknesses: tuple[str, ...]
    warnings: tuple[str, ...]


def diagnose(result: BacktestResult, benchmark_pct: float) -> PerformanceDiagnosis:
    weaknesses: list[str] = []
    warnings: list[str] = []

    if result.trades < 10:
        warnings.append("small_sample")
    if result.total_return_pct < benchmark_pct:
        weaknesses.append("strategy_underperformed_benchmark")
    if result.profit_factor < 1.0 and result.trades:
        weaknesses.append("negative_trade_expectancy")
    if result.max_drawdown_pct > 20.0:
        weaknesses.append("drawdown_too_high")
    if result.win_rate_pct < 40.0 and result.trades:
        weaknesses.append("low_win_rate")

    if not result.trades:
        verdict = "NO_EVIDENCE"
    elif not weaknesses:
        verdict = "PROMISING"
    elif "negative_trade_expectancy" in weaknesses:
        verdict = "REJECT"
    else:
        verdict = "NEEDS_IMPROVEMENT"

    return PerformanceDiagnosis(verdict, tuple(weaknesses), tuple(warnings))
