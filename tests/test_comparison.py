from financial_engine.comparison import compare_to_baseline, comparison_report


def record(window, accuracy, ret, excess, dd, pf, trades):
    return {
        "window_days": window,
        "accuracy_pct": accuracy,
        "strategy_return_pct": ret,
        "excess_return_pct": excess,
        "max_drawdown_pct": dd,
        "profit_factor": pf,
        "signals": trades,
    }


def test_comparison_reports_exact_deltas():
    baseline = record(365, 20.0, -10.35, 18.21, 22.61, 0.5156, 5)
    current = record(365, 60.0, 12.0, 15.0, 10.0, 1.5, 20)
    delta = compare_to_baseline(current, baseline)
    assert delta.accuracy_delta_pct == 40.0
    assert delta.return_delta_pct == 22.35
    assert delta.drawdown_delta_pct == -12.61
    assert delta.profit_factor_delta == 0.9844


def test_comparison_report_is_human_readable():
    baseline = record(30, 0.0, 0.0, -25.87, 0.0, 0.0, 0)
    current = record(30, 50.0, 5.0, 3.0, 4.0, 1.2, 10)
    report = comparison_report([compare_to_baseline(current, baseline)])
    assert "30 روز" in report
    assert "+50.00%" in report
    assert "+5.00%" in report
