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

需求函数：

$$Q_i = A - B\,p_i + \gamma\,(p_j + p_k)$$

利润函数：

$$\pi_i = (p_i - c_i)\,Q_i$$

反应函数：

$$p_i = \frac{A}{2B} + \frac{c_i}{2} + \frac{\gamma}{2B}\,(p_j + p_k)$$

本例 $A=10$ 、 $B=2$ 、 $\gamma=1$ ，即 $p_i = 2.5 + c_i/2 + 0.25\,(p_j + p_k)$ 。

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
├── outputs/                   # 仿真图表输出（*.png 已 gitignore，保留 .gitkeep）
│   ├── dynamics.png           #   ← run_dynamics.py 生成
│   ├── deviation.png          #   ← run_deviation.py 生成
│   ├── comparative_cost.png   #   ← run_comparative.py 生成
│   └── comparative_gamma.png  #   ← run_comparative.py 生成
├── docs/
│   ├── model.md               # 模型数学推导记录
│   └── results.md             # 仿真结果记录（含 γ 扫描与建模说明的矛盾分析）
└── tests/
    └── test_model.py          # 单元测试（均衡解 / 反应动态 / 偏离 / 比较静态）
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

> 脚本通过 `uv run` 在项目环境中运行，无需手动激活虚拟环境。每个脚本都**先把
> 关键数值打印到终端**（与期望值 / 理论值对照），再把图保存到 `outputs/`，
> 因此不看图也能验证结论。绘图使用非交互后端（Agg），不弹任何窗口；图内文字
> 统一英文以规避中文字体缺失导致的乱码。

| 仿真 | 命令 | 产出图片 |
| --- | --- | --- |
| 1. 纳什均衡 | `uv run python scripts/run_equilibrium.py` | （无图，纯打印） |
| 2. 最优反应动态 | `uv run python scripts/run_dynamics.py` | `outputs/dynamics.png` |
| 3. 单边偏离检验 | `uv run python scripts/run_deviation.py` | `outputs/deviation.png` |
| 4. 比较静态分析 | `uv run python scripts/run_comparative.py` | `outputs/comparative_cost.png`、`outputs/comparative_gamma.png` |

### 1. 纳什均衡（解析解）

求解 3×3 线性方程组得均衡，并与 `EXPECTED_*` 逐项对照、报告最大误差：

```text
quantity          OpenAI   Anthropic      Google     max err
price  p*         7.3800      7.5400      6.9800    8.88e-16
demand Q*         9.7600      9.2800     10.9600    1.78e-15
profit pi*       47.6288     43.0592     60.0608    1.20e-03
```

### 2. 最优反应动态

从任意初值（默认全 0）同步迭代，约 31 轮收敛到 $p^*$，验证均衡是稳定吸引子：

```text
converged      : True
iterations     : 31
final prices   : [7.38 7.54 6.98]
distance to p* : 5.89e-09
```

### 3. 单边偏离检验

固定其余两家于均衡价，扫描某家价格，利润峰值落在其 $p_i^*$，证明无单边偏离激励：

```text
firm          numeric best     theory p*   peak profit
OpenAI               7.380         7.380        47.629
Anthropic            7.537         7.540        43.059
Google               6.982         6.980        60.061
```

### 4. 比较静态分析

- **扫成本 $c_i$**：自身成本上升 ⟹ 自身均衡价上升、利润下降（符合预期）。
- **扫差异化 $\gamma$**：随 $\gamma$ 增大，均衡价 / 利润**同向上升**，并在 $\gamma = B$
  处奇异发散。这与第2版报告「模块4 概念澄清」一致——其中 $\gamma$ 是价格协同系数，
  $\gamma\uparrow$ 体现定价协同性增强而非竞争加剧（分析限定 $\gamma < B$，不涉及
  趋于同质的零利润悖论极限）。因此 $\gamma$ 图采用对数纵轴并标注 $\gamma=B$
  奇异线。详细数值与机理见 [`docs/results.md`](docs/results.md)。

## 结果验证

- **解析解** 与建模组给定的期望值对照（见上「期望均衡结果」）；
- 单元测试（共 8 项）覆盖：解析均衡价 / 需求 / 利润与 `EXPECTED_*` 一致、反应
  动态收敛到 $p^*$、单边偏离峰值落在 $p_i^*$、成本扫描单调性、以及 $\gamma=1$ 复现
  均衡及 $\gamma$ 扫描的真实趋势：

```bash
uv run pytest
```

## 调整模型参数

所有参数集中在 `src/bertrand_game/config.py`（`BertrandConfig` dataclass）。
修改成本、需求系数或差异化系数时只改此文件，其余模块与脚本自动生效。
