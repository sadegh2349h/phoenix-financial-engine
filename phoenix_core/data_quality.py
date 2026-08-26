from dataclasses import dataclass
import pandas as pd


@dataclass(frozen=True)
class QualityReport:
    score: float
    rows: int
    missing: int
    duplicate_timestamps: int
    invalid_ohlc: int


def assess_ohlcv(df: pd.DataFrame) -> QualityReport:
    required = ["timestamp", "open", "high", "low", "close", "volume"]
    if not all(c in df.columns for c in required):
        return QualityReport(0.0, len(df), len(df), 0, len(df))
    missing = int(df[required].isna().any(axis=1).sum())
    duplicates = int(df["timestamp"].duplicated().sum())
    invalid = int(((df["high"] < df[["open", "close"]].max(axis=1)) | (df["low"] > df[["open", "close"]].min(axis=1)) | (df["volume"] < 0)).sum())
    total = max(len(df), 1)
    score = max(0.0, 100.0 * (1 - (missing + duplicates + invalid) / total))
    return QualityReport(round(score, 2), len(df), missing, duplicates, invalid)
