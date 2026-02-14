from __future__ import annotations

from dataclasses import dataclass
from math import floor

from .models import HospitalCase, IncentivePolicy, ProcessTimes, ScheduleTemplate


@dataclass(frozen=True)
class PlanMetrics:
    cycle_time_min: float
    surgeries_per_day: int
    throughput_gap: int
    fatigue_score: float
    cleaning_bonus_per_staff_php: float


@dataclass(frozen=True)
class ObjectiveBreakdown:
    total_score: float
    throughput_penalty: float
    fatigue_penalty: float
    fairness_penalty: float


class Evaluator:
    """score model"""

    def __init__(self, case: HospitalCase, process: ProcessTimes) -> None:
        self.case = case
        self.process = process

    def metrics(self, template: ScheduleTemplate, policy: IncentivePolicy, cleaning_gain: float, setup_gain: float) -> PlanMetrics:
        cleaning_time = self.process.cleaning_standard + (1 - cleaning_gain) * self.process.cleaning_delay_max
        setup_time = self.process.setup_standard + (1 - setup_gain) * self.process.setup_delay_max
        fatigue_multiplier = template.fatigue_penalty_rate

        cycle_time = self.case.surgery_duration_min + self.process.patient_exit_doc_standard + cleaning_time + setup_time
        surgeries = floor(self.case.operating_minutes_per_day / cycle_time)
        gap = max(0, self.case.surgeries_target_per_day - surgeries)

        fatigue_score = (template.shift_hours / 12) * fatigue_multiplier
        per_staff = self.case.bonus_pool_php_monthly / self.case.cleaning_staff_count
        bonus = per_staff * (policy.base_cleaning_bonus_share + policy.throughput_bonus_share * min(1.0, surgeries / self.case.surgeries_target_per_day))

        return PlanMetrics(
            cycle_time_min=cycle_time,
            surgeries_per_day=surgeries,
            throughput_gap=gap,
            fatigue_score=fatigue_score,
            cleaning_bonus_per_staff_php=bonus,
        )

    def score(self, metrics: PlanMetrics) -> ObjectiveBreakdown:
        throughput_penalty = metrics.throughput_gap * 1000
        fatigue_penalty = metrics.fatigue_score * 100
        fairness_penalty = abs(metrics.cleaning_bonus_per_staff_php - (self.case.bonus_pool_php_monthly / self.case.cleaning_staff_count))
        total = throughput_penalty + fatigue_penalty + fairness_penalty
        return ObjectiveBreakdown(total, throughput_penalty, fatigue_penalty, fairness_penalty)
