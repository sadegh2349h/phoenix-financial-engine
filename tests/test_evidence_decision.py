from phoenix_core.aggregator import SourceResult
from phoenix_core.evidence_decision import EvidenceDecisionEngine
from phoenix_core.memory import MemoryStore


def test_decision_is_persisted_with_evidence_and_confidence():
    memory = MemoryStore()
    engine = EvidenceDecisionEngine(memory)
    record = engine.decide("btc", [
        SourceResult("market", {"price": 100}, True),
        SourceResult("sentiment", {"score": 70}, True),
    ])
    assert record.decision == "proceed"
    assert record.confidence == 1.0
    assert memory.get("decision:btc")["confidence"] == 1.0
    assert len(memory.get("decision:btc")["evidence"]) == 2
