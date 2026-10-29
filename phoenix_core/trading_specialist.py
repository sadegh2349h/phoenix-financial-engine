from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Any, Mapping, Sequence


@dataclass(frozen=True)
class TradingSpecialistProfile:
    name: str = "trading_specialist"
    version: str = "1.1"
    domain: str = "professional trading and financial markets"
    mandate: tuple[str, ...] = (
        "market_structure", "multi_timeframe_technical_analysis",
        "trend_momentum", "volume_liquidity", "volatility",
        "support_resistance_breakouts", "derivatives_positioning",
        "sentiment", "macro_fundamental", "strategy_design",
        "risk_management", "backtesting", "opportunity_detection",
    )
    required_timeframes: tuple[str, ...] = ("1d", "4h", "1h")
    minimum_bars_per_timeframe: int = 100
    minimum_out_of_sample_trades: int = 30
    human_approval_required: bool = True


class TradingSpecialist:
    """Evidence-gated PHOENIX trading analysis contract.

    This component validates evidence and risk controls; it does not calculate
    a trade signal or execute orders. Missing, malformed, or incomplete evidence
    fails closed to NO_TRADE.
    """

    profile = TradingSpecialistProfile()
    _ohlcv_fields = ("open", "high", "low", "close", "volume")

    @staticmethod
    def _finite_number(value: Any) -> bool:
        if isinstance(value, bool):
            return False
        try:
            return math.isfinite(float(value))
        except (TypeError, ValueError):
            return False

    def _validate_timeframes(self, price_data: Any) -> list[str]:
        problems: list[str] = []
        if not isinstance(price_data, Mapping):
            return ["price_data must be a mapping of timeframe to OHLCV rows"]

        for timeframe in self.profile.required_timeframes:
            rows = price_data.get(timeframe)
            if not isinstance(rows, Sequence) or isinstance(rows, (str, bytes)):
                problems.append(f"price_data.{timeframe} must be a sequence of OHLCV rows")
                continue
            if len(rows) < self.profile.minimum_bars_per_timeframe:
                problems.append(
                    f"price_data.{timeframe} needs at least "
                    f"{self.profile.minimum_bars_per_timeframe} rows; got {len(rows)}"
                )
                continue
            for index, row in enumerate(rows):
                if not isinstance(row, Mapping):
                    problems.append(f"price_data.{timeframe}[{index}] must be an OHLCV mapping")
                    break
                missing_fields = [field for field in self._ohlcv_fields if field not in row]
                if missing_fields:
                    problems.append(
                        f"price_data.{timeframe}[{index}] missing fields: {', '.join(missing_fields)}"
                    )
                    break
                if not all(self._finite_number(row[field]) for field in self._ohlcv_fields):
                    problems.append(f"price_data.{timeframe}[{index}] contains non-finite OHLCV values")
                    break
                open_, high, low, close, volume = (float(row[field]) for field in self._ohlcv_fields)
                if min(open_, high, low, close) <= 0 or volume < 0:
                    problems.append(f"price_data.{timeframe}[{index}] has invalid price or volume")
                    break
                if low > min(open_, close) or high < max(open_, close) or low > high:
                    problems.append(f"price_data.{timeframe}[{index}] violates OHLC consistency")
                    break
        return problems

    def _validate_evidence(self, market: Mapping[str, Any]) -> list[str]:
        problems: list[str] = []
        evidence = market.get("evidence")
        if not isinstance(evidence, Mapping):
            return ["evidence mapping is required"]

        for key in ("technical_analysis", "fundamental_analysis", "sentiment_analysis", "positioning_analysis"):
            if evidence.get(key) is not True:
                problems.append(f"evidence.{key} must be explicitly confirmed")

        backtest = evidence.get("backtest")
        if not isinstance(backtest, Mapping):
            problems.append("evidence.backtest report is required")
        else:
            if backtest.get("passed") is not True:
                problems.append("evidence.backtest.passed must be true")
            if backtest.get("out_of_sample") is not True:
                problems.append("evidence.backtest.out_of_sample must be true")
            if backtest.get("costs_included") is not True:
                problems.append("evidence.backtest.costs_included must be true")
            trades = backtest.get("trades")
            if not self._finite_number(trades) or float(trades) < self.profile.minimum_out_of_sample_trades:
                problems.append(
                    f"evidence.backtest.trades must be at least {self.profile.minimum_out_of_sample_trades}"
                )
        return problems

    def _validate_risk(self, market: Mapping[str, Any]) -> list[str]:
        problems: list[str] = []
        risk = market.get("risk")
        if not isinstance(risk, Mapping):
            return ["risk controls are required"]

        for key in ("stop_loss_defined", "circuit_breakers_enabled"):
            if risk.get(key) is not True:
                problems.append(f"risk.{key} must be true")

        position_size = risk.get("position_size_pct")
        if not self._finite_number(position_size) or not (0 < float(position_size) <= 1.0):
            problems.append("risk.position_size_pct must be greater than 0 and no more than 1%")

        risk_reward = risk.get("risk_reward_ratio")
        if not self._finite_number(risk_reward) or float(risk_reward) < 1.5:
            problems.append("risk.risk_reward_ratio must be at least 1.5")

        max_drawdown = risk.get("max_drawdown_pct")
        if not self._finite_number(max_drawdown) or not (0 <= float(max_drawdown) < 20):
            problems.append("risk.max_drawdown_pct must be measured and below 20%")

        daily_loss = risk.get("daily_loss_pct")
        if not self._finite_number(daily_loss) or not (0 <= float(daily_loss) < 3):
            problems.append("risk.daily_loss_pct must be measured and below 3%")
        return problems

    def analyze(self, market: dict[str, Any]) -> dict[str, Any]:
        required = ("asset", "timeframes", "price_data")
        missing = [key for key in required if key not in market]
        if missing:
            return {
                "status": "insufficient_data",
                "missing": missing,
                "blockers": ["core market fields are missing"],
                "decision": "NO_TRADE",
                "confidence": 0.0,
                "human_approval_required": True,
            }

        blockers = self._validate_timeframes(market.get("price_data"))
        blockers.extend(self._validate_evidence(market))
        blockers.extend(self._validate_risk(market))

        declared_timeframes = market.get("timeframes")
        if not isinstance(declared_timeframes, Sequence) or isinstance(declared_timeframes, (str, bytes)):
            blockers.append("timeframes must be a sequence")
        elif not all(isinstance(item, str) for item in declared_timeframes) or not set(self.profile.required_timeframes).issubset(set(declared_timeframes)):
            blockers.append(
                "timeframes must include " + ", ".join(self.profile.required_timeframes)
            )

        candidate = market.get("candidate_signal")
        if not isinstance(candidate, str) or candidate not in {"BUY", "SELL", "HOLD"}:
            blockers.append("candidate_signal must be BUY, SELL, or HOLD from a separately validated strategy")

        if blockers:
            return {
                "status": "blocked",
                "specialist": self.profile.name,
                "blockers": blockers,
                "decision": "NO_TRADE",
                "confidence": 0.0,
                "human_approval_required": self.profile.human_approval_required,
            }

        return {
            "status": "ready_for_human_review",
            "specialist": self.profile.name,
            "evidence_required": list(self.profile.mandate),
            "decision": candidate,
            "confidence": 0.0,
            "confidence_note": "No probability is generated by this validation-only component.",
            "human_approval_required": self.profile.human_approval_required,
            "risk_gate": "passed",
            "backtest_gate": "passed",
        }
