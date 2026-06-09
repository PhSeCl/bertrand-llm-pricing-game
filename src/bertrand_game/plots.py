"""绘图工具：供各 scripts 调用，统一图表风格与输出路径。

所有绘图函数接收已算好的数据结构（来自 solver / analysis），负责出图并
保存到 outputs/ 目录，不参与任何数值计算。

约定：
    - 使用非交互后端 Agg，全程 savefig、不 show，不弹任何窗口。
    - 图内文字（标题 / 轴标签 / 图例）统一用英文，规避中文字体缺失导致的
      方框乱码；中文说明留在 docs/。
"""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # 非交互后端：仅出图保存，不依赖显示环境

import matplotlib.pyplot as plt

from .analysis import ComparativeStaticsResult, DeviationResult
from .config import FIRM_NAMES
from .solver import DynamicsResult

# 仿真图表默认输出目录（仓库根下的 outputs/）。
OUTPUT_DIR: Path = Path(__file__).resolve().parents[2] / "outputs"


def _resolve_save_path(save_path: Path | None, default_name: str) -> Path:
    """确定图片保存路径，确保父目录存在。

    Args:
        save_path: 调用方指定的路径；为 None 时使用 OUTPUT_DIR/default_name。
        default_name: 默认文件名。

    Returns:
        最终保存路径（父目录已创建）。
    """
    path = Path(save_path) if save_path is not None else OUTPUT_DIR / default_name
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def _finish(fig: "plt.Figure", path: Path, show: bool) -> Path:
    """统一收尾：保存图片并按需显示 / 关闭，返回保存路径。"""
    fig.savefig(path, dpi=150, bbox_inches="tight")
    if show:
        plt.show()
    plt.close(fig)
    return path


def plot_dynamics(
    result: DynamicsResult,
    *,
    save_path: Path | None = None,
    show: bool = False,
) -> Path:
    """绘制最优反应动态的价格收敛轨迹。

    横轴为迭代轮次，纵轴为价格，三家厂商各一条曲线，并以水平虚线标注各家
    收敛到的均衡价。

    Args:
        result: best_response_dynamics 返回的迭代结果。
        save_path: 图片保存路径；为 None 时保存到 OUTPUT_DIR/dynamics.png。
        show: 是否调用 plt.show() 交互显示（默认 False，不弹窗）。

    Returns:
        实际保存的图片路径。
    """
    history = result.history
    iterations = range(history.shape[0])

    fig, ax = plt.subplots(figsize=(8, 5))
    for i, name in enumerate(FIRM_NAMES):
        line, = ax.plot(iterations, history[:, i], marker="o", markersize=3, label=name)
        # 收敛价水平虚线，颜色与对应曲线一致
        ax.axhline(result.final_prices[i], color=line.get_color(), ls="--", lw=0.8, alpha=0.6)

    status = "converged" if result.converged else "not converged"
    ax.set_title(f"Best-Response Dynamics Convergence ({status} in {result.n_iter} iters)")
    ax.set_xlabel("Iteration")
    ax.set_ylabel("Price ($/Mtoken)")
    ax.legend(title="Firm")
    ax.grid(True, alpha=0.3)

    return _finish(fig, _resolve_save_path(save_path, "dynamics.png"), show)


def plot_deviation(
    result: DeviationResult | Sequence[DeviationResult],
    *,
    save_path: Path | None = None,
    show: bool = False,
) -> Path:
    """绘制单边偏离的利润曲线（支持单家或多家三合一）。

    横轴为被扫描厂商的价格，纵轴为其利润；以竖直虚线标出各家均衡价 pᵢ*，
    并在数值最优点处打标记，直观展示利润峰值落在均衡价。

    Args:
        result: deviation_scan 返回的单个结果，或多家结果的序列（多家时
            叠加到同一坐标系，便于三合一对照）。
        save_path: 图片保存路径；为 None 时保存到 OUTPUT_DIR/deviation.png。
        show: 是否交互显示（默认 False）。

    Returns:
        实际保存的图片路径。
    """
    results = [result] if isinstance(result, DeviationResult) else list(result)

    fig, ax = plt.subplots(figsize=(8, 5))
    for res in results:
        name = FIRM_NAMES[res.firm]
        line, = ax.plot(res.price_grid, res.profits, label=f"{name} profit")
        color = line.get_color()
        # 均衡价竖线 + 数值最优点标记
        ax.axvline(res.equilibrium_price, color=color, ls="--", lw=0.9, alpha=0.7)
        peak = res.profits.max()
        ax.plot(res.best_price, peak, marker="*", color=color, markersize=12)

    ax.set_title("Unilateral Deviation Check (peak profit at $p_i^*$)")
    ax.set_xlabel("Own price ($/Mtoken)")
    ax.set_ylabel("Own profit")
    ax.legend(title="Firm (dashed line = $p_i^*$)")
    ax.grid(True, alpha=0.3)

    return _finish(fig, _resolve_save_path(save_path, "deviation.png"), show)


def plot_comparative_statics(
    result: ComparativeStaticsResult,
    *,
    quantity: str = "prices",
    save_path: Path | None = None,
    show: bool = False,
    logy: bool = False,
    vline: float | None = None,
    vline_label: str | None = None,
) -> Path:
    """绘制比较静态扫描结果。

    横轴为被扫描参数（cᵢ 或 γ），纵轴为三家厂商的均衡价格或利润。

    Args:
        result: comparative_statics_* 返回的扫描结果。
        quantity: 绘制对象，"prices"、"profits" 或 "both"（左右子图并列）。
        save_path: 图片保存路径；为 None 时保存到
            OUTPUT_DIR/comparative_{param_name}.png。
        show: 是否交互显示（默认 False）。
        logy: 纵轴是否用对数刻度（用于 γ 扫描中利润 / 价格爆炸到大数量级的情形）。
        vline: 若给定，在该横坐标处画竖直虚线（用于标注 γ=B 奇异线）。
        vline_label: 竖线的图例标签。

    Returns:
        实际保存的图片路径。
    """
    panels = ["prices", "profits"] if quantity == "both" else [quantity]
    data_map = {"prices": result.prices, "profits": result.profits}
    ylabel_map = {"prices": "Equilibrium price ($/Mtoken)", "profits": "Equilibrium profit"}

    fig, axes = plt.subplots(1, len(panels), figsize=(6 * len(panels), 5), squeeze=False)
    for ax, panel in zip(axes[0], panels):
        data = data_map[panel]
        for i, name in enumerate(FIRM_NAMES):
            ax.plot(result.param_grid, data[:, i], marker=".", label=name)
        if vline is not None:
            ax.axvline(vline, color="red", ls=":", lw=1.5, label=vline_label or "singular")
        if logy:
            ax.set_yscale("log")
        ax.set_xlabel(result.param_name)
        ax.set_ylabel(ylabel_map[panel])
        ax.set_title(f"Equilibrium {panel} vs {result.param_name}")
        ax.legend(title="Firm")
        ax.grid(True, alpha=0.3)

    default_name = f"comparative_{result.param_name}.png"
    return _finish(fig, _resolve_save_path(save_path, default_name), show)
