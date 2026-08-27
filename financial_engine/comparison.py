from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class PerformanceDelta:
    window_days: int
    baseline_accuracy_pct: float
    current_accuracy_pct: float
    accuracy_delta_pct: float
    baseline_return_pct: float
    current_return_pct: float
    return_delta_pct: float
    baseline_excess_return_pct: float
    current_excess_return_pct: float
    excess_return_delta_pct: float
    baseline_max_drawdown_pct: float
    current_max_drawdown_pct: float
    drawdown_delta_pct: float
    baseline_profit_factor: float
    current_profit_factor: float
    profit_factor_delta: float
    baseline_trades: int
    current_trades: int


def compare_to_baseline(current: dict[str, Any], baseline: dict[str, Any]) -> PerformanceDelta:
    fields = (
        "accuracy_pct", "strategy_return_pct", "excess_return_pct",
        "max_drawdown_pct", "profit_factor", "signals",
    )
    for source in (current, baseline):
        missing = [f for f in fields if f not in source]
        if missing:
            raise ValueError(f"evaluation record missing fields: {', '.join(missing)}")
    return PerformanceDelta(
        window_days=int(current["window_days"]),
        baseline_accuracy_pct=float(baseline["accuracy_pct"]),
        current_accuracy_pct=float(current["accuracy_pct"]),
        accuracy_delta_pct=round(float(current["accuracy_pct"]) - float(baseline["accuracy_pct"]), 2),
        baseline_return_pct=float(baseline["strategy_return_pct"]),
        current_return_pct=float(current["strategy_return_pct"]),
        return_delta_pct=round(float(current["strategy_return_pct"]) - float(baseline["strategy_return_pct"]), 2),
        baseline_excess_return_pct=float(baseline["excess_return_pct"]),
        current_excess_return_pct=float(current["excess_return_pct"]),
        excess_return_delta_pct=round(float(current["excess_return_pct"]) - float(baseline["excess_return_pct"]), 2),
        baseline_max_drawdown_pct=float(baseline["max_drawdown_pct"]),
        current_max_drawdown_pct=float(current["max_drawdown_pct"]),
        drawdown_delta_pct=round(float(current["max_drawdown_pct"]) - float(baseline["max_drawdown_pct"]), 2),
        baseline_profit_factor=float(baseline["profit_factor"]),
        current_profit_factor=float(current["profit_factor"]),
        profit_factor_delta=round(float(current["profit_factor"]) - float(baseline["profit_factor"]), 4),
        baseline_trades=int(baseline["signals"]),
        current_trades=int(current["signals"]),
    )


def comparison_report(deltas: list[PerformanceDelta]) -> str:
    lines = [
        "# PHOENIX Performance Comparison",
        "",
        "| دوره | دقت قبلی | دقت فعلی | تغییر دقت | بازده قبلی | بازده فعلی | تغییر بازده | مازاد قبلی | مازاد فعلی | تغییر مازاد | افت قبلی | افت فعلی | تغییر افت | ضریب سود قبلی | ضریب سود فعلی |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for d in deltas:
        lines.append(
            f"| {d.window_days} روز | {d.baseline_accuracy_pct:.2f}% | {d.current_accuracy_pct:.2f}% | {d.accuracy_delta_pct:+.2f}% | "
            f"{d.baseline_return_pct:.2f}% | {d.current_return_pct:.2f}% | {d.return_delta_pct:+.2f}% | "
            f"{d.baseline_excess_return_pct:.2f}% | {d.current_excess_return_pct:.2f}% | {d.excess_return_delta_pct:+.2f}% | "
            f"{d.baseline_max_drawdown_pct:.2f}% | {d.current_max_drawdown_pct:.2f}% | {d.drawdown_delta_pct:+.2f}% | "
            f"{d.baseline_profit_factor:.4f} | {d.current_profit_factor:.4f} |"
        )
    lines += ["", "تغییر افت سرمایه منفی‌تر بهتر است؛ تغییر بازده، مازاد بازده و ضریب سود مثبت‌تر بهتر است."]
    return "\n".join(lines)


def as_json(deltas: list[PerformanceDelta]) -> list[dict[str, Any]]:
    return [asdict(d) for d in deltas]
