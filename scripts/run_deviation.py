"""仿真入口 3：单边偏离检验 + 出图。

运行：
    uv run python scripts/run_deviation.py

预期输出：固定其余两家于均衡价，扫描某一家价格，终端打印其利润峰值
所在价格并与该厂均衡价 pᵢ* 对照，在 outputs/ 下生成利润曲线图，确认
峰值落在均衡价（均衡处无单边偏离激励）。
"""

from __future__ import annotations

from bertrand_game.analysis import deviation_scan
from bertrand_game.config import DEFAULT_CONFIG
from bertrand_game.plots import plot_deviation


def main() -> None:
    """运行单边偏离检验并出图（待实现）。"""
    raise NotImplementedError


if __name__ == "__main__":
    main()
