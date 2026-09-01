"""Phoenix Edu: transformation-based instructional design specialist."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LearningModule:
    title: str
    learning_objective: str
    core_content: tuple[str, ...]
    actionable_exercise: str
    success_metric: str


def design_course(expertise: str, audience: str, transformation: str) -> tuple[LearningModule, ...]:
    """Create a transformation-first course skeleton with an early quick win."""
    if not expertise.strip() or not audience.strip() or not transformation.strip():
        raise ValueError("expertise, audience and transformation are required")
    return (
        LearningModule(
            "Quick Win: first measurable result", f"Help {audience} experience an early step toward {transformation}.",
            (expertise, "Point A pain", "Point B result", "one key concept"),
            "Complete a small task that produces a visible result in the first session.",
            "Learner completes the task and demonstrates the target behavior.",
        ),
        LearningModule(
            "Core Transformation", f"Apply the core method to move from pain to {transformation}.",
            ("model", "worked example", "common mistakes", "decision rules"),
            "Apply the method to a real learner case.",
            "Rubric-based demonstration of competence.",
        ),
        LearningModule(
            "Implementation & Accountability", "Transfer the skill into real-world behavior.",
            ("micro-learning review", "practice loop", "community accountability", "live Q&A"),
            "Run a real implementation and submit evidence/results.",
            "Completion, implementation rate, and outcome KPI.",
        ),
    )


FRAMEWORKS = ("Bloom's Taxonomy", "ADDIE Model", "Micro-learning")
FORMATS = ("interactive worksheets", "live Q&A", "community accountability")
