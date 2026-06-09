"""仿真入口 2：最优反应动态收敛仿真 + 出图。

运行：
    uv run python scripts/run_dynamics.py

预期输出：从任意初始价格迭代逼近均衡，终端打印收敛信息（迭代次数、
最终价格），并在 outputs/ 下生成价格收敛轨迹图，验证均衡为稳定吸引子。
"""

from __future__ import annotations

import numpy as np

from bertrand_game.config import DEFAULT_CONFIG, FIRM_NAMES
from bertrand_game.plots import plot_dynamics
from bertrand_game.solver import best_response_dynamics, solve_equilibrium


def main() -> None:
    """从任意初始价格运行最优反应动态，打印收敛信息并出图。"""
    initial_prices = np.zeros(3)  # 任意初值，验证均衡为稳定吸引子
    eq = solve_equilibrium(DEFAULT_CONFIG)
    dyn = best_response_dynamics(initial_prices, DEFAULT_CONFIG)

    print("=" * 60)
    print("Best-response dynamics (synchronous / Jacobi)")
    print("=" * 60)
    print(f"firms          : {FIRM_NAMES}")
    print(f"initial prices : {np.round(initial_prices, 4)}")
    print(f"converged      : {dyn.converged}")
    print(f"iterations     : {dyn.n_iter}")
    print(f"final prices   : {np.round(dyn.final_prices, 4)}")
    print(f"equilibrium p* : {np.round(eq.prices, 4)}")
    print(f"distance to p* : {np.linalg.norm(dyn.final_prices - eq.prices):.2e}")

    out = plot_dynamics(dyn)
    print(f"\nFigure saved to: {out}")


if __name__ == "__main__":
    main()
