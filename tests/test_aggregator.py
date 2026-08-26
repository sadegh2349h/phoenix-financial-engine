from phoenix_core.aggregator import MultiSourceAggregator
from phoenix_core.data_access import DataAccessLayer


class SourceA:
    name = "a"
    def read(self, query):
        return {"source": self.name, "query": query, "data": {"value": 1}}


class SourceB:
    name = "b"
    def read(self, query):
        return {"source": self.name, "query": query, "data": None}


def test_aggregator_preserves_partial_source_availability():
    results = MultiSourceAggregator(DataAccessLayer([SourceA(), SourceB()])).collect("btc")
    summary = MultiSourceAggregator.summary(results)
    assert summary["source_count"] == 2
    assert summary["available_sources"] == ["a"]
    assert summary["coverage"] == 0.5
