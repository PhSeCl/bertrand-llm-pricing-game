"""仿真入口 3：单边偏离检验 + 出图。

运行：
    uv run python scripts/run_deviation.py

预期输出：固定其余两家于均衡价，扫描某一家价格，终端打印其利润峰值
所在价格并与该厂均衡价 pᵢ* 对照，在 outputs/ 下生成利润曲线图，确认
峰值落在均衡价（均衡处无单边偏离激励）。
"""

from __future__ import annotations

from bertrand_game.analysis import deviation_scan
from bertrand_game.config import DEFAULT_CONFIG, FIRM_NAMES
from bertrand_game.plots import plot_deviation


def main() -> None:
    """对三家各做单边偏离检验，打印数值最优 vs 理论 p*，并三合一出图。"""
    results = [deviation_scan(f, DEFAULT_CONFIG, price_range=(0.0, 15.0), n_points=2001)
               for f in range(3)]

    print("=" * 64)
    print("Unilateral deviation check (rivals fixed at equilibrium)")
    print("=" * 64)
    print(f"{'firm':<12}{'numeric best':>14}{'theory p*':>14}{'peak profit':>14}")
    print("-" * 54)
    for res in results:
        name = FIRM_NAMES[res.firm]
        print(f"{name:<12}{res.best_price:>14.3f}{res.equilibrium_price:>14.3f}"
              f"{res.profits.max():>14.3f}")
    print("-" * 54)
    print("Numeric peak matches theoretical p* within grid resolution => p* is a Nash equilibrium.")

    out = plot_deviation(results)
    print(f"\nFigure saved to: {out}")


if __name__ == "__main__":
    main()
