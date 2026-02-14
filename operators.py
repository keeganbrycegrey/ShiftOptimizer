from __future__ import annotations

import random
from dataclasses import dataclass

from .models import DEFAULT_POLICIES, DEFAULT_TEMPLATES


@dataclass(frozen=True)
class CandidateGenome:
    template_idx: int
    policy_idx: int
    cleaning_gain: float
    setup_gain: float


def random_genome(rng: random.Random) -> CandidateGenome:
    return CandidateGenome(
        template_idx=rng.randrange(len(DEFAULT_TEMPLATES)),
        policy_idx=rng.randrange(len(DEFAULT_POLICIES)),
        cleaning_gain=rng.uniform(0.0, 1.0),
        setup_gain=rng.uniform(0.0, 1.0),
    )


def crossover(a: CandidateGenome, b: CandidateGenome, rng: random.Random) -> CandidateGenome:
    return CandidateGenome(
        template_idx=a.template_idx if rng.random() < 0.5 else b.template_idx,
        policy_idx=a.policy_idx if rng.random() < 0.5 else b.policy_idx,
        cleaning_gain=(a.cleaning_gain + b.cleaning_gain) / 2,
        setup_gain=(a.setup_gain + b.setup_gain) / 2,
    )


def mutate(g: CandidateGenome, rng: random.Random, rate: float) -> CandidateGenome:
    template = g.template_idx
    policy = g.policy_idx
    c_gain = g.cleaning_gain
    s_gain = g.setup_gain

    if rng.random() < rate:
        template = rng.randrange(len(DEFAULT_TEMPLATES))
    if rng.random() < rate:
        policy = rng.randrange(len(DEFAULT_POLICIES))
    if rng.random() < rate:
        c_gain = min(1.0, max(0.0, c_gain + rng.uniform(-0.2, 0.2)))
    if rng.random() < rate:
        s_gain = min(1.0, max(0.0, s_gain + rng.uniform(-0.2, 0.2)))

    return CandidateGenome(template, policy, c_gain, s_gain)


def throughput_repair(g: CandidateGenome) -> CandidateGenome:
    """boost gains"""
    return CandidateGenome(
        template_idx=g.template_idx,
        policy_idx=g.policy_idx,
        cleaning_gain=min(1.0, g.cleaning_gain + 0.1),
        setup_gain=min(1.0, g.setup_gain + 0.1),
    )
