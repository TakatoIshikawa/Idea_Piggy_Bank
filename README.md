# 価値観の伝播と転向ダイナミクスモデル (Value_Transmission_and_Switching_Dynamic Model)

このリポジトリは、親の影響と対立の下で子どもたちの価値観が空間的に拡散し、世間の圧力に応じて転向していく社会的ダイナミクスを再現するシミュレーションを実装しています。本モデルは、反応拡散系の枠組みに非線形の転向（スイッチング）項を加えたものです。

---

## モデルの概要

シミュレーションでは、2次元グリッド上の各セルを「子ども」とみなし、セル内の値として以下の2種類の変数を用います。

- **$C_A(x,y,t)$**：位置 $(x,y)$、時刻 $t$ における、親Aに沿った価値観の強さ  
- **$C_B(x,y,t)$**：同じく親Bに沿った価値観の強さ

グリッドは空間的に分割され、左半分は親Aの支配下、右半分は親Bの支配下とされています。各セルは、所属する親（A または B）の固定された影響（バイナリマスク $A(x,y)$ または $B(x,y)$）を受け、時間とともに増大して飽和する影響 $S(t)$ の下で変化します。また、隣接セルとの価値観の違いが閾値 $\delta$ を超えると転向が起こります。

子どもたちの価値観は、以下の3つの要素によって進化します。

1. **拡散 (Diffusion)**  
   隣接セルとの相互作用を通じて価値観が空間的に広がる。  
   空間離散化は有限差分法（ラプラシアン）で表現される。

2. **親の影響 (Parental Influence)**  
   各セルは、所属する親の価値観に引き寄せられる。  
   この効果は、バイナリマスクと $S(t)$ により実現され、$S(t)$ は sigmoid 関数で飽和するようにモデル化される。

3. **転向 (Conversion/Switching)**  
   セル内および周囲との価値観の差が一定の閾値 $\delta$ を超える場合、値が非線形的に転向する。  
   転向率は sigmoid 関数で滑らかに制御され、例えば以下の形で表される：

   $$
   \theta_{A \to B}\left( C_A,C_B \right) = \beta\,C_A\,\sigma\Bigl(|C_A - C_B| - \delta\Bigr)
   $$

   $$
   \theta_{B \to A}\left( C_B,C_A \right) = \beta\,C_B\,\sigma\Bigl(|C_A - C_B| - \delta\Bigr)
   $$

   ここで、$\sigma(z)=\frac{1}{1+\exp(-k_{\text{sig}}\,z)}$ です。

---

## 数学的なモデル表現

モデルの状態変数 $C_A(x,y,t)$ および $C_B(x,y,t)$ の時間発展は、次の偏微分方程式 (PDE) で記述されます：

$$
\frac{\partial C_A}{\partial t}(x,y,t) = D_A\,\nabla^2 C_A(x,y,t) + \alpha \Bigl( A(x,y)\,S(t) - C_A(x,y,t) \Bigr) - \theta_{A \to B}\left( C_A, C_B \right)
$$

$$
\frac{\partial C_B}{\partial t}(x,y,t) = D_B\,\nabla^2 C_B(x,y,t) + \alpha \Bigl( B(x,y)\,S(t) - C_B(x,y,t) \Bigr) - \theta_{B \to A}\left( C_B, C_A \right)
$$

**各項の意味:**

- **拡散項**:  
  $D_A\,\nabla^2 C_A(x,y,t)$ および $D_B\,\nabla^2 C_B(x,y,t)$  
  ここで、$\nabla^2$ は隣接セル間の値の差分（有限差分法で近似）を用いたラプラシアン演算子です。

- **親の影響項**:  
  $\alpha \Bigl( A(x,y)\,S(t) - C_A(x,y,t) \Bigr)$  
  $A(x,y)$（または $B(x,y)$）は、各領域での親の影響を示すバイナリマスクです。  
  $S(t)$ は、親の影響が時間とともに増加し、最終的に最大値に飽和する様子を示す関数で、一般には以下のように表されます：

  $$
  S(t) = \text{max\_strength} \cdot \frac{1}{1+\exp\bigl(-k\,(t-t_0)\bigr)}
  $$

