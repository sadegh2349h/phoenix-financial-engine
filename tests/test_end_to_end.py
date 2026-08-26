from phoenix_core.agent_orchestrator import AgentOrchestrator, AgentTask
from phoenix_core.data_access import DataAccessLayer, InMemoryDataSource
from phoenix_core.intelligence import IntelligenceLayer


def test_end_to_end_data_agent_intelligence_flow():
    data = DataAccessLayer([InMemoryDataSource({"create growth plan": {"signal": "positive"}})])
    result = AgentOrchestrator(data_access=data, intelligence=IntelligenceLayer()).execute(
        AgentTask("create growth plan", "growth_strategy", {"tenant": "test"})
    )
    assert result["status"] == "completed"
    assert result["data"]["memory"]["data"] == {"signal": "positive"}
    assert result["intelligence"].requires_human_review is True
