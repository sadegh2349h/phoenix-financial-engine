from phoenix_core.agent_dialogue import AgentDialogue


def test_agents_exchange_context_across_rounds():
    dialogue = AgentDialogue()
    dialogue.register("strategy", lambda ctx: {"view": f"strategy-{ctx['round']}"})
    dialogue.register("risk", lambda ctx: {"seen": sorted(ctx["previous"].keys())})
    messages = dialogue.run({"objective": "growth"}, rounds=2)
    assert len(messages) == 4
    assert messages[-1].round == 2
    assert messages[-1].content["seen"] == sorted(["strategy", "risk"])


def test_dialogue_rejects_invalid_rounds():
    dialogue = AgentDialogue()
    try:
        dialogue.run({}, rounds=0)
    except ValueError:
        return
    assert False
