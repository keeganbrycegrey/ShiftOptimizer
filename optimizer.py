from __future__ import annotations

import random
from dataclasses import dataclass
from typing import List

from .models import DEFAULT_POLICIES, DEFAULT_TEMPLATES, HospitalCase, ProcessTimes
from .objective import Evaluator, ObjectiveBreakdown, PlanMetrics
from .operators import CandidateGenome, crossover, mutate, random_genome, throughput_repair


@dataclass(frozen=True)
class Candidate:
    genome: CandidateGenome
    metrics: PlanMetrics
    objective: ObjectiveBreakdown


class HospitalMetaheuristic:
    def __init__(self, case: HospitalCase, process: ProcessTimes, seed: int = 7, population_size: int = 48, generations: int = 150) -> None:
        self.case = case
        self.process = process
        self.rng = random.Random(seed)
        self.population_size = population_size
        self.generations = generations
        self.evaluator = Evaluator(case, process)

    def optimize(self) -> Candidate:
        population = [self._evaluate(random_genome(self.rng)) for _ in range(self.population_size)]
        population.extend(self._seed_high_throughput_candidates())

        for _ in range(self.generations):
            population = sorted(population, key=lambda c: c.objective.total_score)
            elites = population[: max(4, self.population_size // 6)]
            next_pop: List[Candidate] = elites[:]

            while len(next_pop) < self.population_size:
                a, b = self.rng.sample(elites, 2)
                child_g = mutate(crossover(a.genome, b.genome, self.rng), self.rng, rate=0.22)
                child = self._evaluate(child_g)
                if child.metrics.surgeries_per_day < self.case.surgeries_target_per_day:
                    child = self._evaluate(throughput_repair(child.genome))
                next_pop.append(child)
            population = next_pop

        feasible = [c for c in population if c.metrics.surgeries_per_day >= self.case.surgeries_target_per_day]
        if feasible:
            return min(feasible, key=lambda c: c.objective.total_score)
        return min(population, key=lambda c: c.objective.total_score)

    def _seed_high_throughput_candidates(self) -> List[Candidate]:
        seeded: List[Candidate] = []
        for t_idx in range(len(DEFAULT_TEMPLATES)):
            for p_idx in range(len(DEFAULT_POLICIES)):
                seeded.append(self._evaluate(CandidateGenome(t_idx, p_idx, cleaning_gain=1.0, setup_gain=1.0)))
        return seeded

    def _evaluate(self, genome: CandidateGenome) -> Candidate:
        template = DEFAULT_TEMPLATES[genome.template_idx]
        policy = DEFAULT_POLICIES[genome.policy_idx]
        metrics = self.evaluator.metrics(template, policy, genome.cleaning_gain, genome.setup_gain)
        objective = self.evaluator.score(metrics)
        return Candidate(genome=genome, metrics=metrics, objective=objective)
