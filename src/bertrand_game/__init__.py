"""bertrand_game：大模型 API 厂商差异化 Bertrand 价格博弈仿真包。

子模块组织（关注点分离）：
    - config:   全部模型参数集中管理（边际成本、需求函数系数等）。
    - model:    纯模型定义（需求函数、利润函数、反应函数）。
    - solver:   纳什均衡求解（解析解 + 最优反应动态迭代）。
    - analysis: 单边偏离检验与比较静态扫描。
    - plots:    绘图工具，供 scripts 调用。
"""

__version__ = "0.1.0"
