"""绘图工具：供各 scripts 调用，统一图表风格与输出路径。

所有绘图函数接收已算好的数据结构（来自 solver / analysis），负责出图并
保存到 outputs/ 目录，不参与任何数值计算。
"""

from __future__ import annotations

from pathlib import Path

from .analysis import ComparativeStaticsResult, DeviationResult
from .solver import DynamicsResult

# 仿真图表默认输出目录（仓库根下的 outputs/）。
OUTPUT_DIR: Path = Path(__file__).resolve().parents[2] / "outputs"


def plot_dynamics(
    result: DynamicsResult,
    *,
    save_path: Path | None = None,
    show: bool = False,
) -> Path:
    """绘制最优反应动态的价格收敛轨迹。

    横轴为迭代轮次，纵轴为价格，三家厂商各一条曲线，并标注收敛到的均衡价。

    Args:
        result: best_response_dynamics 返回的迭代结果。
        save_path: 图片保存路径；为 None 时保存到 OUTPUT_DIR 下的默认文件名。
        show: 是否调用 plt.show() 交互显示。

    Returns:
        实际保存的图片路径。
    """
    raise NotImplementedError


def plot_deviation(
    result: DeviationResult,
    *,
    save_path: Path | None = None,
    show: bool = False,
) -> Path:
    """绘制单边偏离的利润曲线。

    横轴为被扫描厂商的价格，纵轴为其利润，并用竖线 / 标记标出均衡价 pᵢ*
    与数值最优价，直观展示峰值位置。

    Args:
        result: deviation_scan 返回的检验结果。
        save_path: 图片保存路径；为 None 时使用 OUTPUT_DIR 下默认文件名。
        show: 是否交互显示。

    Returns:
        实际保存的图片路径。
    """
    raise NotImplementedError


def plot_comparative_statics(
    result: ComparativeStaticsResult,
    *,
    quantity: str = "prices",
    save_path: Path | None = None,
    show: bool = False,
) -> Path:
    """绘制比较静态扫描结果。

    横轴为被扫描参数（cᵢ 或 γ），纵轴为三家厂商的均衡价格或利润，展示
    随参数变化的趋势。

    Args:
        result: comparative_statics_* 返回的扫描结果。
        quantity: 绘制对象，"prices" 或 "profits"。
        save_path: 图片保存路径；为 None 时使用 OUTPUT_DIR 下默认文件名。
        show: 是否交互显示。

    Returns:
        实际保存的图片路径。
    """
    raise NotImplementedError
