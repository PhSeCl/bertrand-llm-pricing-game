"""仿真入口 4：比较静态分析 + 出图。

运行：
    uv run python scripts/run_comparative.py

预期输出：分别扫描某厂边际成本 cᵢ 与差异化系数 γ，终端打印关键趋势，
并在 outputs/ 下生成均衡价格 / 利润随参数变化的曲线图。
"""

from __future__ import annotations

import numpy as np

from bertrand_game.analysis import (
    comparative_statics_cost,
    comparative_statics_gamma,
)
from bertrand_game.config import DEFAULT_CONFIG, FIRM_NAMES
from bertrand_game.plots import OUTPUT_DIR, plot_comparative_statics


def _print_table(title: str, param_name: str, grid, prices, profits) -> None:
    """打印某次扫描的抽样行（参数 / 三家价格 / 总利润）。"""
    print("=" * 64)
    print(title)
    print("=" * 64)
    print(f"{param_name:>8}" + "".join(f"{n[:6]+'_p':>10}" for n in FIRM_NAMES)
          + f"{'total_pi':>12}")
    print("-" * 60)
    # 抽样若干行，避免刷屏
    idx = np.linspace(0, len(grid) - 1, 8, dtype=int)
    for i in idx:
        print(f"{grid[i]:>8.3f}" + "".join(f"{prices[i, j]:>10.3f}" for j in range(3))
              + f"{profits[i].sum():>12.3f}")
    print("-" * 60)


def main() -> None:
    """运行成本扫描与差异化系数扫描，打印趋势并分别出图。"""
    B = DEFAULT_CONFIG.B

    # --- 扫成本 c1（OpenAI），其余不变 ---
    cost = comparative_statics_cost(0, DEFAULT_CONFIG, cost_range=(0.5, 5.0), n_points=50)
    _print_table("Comparative statics: scan c1 (OpenAI)", "c1",
                 cost.param_grid, cost.prices, cost.profits)
    print("Trend: higher own cost => higher own price, lower own profit (as expected).\n")
    out_cost = plot_comparative_statics(cost, quantity="both",
                                        save_path=OUTPUT_DIR / "comparative_cost.png")
    print(f"Figure saved to: {out_cost}\n")

    # --- 扫差异化系数 γ，上界留余量(γ<B) ---
    gamma = comparative_statics_gamma(DEFAULT_CONFIG, gamma_range=(0.0, 1.9), n_points=50)
    _print_table("Comparative statics: scan gamma", "gamma",
                 gamma.param_grid, gamma.prices, gamma.profits)
    print("WARNING: profits EXPLODE as gamma -> B (singular at gamma=B); "
          "opposite to the 'zero-profit' expectation. See docs/results.md.")
    # 利润 / 价格爆炸到大数量级 -> 对数纵轴；并标注 γ=B 奇异线
    out_gamma = plot_comparative_statics(
        gamma, quantity="both", logy=True, vline=B, vline_label=f"gamma = B = {B:g} (singular)",
        save_path=OUTPUT_DIR / "comparative_gamma.png",
    )
    print(f"Figure saved to: {out_gamma}")


if __name__ == "__main__":
    main()
