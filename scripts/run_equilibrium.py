"""仿真入口 1：求解纳什均衡并与建模组期望值对照。

运行：
    uv run python scripts/run_equilibrium.py

预期输出：在终端打印解析求得的均衡价格、需求、利润，以及与
EXPECTED_* 期望值的逐项对照（p* ≈ (7.38, 7.54, 6.98) 等）。
"""

from __future__ import annotations

from bertrand_game.config import DEFAULT_CONFIG
from bertrand_game.solver import solve_equilibrium


def main() -> None:
    """求解均衡并打印结果与期望值对照（待实现）。"""
    raise NotImplementedError


if __name__ == "__main__":
    main()
