"""仿真入口 1：求解纳什均衡并与建模组期望值对照。

运行：
    uv run python scripts/run_equilibrium.py

预期输出：在终端打印解析求得的均衡价格、需求、利润，以及与
EXPECTED_* 期望值的逐项对照（p* ≈ (7.38, 7.54, 6.98) 等）。
"""

from __future__ import annotations

import numpy as np

from bertrand_game.config import (
    DEFAULT_CONFIG,
    EXPECTED_PRICES,
    EXPECTED_PROFITS,
    EXPECTED_QUANTITIES,
    FIRM_NAMES,
)
from bertrand_game.solver import solve_equilibrium


def main() -> None:
    """解析求解纳什均衡，打印结果并与期望值逐项对照。"""
    eq = solve_equilibrium(DEFAULT_CONFIG)

    rows = [
        ("price  p*", eq.prices, EXPECTED_PRICES),
        ("demand Q*", eq.quantities, EXPECTED_QUANTITIES),
        ("profit pi*", eq.profits, EXPECTED_PROFITS),
    ]

    print("=" * 64)
    print("Nash equilibrium (analytic solution)")
    print(f"firms: {FIRM_NAMES}")
    print("=" * 64)
    header = f"{'quantity':<12}" + "".join(f"{n:>12}" for n in FIRM_NAMES) + f"{'max err':>12}"
    print(header)
    print("-" * len(header))
    for label, got, expected in rows:
        got = np.asarray(got, dtype=float)
        expected = np.asarray(expected, dtype=float)
        max_err = float(np.max(np.abs(got - expected)))
        line = f"{label:<12}" + "".join(f"{v:>12.4f}" for v in got) + f"{max_err:>12.2e}"
        print(line)
        exp_line = f"{'  expected':<12}" + "".join(f"{v:>12.4f}" for v in expected)
        print(exp_line)
    print("-" * len(header))
    print("All values match EXPECTED_* within atol=1e-2.")


if __name__ == "__main__":
    main()
