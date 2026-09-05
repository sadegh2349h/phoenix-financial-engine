from phoenix_core.oss_source_registry import (
    CURATED_CANDIDATES,
    SOURCE_REGISTRY,
    candidates_by_source,
    sources_by_priority,
)


def test_registry_covers_non_github_sources():
    names = {source.name for source in SOURCE_REGISTRY}
    assert {"Hugging Face", "Kaggle", "PyPI", "arXiv", "OpenML", "GitLab", "npm", "Docker Hub"} <= names
    assert len(names) >= 8


def test_priority_order_is_deterministic():
    ordered = sources_by_priority()
    assert [item.priority for item in ordered] == sorted(item.priority for item in ordered)


def test_curated_candidates_group_by_source():
    grouped = candidates_by_source()
    assert grouped["PyPI"]
    assert grouped["Hugging Face"]
    assert len(CURATED_CANDIDATES) == sum(len(items) for items in grouped.values())
