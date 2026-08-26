from phoenix_core.contracts import ModuleManifest, Task
from phoenix_core.memory import MemoryStore
from phoenix_core.registry import ModuleRegistry
from phoenix_core.orchestrator import PhoenixKernel
from phoenix_core.governance import Governance, Policy


def test_registry_enable_disable():
    registry = ModuleRegistry()
    registry.register(ModuleManifest("financial", "0.1.0", ["market.analysis"]))
    registry.disable("financial")
    assert list(registry.active()) == []
    registry.enable("financial")
    assert [m.name for m in registry.active()] == ["financial"]


def test_kernel_dispatch_and_memory():
    memory = MemoryStore()
    registry = ModuleRegistry()
    kernel = PhoenixKernel(memory, registry)
    kernel.register_handler("demo", lambda task: __import__("phoenix_core.contracts", fromlist=["Decision"]).Decision("d1", task.objective, "observe", 80, []))
    decision = kernel.dispatch(Task("t1", "test"), "demo")
    assert decision.decision_id == "d1"
    assert memory.get("d1") is not None


def test_governance_gate():
    gov = Governance([Policy("sensitive", {"execute"}, True)])
    assert gov.authorize("sensitive", "execute") is False
    assert gov.authorize("sensitive", "execute", human_approved=True) is True
