"""纳什均衡求解：解析解 + 最优反应动态迭代。

提供两种求解路径：
    - solve_equilibrium: 把三条反应函数联立成 3×3 线性方程组直接解出均衡价格；
    - best_response_dynamics: 从任意初始价格出发反复套用反应函数，迭代逼近
      均衡，用于验证均衡是稳定吸引子。
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .config import BertrandConfig, DEFAULT_CONFIG
from .model import best_response_all, demand, profit


@dataclass
class EquilibriumResult:
    """纳什均衡求解结果。

    Attributes:
        prices: 均衡价格向量 (p₁*, p₂*, p₃*)。
        quantities: 均衡需求向量 (Q₁*, Q₂*, Q₃*)。
        profits: 均衡利润向量 (π₁*, π₂*, π₃*)。
    """

    prices: np.ndarray
    quantities: np.ndarray
    profits: np.ndarray


@dataclass
class DynamicsResult:
    """最优反应动态迭代结果。

    Attributes:
        history: 形状为 (n_iter + 1, 3) 的价格轨迹，第 0 行为初始价格。
        converged: 是否在容差内收敛。
        n_iter: 实际迭代次数。
        final_prices: 收敛（或停止）时的价格向量。
    """

    history: np.ndarray
    converged: bool
    n_iter: int
    final_prices: np.ndarray


def solve_equilibrium(config: BertrandConfig = DEFAULT_CONFIG) -> EquilibriumResult:
    """解析求解纳什均衡。

    将三条反应函数 pᵢ = A/4 + cᵢ/2 + (γ/(2B))·(pⱼ + pₖ) 整理为线性方程组
    M·p = b 并求解，再代入需求函数与利润函数得到均衡需求与利润。

    Args:
        config: 模型参数配置，默认使用 DEFAULT_CONFIG。

    Returns:
        EquilibriumResult，包含均衡价格、需求、利润。
    """
    A, B, gamma = config.A, config.B, config.gamma
    costs = np.asarray(config.marginal_costs, dtype=float)
    n = costs.size

    # 反应函数 pᵢ = A/(2B) + cᵢ/2 + (γ/(2B))·Σ_{j≠i} pⱼ 两边乘 2B 移项：
    #   2B·pᵢ − γ·Σ_{j≠i} pⱼ = A + B·cᵢ
    # 写成 M·p = b：对角元 2B，非对角元 −γ。
    M = np.full((n, n), -gamma, dtype=float)
    np.fill_diagonal(M, 2 * B)
    b = A + B * costs

    prices = np.linalg.solve(M, b)
    quantities = demand(prices, config)
    profits = profit(prices, config)
    return EquilibriumResult(prices=prices, quantities=quantities, profits=profits)


def best_response_dynamics(
    initial_prices: np.ndarray,
    config: BertrandConfig = DEFAULT_CONFIG,
    *,
    tol: float = 1e-8,
    max_iter: int = 1000,
) -> DynamicsResult:
    """最优反应动态迭代求解。

    从 initial_prices 出发，每轮同步对三家套用反应函数更新价格，直到相邻
    两轮价格变化的范数小于 tol 或达到 max_iter。

    Args:
        initial_prices: 长度为 3 的初始价格向量。
        config: 模型参数配置，默认使用 DEFAULT_CONFIG。
        tol: 收敛容差（相邻两轮价格差的范数阈值）。
        max_iter: 最大迭代次数。

    Returns:
        DynamicsResult，包含价格轨迹、是否收敛、迭代次数与最终价格。
    """
    prices = np.asarray(initial_prices, dtype=float).copy()
    history = [prices.copy()]
    converged = False
    n_iter = 0

    for n_iter in range(1, max_iter + 1):
        # 同步（Jacobi 式）更新：三家同时按上一轮对手价做最优反应
        new_prices = best_response_all(prices, config)
        history.append(new_prices.copy())
        if np.linalg.norm(new_prices - prices) < tol:
            prices = new_prices
            converged = True
            break
        prices = new_prices

    return DynamicsResult(
        history=np.asarray(history),
        converged=converged,
        n_iter=n_iter,
        final_prices=prices,
    )
