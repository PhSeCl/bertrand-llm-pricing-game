# 模型数学推导记录

> 本文件记录差异化 Bertrand 价格博弈的模型设定与均衡推导。模型由建模组
> 给定，本仓库只做代码实现。（先放骨架，后续补充推导细节。）

## 1. 模型设定

- 厂商集合：1 = OpenAI、2 = Anthropic、3 = Google
- 决策变量：各厂定价 $p_i$（单位 \$/Mtoken）

### 1.1 参数

| 参数 | 含义 | 取值 |
| --- | --- | --- |
| $c_1, c_2, c_3$ | 边际成本 | 2.5 / 2.9 / 1.5 |
| $A$ | 需求截距 | 10 |
| $B$ | 自价格敏感系数 | 2 |
| $\gamma$ | 差异化 / 交叉价格系数 | 1 |

## 2. 需求函数

$$Q_i = A - B\,p_i + \gamma\,(p_j + p_k)$$

经济含义上，需求项 $-Bp_i$ 表示自身提价导致需求下降，交叉项 $+\gamma(p_j+p_k)$
表示竞品提价时部分客户转向本厂；约束 $\gamma < B$ 表示交叉价格效应弱于自价格
效应，体现产品差异化（客户不会因微小价差全部流失）。

## 3. 利润函数

$$\pi_i = (p_i - c_i)\,Q_i$$

## 4. 反应函数

对 $\pi_i = (p_i - c_i)\big(A - Bp_i + \gamma(p_j+p_k)\big)$ 关于 $p_i$ 求一阶条件
$\partial \pi_i/\partial p_i = 0$：

$$\frac{\partial \pi_i}{\partial p_i} = \big(A - Bp_i + \gamma(p_j+p_k)\big) + (p_i - c_i)(-B) = 0$$

$$\Rightarrow A + Bc_i + \gamma(p_j+p_k) - 2Bp_i = 0$$

$$\Rightarrow p_i = \frac{A}{2B} + \frac{c_i}{2} + \frac{\gamma}{2B}(p_j+p_k)$$

二阶条件为 $\partial^2\pi_i/\partial p_i^2 = -2B < 0$，故一阶条件给出的是利润最大值点。

本例参数下：

$$p_i = 2.5 + c_i/2 + 0.25\,(p_j + p_k)$$

## 5. 纳什均衡求解

将通式两边乘 $2B$ 整理得 $2Bp_i - \gamma(p_j+p_k) = A + Bc_i$，三式联立为
$M\mathbf{p} = \mathbf{b}$。代入 $A=10,\ B=2,\ \gamma=1$：

$$M = \begin{pmatrix} 4 & -1 & -1 \\ -1 & 4 & -1 \\ -1 & -1 & 4 \end{pmatrix}, \quad \mathbf{b} = \begin{pmatrix} A+Bc_1 \\ A+Bc_2 \\ A+Bc_3 \end{pmatrix} = \begin{pmatrix} 15.0 \\ 15.8 \\ 13.0 \end{pmatrix}$$

存在唯一性：一般地 $\det(M) = (2B-2\gamma)(2B+\gamma)^2$，当 $\gamma < B$ 时
$\det(M)\neq 0$，方程组有唯一解；当 $\gamma \to B$ 时矩阵奇异、解发散（这与比较
静态中 γ 扫描的发散现象一致）。代码用 `numpy.linalg.solve(M, b)` 求解。

## 6. 期望均衡结果（用于验证）

- $p^* \approx (7.38,\ 7.54,\ 6.98)$
- $Q^* \approx (9.76,\ 9.28,\ 10.96)$
- $\pi^* \approx (47.63,\ 43.06,\ 60.06)$

注：以上为保留两位小数的四舍五入值；`tests/test_model.py` 中以 $\text{atol}\approx 0.01$
对解析解进行断言验证。
