"""分析模块：单边偏离检验 + 比较静态扫描。

    - deviation_scan: 固定其余两家在均衡价，扫描某一家的价格，得到其利润
      曲线，用于验证利润峰值恰在该厂的均衡价 pᵢ*（即均衡处无单边偏离激励）。
    - comparative_statics_cost / comparative_statics_gamma: 分别扫描某厂边际
      成本 cᵢ 与差异化系数 γ，记录均衡价格 / 利润随参数的变化趋势。
"""

from __future__ import annotations

from dataclasses import dataclass, replace

import numpy as np

from .config import BertrandConfig, DEFAULT_CONFIG
from .model import profit
from .solver import solve_equilibrium


@dataclass
class DeviationResult:
    """单边偏离检验结果。

    Attributes:
        firm: 被扫描的厂商下标（0/1/2）。
        price_grid: 扫描的价格取值数组。
        profits: 与 price_grid 对应的该厂利润数组。
        equilibrium_price: 该厂均衡价格 pᵢ*（理论最优点）。
        best_price: 利润曲线上数值上的最优价格（用于与均衡价对照）。
    """

    firm: int
    price_grid: np.ndarray
    profits: np.ndarray
    equilibrium_price: float
    best_price: float


@dataclass
class ComparativeStaticsResult:
    """比较静态扫描结果。

    Attributes:
        param_name: 被扫描的参数名称（如 "c1"、"gamma"）。
        param_grid: 参数取值数组。
        prices: 形状 (len(param_grid), 3) 的均衡价格随参数变化轨迹。
        profits: 形状 (len(param_grid), 3) 的均衡利润随参数变化轨迹。
    """

    param_name: str
    param_grid: np.ndarray
    prices: np.ndarray
    profits: np.ndarray


def deviation_scan(
    firm: int,
    config: BertrandConfig = DEFAULT_CONFIG,
    *,
    price_range: tuple[float, float] = (0.0, 15.0),
    n_points: int = 200,
) -> DeviationResult:
    """单边偏离检验：固定其余两家于均衡价，扫描指定厂商价格。

    先解出均衡价格作为其余两家的固定值，再在 price_range 上对 firm 取
    n_points 个价格点，计算其利润，从而检验利润峰值是否落在 pᵢ*。

    Args:
        firm: 被扫描的厂商下标（0/1/2）。
        config: 模型参数配置，默认使用 DEFAULT_CONFIG。
        price_range: 扫描价格区间 (低, 高)，单位 $/Mtoken。
        n_points: 价格网格点数。

    Returns:
        DeviationResult，包含价格网格、利润曲线及理论 / 数值最优价格。
    """
    eq = solve_equilibrium(config)
    eq_prices = eq.prices
    equilibrium_price = float(eq_prices[firm])

    price_grid = np.linspace(price_range[0], price_range[1], n_points)
    profits = np.empty(n_points, dtype=float)
    for idx, p_i in enumerate(price_grid):
        # 固定其余两家于均衡价，只改 firm 自身价格
        prices = eq_prices.copy()
        prices[firm] = p_i
        profits[idx] = profit(prices, config)[firm]

    best_price = float(price_grid[int(np.argmax(profits))])
    return DeviationResult(
        firm=firm,
        price_grid=price_grid,
        profits=profits,
        equilibrium_price=equilibrium_price,
        best_price=best_price,
    )


def comparative_statics_cost(
    firm: int,
    config: BertrandConfig = DEFAULT_CONFIG,
    *,
    cost_range: tuple[float, float] = (0.5, 5.0),
    n_points: int = 50,
) -> ComparativeStaticsResult:
    """比较静态：扫描指定厂商的边际成本 cᵢ，观察均衡变化。

    在 cost_range 上对厂商 firm 的边际成本取 n_points 个值，其余参数不变，
    逐点重解均衡，记录三家的均衡价格与利润随 cᵢ 的变化。

    Args:
        firm: 成本被扫描的厂商下标（0/1/2）。
        config: 模型参数配置（提供其余厂商成本及 A/B/γ），默认 DEFAULT_CONFIG。
        cost_range: 边际成本扫描区间 (低, 高)，单位 $/Mtoken。
        n_points: 网格点数。

    Returns:
        ComparativeStaticsResult，记录均衡价格 / 利润随 cᵢ 的轨迹。
    """
    param_grid = np.linspace(cost_range[0], cost_range[1], n_points)
    prices = np.empty((n_points, 3), dtype=float)
    profits = np.empty((n_points, 3), dtype=float)

    base_costs = list(config.marginal_costs)
    for idx, c_i in enumerate(param_grid):
        costs = base_costs.copy()
        costs[firm] = float(c_i)
        cfg = replace(config, marginal_costs=tuple(costs))
        eq = solve_equilibrium(cfg)
        prices[idx] = eq.prices
        profits[idx] = eq.profits

    return ComparativeStaticsResult(
        param_name=f"c{firm + 1}",
        param_grid=param_grid,
        prices=prices,
        profits=profits,
    )


def comparative_statics_gamma(
    config: BertrandConfig = DEFAULT_CONFIG,
    *,
    gamma_range: tuple[float, float] = (0.0, 1.9),
    n_points: int = 50,
) -> ComparativeStaticsResult:
    """比较静态：扫描差异化系数 γ，观察均衡变化。

    在 gamma_range 上取 n_points 个 γ 值（γ 越大产品越同质、竞争越激烈），
    其余参数不变，逐点重解均衡，记录三家均衡价格与利润随 γ 的变化。

    注意：为保证需求 / 均衡的良态，需关注 γ 相对 B 的取值范围（γ < B）。

    Args:
        config: 模型参数配置，默认使用 DEFAULT_CONFIG。
        gamma_range: 差异化系数扫描区间 (低, 高)。
        n_points: 网格点数。

    Returns:
        ComparativeStaticsResult，记录均衡价格 / 利润随 γ 的轨迹。
    """
    param_grid = np.linspace(gamma_range[0], gamma_range[1], n_points)
    prices = np.empty((n_points, 3), dtype=float)
    profits = np.empty((n_points, 3), dtype=float)

    for idx, g in enumerate(param_grid):
        cfg = replace(config, gamma=float(g))
        eq = solve_equilibrium(cfg)
        prices[idx] = eq.prices
        profits[idx] = eq.profits

    return ComparativeStaticsResult(
        param_name="gamma",
        param_grid=param_grid,
        prices=prices,
        profits=profits,
    )
