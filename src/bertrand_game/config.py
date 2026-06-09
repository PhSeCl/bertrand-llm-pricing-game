"""模型参数集中管理。

本仿真的所有口径参数都定义在这里——需要调整成本、需求弹性或差异化
系数时，**只改本文件**，其余模块通过导入获取，保证全局一致。

参数全部由建模组人工拍定，不涉及任何数据采集 / 爬虫环节。
"""

from __future__ import annotations

from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# 厂商标识（下标约定）
# ---------------------------------------------------------------------------
# 1 = OpenAI, 2 = Anthropic, 3 = Google
FIRM_NAMES: tuple[str, str, str] = ("OpenAI", "Anthropic", "Google")
N_FIRMS: int = 3


@dataclass(frozen=True)
class BertrandConfig:
    """差异化 Bertrand 价格博弈的全部参数。

    需求函数：  Qᵢ = A − B·pᵢ + γ·(pⱼ + pₖ)
    利润函数：  πᵢ = (pᵢ − cᵢ)·Qᵢ
    反应函数：  pᵢ = A/4 + cᵢ/2 + (γ/(2B))·(pⱼ + pₖ)

    Attributes:
        marginal_costs: 三家厂商的边际成本 (c₁, c₂, c₃)，单位 $/Mtoken。
            默认 OpenAI=2.5、Anthropic=2.9、Google=1.5。
        A: 需求函数截距（市场基础需求规模），无量纲。默认 10。
        B: 自价格敏感系数（自家提价对自身需求的抑制强度）。默认 2。
        gamma: 交叉价格 / 差异化系数（竞品提价对本厂需求的提振强度），
            反映产品替代性，越大越同质。默认 1。
    """

    marginal_costs: tuple[float, float, float] = (2.5, 2.9, 1.5)
    A: float = 10.0
    B: float = 2.0
    gamma: float = 1.0


# 默认配置实例：各模块与脚本默认导入此对象。
DEFAULT_CONFIG: BertrandConfig = BertrandConfig()


# ---------------------------------------------------------------------------
# 期望均衡结果（来自建模组，用于仿真结果验证）
# ---------------------------------------------------------------------------
EXPECTED_PRICES: tuple[float, float, float] = (7.38, 7.54, 6.98)
EXPECTED_QUANTITIES: tuple[float, float, float] = (9.76, 9.28, 10.96)
EXPECTED_PROFITS: tuple[float, float, float] = (47.63, 43.06, 60.06)
