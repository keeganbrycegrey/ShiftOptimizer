from __future__ import annotations

from pprint import pprint

from .models import ProblemInstance
from .optimizer import HybridMemeticOptimizer


def run_case_study() -> None:
    instance = ProblemInstance.case_study_default()
    optimizer = HybridMemeticOptimizer(instance=instance)
    result = optimizer.optimize()

    print("Best objective score:", round(result.best.objective.total_score, 2))
    print("Objective breakdown:")
    pprint(result.best.objective)
    print("Example allocation of cleaning incentives:")
    pprint(result.best.incentives)


if __name__ == "__main__":
    run_case_study()
