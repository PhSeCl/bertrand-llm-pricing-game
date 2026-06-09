"""仿真入口 4：比较静态分析 + 出图。

运行：
    uv run python scripts/run_comparative.py

预期输出：分别扫描某厂边际成本 cᵢ 与差异化系数 γ，终端打印关键趋势，
并在 outputs/ 下生成均衡价格 / 利润随参数变化的曲线图。
"""

from __future__ import annotations

from bertrand_game.analysis import (
    comparative_statics_cost,
    comparative_statics_gamma,
)
from bertrand_game.config import DEFAULT_CONFIG
from bertrand_game.plots import plot_comparative_statics


def main() -> None:
    """运行比较静态扫描并出图（待实现）。"""
    raise NotImplementedError


if __name__ == "__main__":
    main()
