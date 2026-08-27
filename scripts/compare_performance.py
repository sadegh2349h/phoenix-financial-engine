from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASELINE = {
    30: {"accuracy_pct": 0.0, "strategy_return_pct": 0.0, "benchmark_return_pct": 25.87, "excess_return_pct": -25.87, "max_drawdown_pct": 0.0, "profit_factor": 0.0, "signals": 0},
    365: {"accuracy_pct": 20.0, "strategy_return_pct": -10.35, "benchmark_return_pct": -28.56, "excess_return_pct": 18.21, "max_drawdown_pct": 22.61, "profit_factor": 0.5156, "signals": 5},
}


def delta(new: float, old: float) -> float:
    return round(new - old, 2)


def main() -> None:
    source = ROOT / "phoenix_market_evaluation.json"
    if not source.exists():
        raise SystemExit("missing phoenix_market_evaluation.json")
    payload = json.loads(source.read_text(encoding="utf-8"))
    results = {int(r["window_days"]): r for r in payload.get("results", [])}

    lines = [
        "# PHOENIX — Before vs Current Performance",
        "",
        "> خط پایه، نتیجه ثبت‌شده تست قبلی است؛ برای ادعای بهبود قطعی باید هر دو نسخه روی داده یکسان و بدون نشت اطلاعات اجرا شوند.",
        "",
        "| دوره | معیار | قبل | فعلی | تغییر |",
        "|---|---|---:|---:|---:|",
    ]
    for days in (30, 365):
        current = results.get(days)
        if not current:
            continue
        for key, label in [
            ("accuracy_pct", "دقت"),
            ("strategy_return_pct", "بازده استراتژی"),
            ("benchmark_return_pct", "بازده معیار"),
            ("excess_return_pct", "بازده مازاد"),
            ("max_drawdown_pct", "افت سرمایه"),
            ("profit_factor", "ضریب سود"),
            ("signals", "تعداد معاملات"),
        ]:
            old = BASELINE[days][key]
            new = float(current[key])
            change = delta(new, old)
            lines.append(f"| {days} روز | {label} | {old:.4f} | {new:.4f} | {change:+.4f} |")

    lines += [
        "",
        "## تفسیر",
        "",
        "- تغییر مثبت در دقت، بازده و بازده مازاد مطلوب است.",
        "- کاهش افت سرمایه مطلوب است؛ بنابراین تغییر منفی در این معیار بهتر است.",
        "- Profit Factor بالاتر از 1 شرط پایه برای سودآوری ناخالص پایدار است.",
        "- کمتر از 10 معامله: نتیجه از نظر آماری نمونه کوچکی است و نباید به‌عنوان موفقیت قطعی تلقی شود.",
    ]
    report = "\n".join(lines) + "\n"
    print(report)
    (ROOT / "phoenix_performance_comparison.md").write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
