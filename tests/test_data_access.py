from phoenix_core.data_access import DataAccessLayer, InMemoryDataSource


def test_data_access_queries_all_sources():
    layer = DataAccessLayer([InMemoryDataSource({"growth": {"score": 90}})])
    result = layer.query("growth")
    assert result["memory"]["data"] == {"score": 90}
