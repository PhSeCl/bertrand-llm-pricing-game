"""纯模型定义：需求函数、利润函数、反应函数。

本模块只描述博弈的数学结构，不做任何求解或仿真。所有函数都是无副作用
的纯函数，输入价格向量与配置，输出对应的需求 / 利润 / 最优反应价格。

约定：价格、需求、利润均以长度为 3 的向量（np.ndarray，下标 0/1/2 对应
厂商 1/2/3）表示。
"""

from __future__ import annotations

import numpy as np

from .config import BertrandConfig, DEFAULT_CONFIG


def demand(prices: np.ndarray, config: BertrandConfig = DEFAULT_CONFIG) -> np.ndarray:
    """计算给定价格向量下三家厂商的需求量。

    需求函数：Qᵢ = A − B·pᵢ + γ·(pⱼ + pₖ)，
    其中 (pⱼ + pₖ) 为除厂商 i 外另两家价格之和。

    Args:
        prices: 长度为 3 的价格向量 (p₁, p₂, p₃)，单位 $/Mtoken。
        config: 模型参数配置，默认使用 DEFAULT_CONFIG。

    Returns:
        长度为 3 的需求向量 (Q₁, Q₂, Q₃)。
    """
    prices = np.asarray(prices, dtype=float)
    # 竞品价格之和 = 全体价格之和 − 自身价格
    rivals_sum = prices.sum() - prices
    return config.A - config.B * prices + config.gamma * rivals_sum


def profit(prices: np.ndarray, config: BertrandConfig = DEFAULT_CONFIG) -> np.ndarray:
    """计算给定价格向量下三家厂商的利润。

    利润函数：πᵢ = (pᵢ − cᵢ)·Qᵢ。

    Args:
        prices: 长度为 3 的价格向量 (p₁, p₂, p₃)，单位 $/Mtoken。
        config: 模型参数配置，默认使用 DEFAULT_CONFIG。

    Returns:
        长度为 3 的利润向量 (π₁, π₂, π₃)。
    """
    prices = np.asarray(prices, dtype=float)
    costs = np.asarray(config.marginal_costs, dtype=float)
    return (prices - costs) * demand(prices, config)


def best_response(
    firm: int,
    prices: np.ndarray,
    config: BertrandConfig = DEFAULT_CONFIG,
) -> float:
    """计算单个厂商在给定竞品价格下的最优反应价格。

    反应函数：pᵢ = A/4 + cᵢ/2 + (γ/(2B))·(pⱼ + pₖ)。
    仅使用 prices 中另两家的价格，prices[firm] 自身的值被忽略。

    Args:
        firm: 厂商下标（0/1/2，对应厂商 1/2/3）。
        prices: 长度为 3 的当前价格向量，用于读取竞品价格之和。
        config: 模型参数配置，默认使用 DEFAULT_CONFIG。

    Returns:
        厂商 firm 的最优反应价格（标量）。
    """
    prices = np.asarray(prices, dtype=float)
    c_i = config.marginal_costs[firm]
    rivals_sum = prices.sum() - prices[firm]
    return config.A / (2 * config.B) + c_i / 2 + (config.gamma / (2 * config.B)) * rivals_sum


def best_response_all(
    prices: np.ndarray,
    config: BertrandConfig = DEFAULT_CONFIG,
) -> np.ndarray:
    """对三家厂商同时计算最优反应价格（同步更新一轮）。

    用于最优反应动态迭代：给定当前价格向量，返回所有厂商各自针对
    当前竞品价格的最优反应。

    Args:
        prices: 长度为 3 的当前价格向量 (p₁, p₂, p₃)。
        config: 模型参数配置，默认使用 DEFAULT_CONFIG。

    Returns:
        长度为 3 的最优反应价格向量。
    """
    prices = np.asarray(prices, dtype=float)
    costs = np.asarray(config.marginal_costs, dtype=float)
    rivals_sum = prices.sum() - prices
    return config.A / (2 * config.B) + costs / 2 + (config.gamma / (2 * config.B)) * rivals_sum