- **転向項**:  
  転向項は、セル内およびその周囲での価値観の差が大きい場合に働く項です。  
  例えば、

  $$
  \theta_{A \to B}\left( C_A,C_B\right) = \beta\,C_A\,\sigma\Bigl(|C_A - C_B|-\delta\Bigr)
  $$

  $$
  \theta_{B \to A}\left( C_B,C_A\right) = \beta\,C_B\,\sigma\Bigl(|C_A - C_B|-\delta\Bigr)
  $$

  と表され、$\beta$ は転向の強さ、$\delta$ は転向の閾値、$\sigma(z)=\frac{1}{1+\exp(-k_{\text{sig}}\,z)}$ は転向を滑らかに調節するシグモイド関数です。

---

## 想定される状況

このモデルは、以下のような社会現象やシナリオを模擬することを意図しています：

- **地域ごとの文化・価値観の違い**：  
  左側は親A（例えば伝統的または保守的な価値観）、右側は親B（例えば革新的または進歩的な価値観）が固定されている。

- **価値観の拡散と交流**：  
  子どもたちは、周囲との相互作用を通じてその価値観が空間的に広がり、隣接領域との対立から混合領域が形成されることがある。

- **社会的圧力による転向**：  
  あるセル内で、隣接する領域との差が一定の閾値 $\delta$ を超えると、子どもたちは周囲の影響を受けて価値観を転向する。

- **ダイナミックな文化・思想の変遷**：  
  パラメータの設定に応じて、ある地域の価値観が支配的になったり、分極化や混合状態が生じたりする現象を再現可能です。

---

## 数値解法と実装

- **空間離散化**:  
  2次元グリッド上で有限差分法を用いてラプラシアンを近似する。

- **時間離散化**:  
  Euler 法を用いて、各時間ステップ $dt$ ごとに状態を更新する。

- **初期条件**:  
  グリッドの左半分に $C_A=1$、右半分に $C_B=1$ を設定し、親の影響マスク（$A(x,y)$ および $B(x,y)$）を左右で固定することで、初期に明確な分断状態を実現する。

- **可視化**:  
  Matplotlib のアニメーション機能を用いて、各時間ステップごとに $C_A$、$C_B$、およびその差分 $C_A-C_B$ の空間分布を表示する。

---

## 利用方法

リポジトリをクローンして、シミュレーションスクリプトを実行してください。アニメーションでは以下の情報が表示されます：

- **左パネル**：$C_A$（親Aの価値観の分布）
- **中央パネル**：$C_B$（親Bの価値観の分布）
- **右パネル**：$C_A-C_B$（境界および転向の状況）

また、各種パラメータ（拡散係数、親の影響強度、転向の閾値など）を変更することで、文化の浸透、思想の分極、混合領域の形成など、さまざまな社会的ダイナミクスのシナリオを検証することができます。

---

---------------------------------- English ver. ---------------------------------

# Value_Transmission_and_Switching_Dynamic Model

This repository contains a simulation that replicates the social dynamics in which children's values diffuse across a spatial domain under the influence and conflict of their parents, ultimately shifting in response to societal pressures. The model is implemented using a reaction-diffusion framework with additional nonlinear switching (conversion) terms.

## Model Description

### 1. Overview

The simulation considers a two-dimensional grid where:
- The left region is influenced by **Parent A** and the right region by **Parent B**.
- Each cell on the grid represents a "child" whose values are modeled by two variables:
  - **$C_A(x,y,t)$**: The strength of values aligned with Parent A at position $(x,y)$ and time $t$.
  - **$C_B(x,y,t)$**: The strength of values aligned with Parent B.

