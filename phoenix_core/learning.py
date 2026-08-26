from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Optional


@dataclass
class PredictionOutcome:
    prediction_id: str
    timestamp: str
    symbol: str
    predicted_direction: str
    confidence: float
    horizon_bars: int
    entry_price: float
    outcome_direction: Optional[str] = None
    realized_return_pct: Optional[float] = None
    correct: Optional[bool] = None


class OutcomeLedger:
    """Persistent prediction ledger that closes the loop: prediction -> outcome -> metrics."""

    def __init__(self, path: str = "data/predictions.jsonl") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def record_prediction(self, prediction_id: str, symbol: str, direction: str, confidence: float,
                          horizon_bars: int, entry_price: float) -> PredictionOutcome:
        item = PredictionOutcome(prediction_id, datetime.now(timezone.utc).isoformat(), symbol,
                                 direction, float(confidence), int(horizon_bars), float(entry_price))
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(item), ensure_ascii=False) + "\n")
        return item

    def close_outcome(self, prediction_id: str, realized_return_pct: float) -> bool:
        rows = self._read()
        changed = False
        for row in rows:
            if row["prediction_id"] == prediction_id and row.get("correct") is None:
                ret = float(realized_return_pct)
                row["realized_return_pct"] = ret
                row["outcome_direction"] = "LONG" if ret > 0 else "SHORT" if ret < 0 else "NEUTRAL"
                pred = row["predicted_direction"]
                row["correct"] = (pred == row["outcome_direction"]) or (pred == "NEUTRAL" and abs(ret) < 0.1)
                changed = True
        if changed:
            self._write(rows)
        return changed

    def metrics(self) -> dict:
        rows = [r for r in self._read() if r.get("correct") is not None]
        if not rows:
            return {"closed": 0, "accuracy_pct": 0.0, "avg_return_pct": 0.0}
        return {"closed": len(rows),
                "accuracy_pct": round(100 * sum(bool(r["correct"]) for r in rows) / len(rows), 2),
                "avg_return_pct": round(sum(float(r["realized_return_pct"]) for r in rows) / len(rows), 4)}

    def _read(self):
        if not self.path.exists():
            return []
        return [json.loads(line) for line in self.path.read_text(encoding="utf-8").splitlines() if line.strip()]

    def _write(self, rows):
        self.path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
