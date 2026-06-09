# 大模型 API 的差异化 Bertrand 价格博弈仿真

博弈论课程团队作业。对 **OpenAI、Anthropic、Google** 三家大模型 API 厂商建立
**差异化 Bertrand 寡头价格博弈模型**，求解纳什均衡并做仿真分析。

> 模型由建模组给定，本仓库只负责代码实现。所有参数为人工拍定，**无数据采集 /
> 爬虫环节**。

## 项目简介

围绕模型实现四块仿真：

1. **解析解**：解 3×3 线性方程组求纳什均衡价格、需求、利润。
2. **最优反应动态**：从任意初始价格迭代逼近均衡，验证均衡是稳定吸引子。
3. **单边偏离检验**：固定其余两家于均衡价，扫描某一家价格，确认利润峰值在 $p_i^*$。
4. **比较静态分析**：扫描成本 $c_i$ 与差异化系数 $\gamma$，观察均衡价 / 利润的变化趋势。

全程脚本运行，无 GUI。

## 模型简述

厂商下标：1 = OpenAI、2 = Anthropic、3 = Google。

### 参数表

| 参数 | 含义 | 单位 | 取值 |
| --- | --- | --- | --- |
| $c_1$ | OpenAI 边际成本 | $/Mtoken | 2.5 |
| $c_2$ | Anthropic 边际成本 | $/Mtoken | 2.9 |
| $c_3$ | Google 边际成本 | $/Mtoken | 1.5 |
| $A$ | 需求截距（市场基础需求规模） | — | 10 |
| $B$ | 自价格敏感系数 | — | 2 |
| $\gamma$ | 差异化 / 交叉价格系数 | — | 1 |

### 函数

- 需求函数：$Q_i = A - B\,p_i + \gamma\,(p_j + p_k)$
- 利润函数：$\pi_i = (p_i - c_i)\,Q_i$
- 反应函数：$p_i = \dfrac{A}{4} + \dfrac{c_i}{2} + \dfrac{\gamma}{2B}\,(p_j + p_k)$
  （本例即 $p_i = 2.5 + c_i/2 + 0.25\,(p_j + p_k)$）

### 期望均衡结果（用于验证）

- $p^* \approx (7.38,\ 7.54,\ 6.98)$
- $Q^* \approx (9.76,\ 9.28,\ 10.96)$
- $\pi^* \approx (47.63,\ 43.06,\ 60.06)$

## 目录结构

```
bertrand-llm-pricing-game/
├── README.md                  # 本文件
├── pyproject.toml             # 项目元信息与依赖（uv 管理）
├── .gitignore
├── .python-version            # Python 3.12
├── src/
│   └── bertrand_game/
│       ├── __init__.py
│       ├── config.py          # 所有参数集中管理（c, A, B, γ）——改口径只动这里
│       ├── model.py           # 需求 / 利润 / 反应函数（纯模型定义）
│       ├── solver.py          # 解析解 + 最优反应动态迭代
│       ├── analysis.py        # 单边偏离检验 + 比较静态扫描
│       └── plots.py           # 绘图工具（供 scripts 调用）
├── scripts/                   # uv run 运行的入口脚本，每块仿真一个
│   ├── run_equilibrium.py
│   ├── run_dynamics.py
│   ├── run_deviation.py
│   └── run_comparative.py
├── outputs/                   # 仿真图表输出（已 gitignore，保留 .gitkeep）
├── docs/
│   ├── model.md               # 模型数学推导记录
│   └── results.md             # 仿真结果记录
└── tests/
    └── test_model.py          # 单元测试（验证均衡解与期望值一致）
```

## 环境搭建

本项目使用 [uv](https://docs.astral.sh/uv/) 管理 Python 环境与依赖。

### 1. 安装 uv

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. 同步依赖

```bash
# 安装运行依赖（numpy、matplotlib）
uv sync

# 如需运行测试，额外安装 dev 依赖（pytest）
uv sync --extra dev
```

uv 会自动按 `.python-version` 创建虚拟环境（`.venv/`）并安装依赖。

## 运行各仿真

> 脚本通过 `uv run` 在项目环境中运行，无需手动激活虚拟环境。

| 仿真 | 命令 | 预期输出 |
| --- | --- | --- |
| 1. 纳什均衡 | `uv run python scripts/run_equilibrium.py` | 终端打印均衡价格 / 需求 / 利润，并与期望值逐项对照 |
| 2. 最优反应动态 | `uv run python scripts/run_dynamics.py` | 终端打印收敛信息，`outputs/` 生成价格收敛轨迹图 |
| 3. 单边偏离检验 | `uv run python scripts/run_deviation.py` | 终端打印利润峰值价格 vs $p_i^*$，`outputs/` 生成利润曲线图 |
| 4. 比较静态分析 | `uv run python scripts/run_comparative.py` | 终端打印趋势，`outputs/` 生成 $c_i$ / $\gamma$ 扫描图 |

## 结果验证

- **解析解** 与建模组给定的期望值对照（见上「期望均衡结果」）；
- 单元测试断言 `solve_equilibrium()` 的结果在容差内等于 `config.py` 中的
  `EXPECTED_PRICES / EXPECTED_QUANTITIES / EXPECTED_PROFITS`：

```bash
uv run pytest
```

## 调整模型参数

所有参数集中在 `src/bertrand_game/config.py`（`BertrandConfig` dataclass）。
修改成本、需求系数或差异化系数时只改此文件，其余模块与脚本自动生效。