Children's values evolve over time due to:
- **Diffusion**: Values spread to neighboring cells.
- **Parental Influence**: Children tend to adopt the values of the parent in their respective region.
- **Conversion (Switching)**: When the difference between a cell's value and that of its surroundings exceeds a threshold $\delta$, a nonlinear switching term facilitates conversion.

### 2. Mathematical Formulation

The evolution of the state variables is described by the following partial differential equations (PDEs):

$$
\frac{\partial C_A}{\partial t}(x,y,t) = D_A\,\nabla^2 C_A(x,y,t) + \alpha \Bigl( A(x,y)\,S(t) - C_A(x,y,t) \Bigr) - \theta_{A \to B}\bigl( C_A, C_B \bigr)
$$

$$
\frac{\partial C_B}{\partial t}(x,y,t) = D_B\,\nabla^2 C_B(x,y,t) + \alpha \Bigl( B(x,y)\,S(t) - C_B(x,y,t) \Bigr) - \theta_{B \to A}\bigl( C_B, C_A \bigr)
$$

**Explanation of each term:**

- **Diffusion Term**:  
  The Laplacian operator $\nabla^2$ is computed via finite differences, and $D_A$ and $D_B$ are the diffusion coefficients for $C_A$ and $C_B$, respectively.

- **Parental Influence Term**:  
  $A(x,y)$ and $B(x,y)$ are binary masks indicating the regions dominated by Parent A (left half) and Parent B (right half). $S(t)$ is a bounded, increasing function (modeled by a sigmoid) representing the strengthening of parental influence over time:

  $$
  S(t) = \text{max\_strength} \cdot \frac{1}{1+\exp\bigl(-k\,(t-t_0)\bigr)}
  $$

- **Conversion (Switching) Term**:  
  Conversion is modeled by:

  $$
  \theta_{A \to B}\bigl( C_A, C_B \bigr) = \beta \, C_A \, \sigma\Bigl(|C_A-C_B|-\delta\Bigr)
  $$

  $$
  \theta_{B \to A}\bigl( C_B, C_A \bigr) = \beta \, C_B \, \sigma\Bigl(|C_A-C_B|-\delta\Bigr)
  $$

  where $\beta$ is the switching strength, $\delta$ is the threshold for conversion, and $\sigma(z)=\frac{1}{1+\exp(-k_{\text{sig}}z)}$ is a sigmoid function that smoothly modulates the conversion based on the difference $|C_A-C_B|$.

### 3. Numerical Implementation

The simulation uses the Euler method for time integration and finite differences to approximate the Laplacian on the grid. The grid is initialized with:
- $C_A = 1$ on the left half.
- $C_B = 1$ on the right half.

Parental influence is fixed using binary masks, ensuring that the left side is always dominated by Parent A and the right side by Parent B.

## Scenario Assumptions

This model is designed to mimic social dynamics where:
- **Parental Influence and Culture**: Two distinct parental (or cultural) paradigms are imposed on different spatial regions.
- **Value Diffusion**: Over time, individuals (children) interact with their neighbors, causing values to diffuse across space.
- **Conversion due to Social Pressure**: Individuals may convert if the difference between their value and that of their surroundings exceeds a threshold.
- **Dynamic Equilibrium and Pattern Formation**: Depending on parameters (e.g., diffusion rates, parental influence strength, switching threshold), the system can evolve toward uniformity, persistent boundaries, or complex spatial patterns such as ideological polarization or cultural drift.

## How to Use

Clone the repository and run the simulation script. The animation will display:
- **Left Panel**: Distribution of $C_A$ (values aligned with Parent A).
- **Middle Panel**: Distribution of $C_B$ (values aligned with Parent B).
- **Right Panel**: The difference $(C_A-C_B)$ indicating boundaries and conversion regions.

You can modify parameters such as the diffusion coefficients, parental influence strength, switching threshold, and sigmoid parameters to explore various social dynamics scenarios.

---

## License

This project is licensed under the MIT License.
