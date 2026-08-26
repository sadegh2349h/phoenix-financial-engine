from dataclasses import dataclass
from typing import Iterable, Mapping


OHLCV_FIELDS = ("timestamp", "open", "high", "low", "close", "volume")


@dataclass(frozen=True)
class DatasetSnapshot:
    name: str
    provider: str
    timeframe: str
    rows: int
    quality_score: float
    observed_from: str | None
    observed_to: str | None


def normalize_ohlcv(rows: Iterable[Mapping]) -> list[dict]:
    normalized = []
    for row in rows:
        item = {field: row.get(field) for field in OHLCV_FIELDS}
        if item["timestamp"] is None or item["close"] is None:
            continue
        normalized.append(item)
    return normalized
