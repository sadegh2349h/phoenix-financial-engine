from phoenix_core.data_access import DataAccessLayer, InMemoryDataSource
from phoenix_core.data_pipeline import DataPipeline


def test_pipeline_collects_auditable_snapshot():
    access = DataAccessLayer([InMemoryDataSource({"btc": {"price": 100}})])
    pipeline = DataPipeline(access)
    snapshot = pipeline.collect("btc")
    assert snapshot.complete is True
    assert snapshot.sources["memory"]["data"] == {"price": 100}
    assert pipeline.monitor.health()["events"] == 2
