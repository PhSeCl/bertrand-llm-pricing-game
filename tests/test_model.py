"""单元测试占位：验证解析均衡解与建模组期望值一致。

运行：
    uv run pytest

实现求解器后，下列测试应验证 solve_equilibrium() 的结果在容差内
等于 EXPECTED_PRICES / EXPECTED_QUANTITIES / EXPECTED_PROFITS。
"""

from __future__ import annotations

import numpy as np
import pytest

from bertrand_game.config import (
    DEFAULT_CONFIG,
    EXPECTED_PRICES,
    EXPECTED_PROFITS,
    EXPECTED_QUANTITIES,
)
from bertrand_game.solver import best_response_dynamics, solve_equilibrium


def test_equilibrium_prices_match_expected() -> None:
    """解析均衡价格应接近 EXPECTED_PRICES ≈ (7.38, 7.54, 6.98)。"""
    result = solve_equilibrium(DEFAULT_CONFIG)
    np.testing.assert_allclose(result.prices, EXPECTED_PRICES, atol=1e-2)


def test_equilibrium_quantities_match_expected() -> None:
    """解析均衡需求应接近 EXPECTED_QUANTITIES ≈ (9.76, 9.28, 10.96)。"""
    result = solve_equilibrium(DEFAULT_CONFIG)
    np.testing.assert_allclose(result.quantities, EXPECTED_QUANTITIES, atol=1e-2)


def test_equilibrium_profits_match_expected() -> None:
    """解析均衡利润应接近 EXPECTED_PROFITS ≈ (47.63, 43.06, 60.06)。"""
    result = solve_equilibrium(DEFAULT_CONFIG)
    np.testing.assert_allclose(result.profits, EXPECTED_PROFITS, atol=1e-2)


@pytest.mark.skip(reason="solver 尚未实现")
def test_dynamics_converges_to_equilibrium() -> None:
    """最优反应动态从任意初始价格应收敛到解析均衡。"""
    eq = solve_equilibrium(DEFAULT_CONFIG)
    dyn = best_response_dynamics(np.zeros(3), DEFAULT_CONFIG)
    assert dyn.converged
    np.testing.assert_allclose(dyn.final_prices, eq.prices, atol=1e-6)
