"""仿真入口 2：最优反应动态收敛仿真 + 出图。

运行：
    uv run python scripts/run_dynamics.py

预期输出：从任意初始价格迭代逼近均衡，终端打印收敛信息（迭代次数、
最终价格），并在 outputs/ 下生成价格收敛轨迹图，验证均衡为稳定吸引子。
"""

from __future__ import annotations

import numpy as np

from bertrand_game.config import DEFAULT_CONFIG
from bertrand_game.plots import plot_dynamics
from bertrand_game.solver import best_response_dynamics


def main() -> None:
    """运行最优反应动态并出图（待实现）。"""
    raise NotImplementedError


if __name__ == "__main__":
    main()
