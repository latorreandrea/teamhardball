from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass
class EvaluationStats:
    created_count: int = 0


def evaluate_user_achievements(user, *, only_definition_ids: Iterable[int] | None = None) -> EvaluationStats:
    # Automatic achievement assignment has been disabled.
    return EvaluationStats()


def evaluate_all_users_achievements() -> EvaluationStats:
    # No automatic awards are generated when this command is run.
    return EvaluationStats()
