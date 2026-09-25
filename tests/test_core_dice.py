"""Dice tests: 4dF distribution with a fixed seed, and ladder
boundaries at every tier edge."""

from __future__ import annotations

import random
from collections import Counter

from linkloader.dice import check, roll_4dF, tier_for


def test_4df_faces_are_only_minus1_0_plus1():
    rng = random.Random(1234)
    for _ in range(500):
        dice = roll_4dF(rng)
        assert len(dice) == 4
        assert all(d in (-1, 0, 1) for d in dice)


def test_4df_is_reproducible_with_a_fixed_seed():
    a = roll_4dF(random.Random(42))
    b = roll_4dF(random.Random(42))
    assert a == b


def test_4df_distribution_is_roughly_even_across_faces():
    rng = random.Random(7)
    counts = Counter()
    for _ in range(6000):
        for die in roll_4dF(rng):
            counts[die] += 1
    total = sum(counts.values())
    assert total == 6000 * 4
    for face in (-1, 0, 1):
        share = counts[face] / total
        assert 0.28 < share < 0.38  # each face should land near 1/3


def test_ladder_boundaries_at_difficulty_2():
    # style: total >= 5, success: total >= 3, tie: total == 2, else fail.
    assert tier_for(5, 2) == "style"
    assert tier_for(4, 2) == "success"
    assert tier_for(3, 2) == "success"
    assert tier_for(2, 2) == "tie"
    assert tier_for(1, 2) == "fail"
    assert tier_for(-4, 2) == "fail"


def test_ladder_boundaries_at_difficulty_0():
    assert tier_for(3, 0) == "style"
    assert tier_for(1, 0) == "success"
    assert tier_for(0, 0) == "tie"
    assert tier_for(-1, 0) == "fail"


def test_check_result_matches_seeded_roll():
    rng = random.Random(5)
    result = check(stat_value=0, difficulty=2, rng=rng)
    assert result.dice == (1, 0, 1, 0)
    assert result.total == 2
    assert result.tier == "tie"
    assert result.shifts == 0


def test_check_adds_stat_to_total():
    rng = random.Random(5)
    result = check(stat_value=3, difficulty=2, rng=rng)
    assert result.total == 5
    assert result.tier == "style"
