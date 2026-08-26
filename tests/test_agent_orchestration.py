from phoenix_core.agent_orchestration import AgentTeam


def test_agents_collaborate_and_produce_consensus():
    team = AgentTeam()
    team.register("strategy", lambda _: {"recommendation": "hold", "confidence": 0.8})
    team.register("risk", lambda _: {"risk": "medium", "confidence": 0.6})
    results = team.run({"objective": "btc"})
    summary = team.consensus(results)
    assert summary["status"] == "completed"
    assert summary["agents"] == ["strategy", "risk"]
    assert summary["confidence"] == 0.7


def test_one_failed_agent_does_not_hide_successful_agents():
    team = AgentTeam()
    team.register("ok", lambda _: {"value": 1, "confidence": 1.0})
    def fail(_):
        raise RuntimeError("temporary failure")
    team.register("broken", fail)
    results = team.run({})
    summary = team.consensus(results)
    assert summary["agents"] == ["ok"]
