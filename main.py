from __future__ import annotations

from .models import DEFAULT_POLICIES, DEFAULT_TEMPLATES, HospitalCase, ProcessTimes
from .optimizer import HospitalMetaheuristic


def diagnostic_list(case: HospitalCase, process: ProcessTimes) -> list[str]:
    ideal_turnover = process.patient_exit_doc_standard + process.cleaning_standard + process.setup_standard
    worst_turnover = process.patient_exit_doc_standard + process.cleaning_standard + process.cleaning_delay_max + process.setup_standard + process.setup_delay_max
    ideal_cycle = case.surgery_duration_min + ideal_turnover
    worst_cycle = case.surgery_duration_min + worst_turnover
    return [
        f"Process loss: turnover standard is {ideal_turnover} min, but current observed can reach {worst_turnover} min.",
        f"Capacity math: ideal cycle={ideal_cycle} min, degraded cycle={worst_cycle} min.",
        "Behavior loss: cleaners gain no marginal reward for faster turnover, so throughput-improving effort is not reinforced.",
        "Fatigue loss: long end-of-shift nursing periods increase setup delays by 20-30 minutes.",
    ]


def run_case_study() -> None:
    case = HospitalCase()
    process = ProcessTimes()
    solver = HospitalMetaheuristic(case, process)
    best = solver.optimize()

    template = DEFAULT_TEMPLATES[best.genome.template_idx]
    policy = DEFAULT_POLICIES[best.genome.policy_idx]

    print("RQ1")
    for item in diagnostic_list(case, process):
        print(f"- {item}")

    print("\nRQ2")
    print(f"- Nurse shift design: {template.name} (shift length={template.shift_hours}h).")
    print(
        "- Cleaner incentive scheme: monthly PHP 15,000 pool, split by base share "
        f"{int(policy.base_cleaning_bonus_share*100)}% and throughput share {int(policy.throughput_bonus_share*100)}%."
    )
    print(f"- Estimated cleaner bonus per staff: PHP {best.metrics.cleaning_bonus_per_staff_php:,.2f}.")

    print("\RQ3")
    print(f"- New cycle time: {best.metrics.cycle_time_min:.1f} minutes.")
    print(f"- Computed surgeries/day: {best.metrics.surgeries_per_day} (target={case.surgeries_target_per_day}).")


if __name__ == "__main__":
    run_case_study()
