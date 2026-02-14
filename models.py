from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ProcessTimes:
    """turnover times"""

    patient_exit_doc_standard: int = 5
    cleaning_standard: int = 30
    setup_standard: int = 20
    cleaning_delay_min: int = 20
    cleaning_delay_max: int = 30
    setup_delay_min: int = 20
    setup_delay_max: int = 30


@dataclass(frozen=True)
class HospitalCase:
    """case inputs"""

    surgeries_target_per_day: int = 6
    surgeries_current_per_day: int = 4
    surgery_duration_min: int = 180
    operating_minutes_per_day: int = 24 * 60
    nurses_required_active: int = 3
    cleaning_staff_count: int = 3
    nurse_monthly_salary_php: float = 28_000.0
    service_staff_hourly_wage_php: float = 86.875
    hazard_multiplier: float = 1.25
    bonus_pool_php_monthly: float = 15_000.0
    operating_days_per_month: int = 30


@dataclass(frozen=True)
class ScheduleTemplate:
    """shift option"""

    name: str
    shift_hours: int
    handoff_buffer_min: int
    fatigue_penalty_rate: float


@dataclass(frozen=True)
class IncentivePolicy:
    """bonus option"""

    base_cleaning_bonus_share: float
    throughput_bonus_share: float
    quality_gate: float


DEFAULT_TEMPLATES = [
    ScheduleTemplate("12h_two_team", shift_hours=12, handoff_buffer_min=20, fatigue_penalty_rate=1.00),
    ScheduleTemplate("8h_three_team_overlap", shift_hours=8, handoff_buffer_min=10, fatigue_penalty_rate=0.75),
    ScheduleTemplate("6h_four_wave", shift_hours=6, handoff_buffer_min=8, fatigue_penalty_rate=0.60),
]

DEFAULT_POLICIES = [
    IncentivePolicy(base_cleaning_bonus_share=0.40, throughput_bonus_share=0.60, quality_gate=0.98),
    IncentivePolicy(base_cleaning_bonus_share=0.30, throughput_bonus_share=0.70, quality_gate=0.99),
    IncentivePolicy(base_cleaning_bonus_share=0.50, throughput_bonus_share=0.50, quality_gate=0.97),
]
