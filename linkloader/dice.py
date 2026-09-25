"""4dF rolling and the four-tier success ladder.

The ladder is the one rule borrowed from High Tech, Low Lives (see
`/home/user/game-high-tech-low-lives/arcade/cabinet/SCENE-FORMAT.md`):
no code from that project is used here, only the tier boundaries.
"""

from __future__ import annotations

import random
from dataclasses import dataclass

FATE_FACES = (-1, 0, 1)

# Named difficulty tiers, for scene authors and the terminal player.
DIFFICULTY_LADDER = {
    "routine": 0,
    "challenging": 2,
    "very_difficult": 4,
    "nearly_impossible": 6,
}


@dataclass(frozen=True)
class RollResult:
    dice: tuple  # four ints, each -1/0/1
    stat: int
    total: int
    difficulty: int
    tier: str  # "style" | "success" | "tie" | "fail"
    shifts: int  # total - difficulty


def roll_4dF(rng: random.Random) -> tuple:
    return tuple(rng.choice(FATE_FACES) for _ in range(4))


def tier_for(total: int, difficulty: int) -> str:
    if total >= difficulty + 3:
        return "style"
    if total >= difficulty + 1:
        return "success"
    if total == difficulty:
        return "tie"
    return "fail"


def check(stat_value: int, difficulty: int, rng: random.Random) -> RollResult:
    dice = roll_4dF(rng)
    total = sum(dice) + stat_value
    tier = tier_for(total, difficulty)
    return RollResult(
        dice=dice,
        stat=stat_value,
        total=total,
        difficulty=difficulty,
        tier=tier,
        shifts=total - difficulty,
    )
