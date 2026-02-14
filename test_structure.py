from hospital_metaheuristic.main import diagnostic_list
from hospital_metaheuristic.models import HospitalCase, ProcessTimes
from hospital_metaheuristic.optimizer import HospitalMetaheuristic


def test_diagnostic_has_key_sources_of_loss():
    lines = diagnostic_list(HospitalCase(), ProcessTimes())
    assert any("Process loss" in line for line in lines)
    assert any("Behavior loss" in line for line in lines)


def test_optimizer_returns_candidate_and_non_negative_throughput():
    best = HospitalMetaheuristic(HospitalCase(), ProcessTimes(), generations=10, population_size=12).optimize()
    assert best.metrics.surgeries_per_day >= 0
    assert best.objective.total_score >= 0
