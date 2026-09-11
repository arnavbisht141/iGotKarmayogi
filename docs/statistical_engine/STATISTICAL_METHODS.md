# Statistical Methods Reference — Price Statistics Module

This document defines the mathematical formulas, assumptions, units, constraints, and algorithmic logic implemented in the `PriceStatisticsModule`.

---

## 1. Price Relative (R)

- **Skill ID**: `price.price_relative`
- **Definition**: The ratio of the price of a specific commodity in the current period to its price in the base period, expressed as a percentage.
- **Formula**:
  $$R = \left(\frac{P_1}{P_0}\right) \times 100$$
- **Inputs**:
  - `current_price` ($P_1$): Price in current period ($P_1 \ge 0$).
  - `base_price` ($P_0$): Price in base period ($P_0 > 0$).
- **Unit**: `percent`
- **Validation Constraints**:
  - $P_0$ must be strictly greater than zero to avoid division by zero.
  - $P_1$ cannot be negative.
- **Rounding Policy**: 4 decimal places internally, presented as 2 decimal places.

---

## 2. Inflation Rate

- **Skill ID**: `price.inflation_rate`
- **Definition**: Percentage rate of change of a price index (CPI or WPI) over a specified time interval (monthly or annually).
- **Formula**:
  $$\text{Inflation} = \left(\frac{I_t - I_{t-1}}{I_{t-1}}\right) \times 100$$
- **Inputs**:
  - `current_index` ($I_t$): Price index in current period.
  - `previous_index` ($I_{t-1}$): Price index in base/prior period ($I_{t-1} > 0$).
- **Unit**: `percent`
- **Validation Constraints**:
  - $I_{t-1}$ must be strictly positive.

---

## 3. Weighted Average of Price Relatives (CPI)

- **Skill ID**: `price.cpi.weighted_price_relatives`
- **Definition**: Consumer Price Index computed as the weighted arithmetic mean of individual commodity price relatives using expenditure weights.
- **Formula**:
  $$\text{CPI} = \frac{\sum (W_i \times R_i)}{\sum W_i}$$
- **Inputs**:
  - `relatives`: Array of commodity price relatives $[R_1, R_2, \dots, R_n]$.
  - `weights`: Array of corresponding expenditure weights $[W_1, W_2, \dots, W_n]$.
- **Unit**: `index_points`
- **Validation Constraints**:
  - Lengths of `relatives` and `weights` must be identical and $> 0$.
  - All weights must be non-negative, and $\sum W_i > 0$.

---

## 4. Laspeyres Price Index ($I_L$)

- **Skill ID**: `price.laspeyres_index`
- **Definition**: Fixed-base weighted price index using base-period consumption quantities as weights.
- **Formula**:
  $$I_L = \frac{\sum (p_1 \times q_0)}{\sum (p_0 \times q_0)} \times 100$$
- **Inputs**:
  - `base_prices` ($p_0$): Array of base period prices.
  - `current_prices` ($p_1$): Array of current period prices.
  - `base_quantities` ($q_0$): Array of base period quantities.
- **Unit**: `index_points`
- **Validation Constraints**:
  - Equal length arrays ($n \ge 1$).
  - $\sum (p_0 \times q_0) > 0$.

---

## 5. Paasche Price Index ($I_P$)

- **Skill ID**: `price.paasche_index`
- **Definition**: Current-weighted price index using current-period quantities as dynamic weights.
- **Formula**:
  $$I_P = \frac{\sum (p_1 \times q_1)}{\sum (p_0 \times q_1)} \times 100$$
- **Inputs**:
  - `base_prices` ($p_0$), `current_prices` ($p_1$), `current_quantities` ($q_1$).
- **Unit**: `index_points`

---

## 6. Fisher's Ideal Index ($I_F$)

- **Skill ID**: `price.fisher_index`
- **Definition**: The geometric mean of the Laspeyres and Paasche price indices. Satisfies time-reversal and factor-reversal tests.
- **Formula**:
  $$I_F = \sqrt{I_L \times I_P}$$
- **Inputs**:
  - `laspeyres` ($I_L \ge 0$), `paasche` ($I_P \ge 0$).
- **Unit**: `index_points`

---

## 7. Real vs Nominal Value Deflation

- **Skill ID**: `price.real_vs_nominal`
- **Definition**: Converting nominal monetary indicators into constant-price real economic measures using an index deflator.
- **Formula**:
  $$\text{Real Value} = \left(\frac{\text{Nominal Value}}{\text{Price Index}}\right) \times 100$$
- **Inputs**:
  - `nominal_value`, `price_index` ($> 0$).
- **Unit**: `deflated_currency`
