from dataclasses import dataclass
from time import monotonic


@dataclass
class Metric:
    name: str
    value: float
    unit: str = "count"


class Timer:
    def __enter__(self):
        self.started = monotonic()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.elapsed_seconds = monotonic() - self.started
