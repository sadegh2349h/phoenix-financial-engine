from phoenix_core.oss_intelligence_agent import (
    OSSDiscoverySignal,
    PhoenixOSSIntelligenceAgent,
)


def test_agent_discovers_ranks_and_requires_human_approval():
    agent = PhoenixOSSIntelligenceAgent()
    signals = [
        OSSDiscoverySignal("low", "test", "x", relevance=0.5, maturity=0.5),
        OSSDiscoverySignal("high", "test", "x", evidence="verified", relevance=0.95, maturity=0.9),
    ]

    result = agent.run(signals)

    assert result["candidates"][0]["candidate"] == "high"
    assert result["approval_required"] is True
    assert result["candidates"][0]["auto_install"] is False
    assert result["candidates"][0]["execute_third_party_code"] is False
