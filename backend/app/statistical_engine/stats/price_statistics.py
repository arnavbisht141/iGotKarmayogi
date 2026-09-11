import math
from typing import Any, Dict, List, Optional, Union
from app.statistical_engine.stats.base import BaseStatisticalModule
from app.statistical_engine.schemas.stats import CalculationResult
from app.statistical_engine.core.exceptions import InvalidStatisticalInputException

class PriceStatisticsModule(BaseStatisticalModule):
    """
    Deterministic implementation of Price Statistics & Index Number algorithms.
    Aligned with MoSPI and National Statistical Commission (NSC) methodologies.
    """

    def calculate(self, operation: str, inputs: Dict[str, Any]) -> CalculationResult:
        dispatch = {
            "price_relative": self.price_relative,
            "inflation_rate": self.inflation_rate,
            "weighted_mean": self.weighted_mean,
            "weighted_price_relatives": self.weighted_price_relatives,
            "weighted_price_relatives_basket": self.weighted_price_relatives_basket,
            "laspeyres_index": self.laspeyres_index,
            "laspeyres_index_basket": self.laspeyres_index_basket,
            "paasche_index": self.paasche_index,
            "fisher_index": self.fisher_index,
            "real_value": self.real_value,
        }
        if operation not in dispatch:
            raise InvalidStatisticalInputException(
                f"Unknown operation '{operation}' in Price Statistics module.",
                details={"available_operations": list(dispatch.keys())}
            )
        return dispatch[operation](**inputs)

    def price_relative(self, current_price: float, base_price: float) -> CalculationResult:
        """
        Calculate Price Relative (R):
        R = (P_1 / P_0) * 100
        """
        if base_price is None or current_price is None:
            raise InvalidStatisticalInputException("Base price and current price must be provided.")
        if base_price <= 0:
            raise InvalidStatisticalInputException("Base price must be strictly greater than zero.", details={"base_price": base_price})
        if current_price < 0:
            raise InvalidStatisticalInputException("Current price cannot be negative.", details={"current_price": current_price})

        ratio = current_price / base_price
        result = round(ratio * 100.0, 4)

        return CalculationResult(
            operation="price_relative",
            result=result,
            unit="percent",
            formula="R = (P_1 / P_0) * 100",
            steps=[
                f"Ratio = {current_price} / {base_price} = {ratio:.6f}",
                f"Multiply by 100: {ratio:.6f} * 100 = {result:.4f}%"
            ],
            metadata={"base_price": base_price, "current_price": current_price}
        )

    def inflation_rate(
        self,
        current_index: Optional[float] = None,
        previous_index: Optional[float] = None,
        curr_cpi: Optional[float] = None,
        prev_cpi: Optional[float] = None,
        **kwargs
    ) -> CalculationResult:
        """
        Calculate Inflation Rate between two successive periods:
        Inflation = ((I_t - I_t-1) / I_t-1) * 100
        """
        c_idx = current_index if current_index is not None else curr_cpi
        p_idx = previous_index if previous_index is not None else prev_cpi

        if p_idx is None or c_idx is None:
            raise InvalidStatisticalInputException("Both previous and current index values must be provided.")
        if p_idx <= 0:
            raise InvalidStatisticalInputException("Previous index value must be strictly positive.", details={"previous_index": p_idx})

        diff = c_idx - p_idx
        rate = (diff / p_idx) * 100.0
        result = round(rate, 4)

        return CalculationResult(
            operation="inflation_rate",
            result=result,
            unit="percent",
            formula="Inflation = ((Index_t - Index_t-1) / Index_t-1) * 100",
            steps=[
                f"Index change = {c_idx} - {p_idx} = {diff:.4f}",
                f"Relative change = {diff:.4f} / {p_idx} = {diff/p_idx:.6f}",
                f"Percentage change = {result:.4f}%"
            ],
            metadata={"current_index": c_idx, "previous_index": p_idx}
        )

    def weighted_mean(self, values: List[float], weights: List[float]) -> CalculationResult:
        """
        Calculate weighted arithmetic mean:
        W_mean = Σ(w_i * x_i) / Σw_i
        """
        if not values or not weights:
            raise InvalidStatisticalInputException("Values and weights arrays must not be empty.")
        if len(values) != len(weights):
            raise InvalidStatisticalInputException(
                f"Length mismatch: {len(values)} values provided vs {len(weights)} weights.",
                details={"values_len": len(values), "weights_len": len(weights)}
            )
        if any(w < 0 for w in weights):
            raise InvalidStatisticalInputException("Weights cannot be negative.")
        
        sum_weights = sum(weights)
        if sum_weights <= 0:
            raise InvalidStatisticalInputException("Sum of weights must be strictly positive.", details={"sum_weights": sum_weights})

        weighted_sum = sum(v * w for v, w in zip(values, weights))
        result = round(weighted_sum / sum_weights, 4)

        return CalculationResult(
            operation="weighted_mean",
            result=result,
            unit="index_points",
            formula="Σ(w_i * x_i) / Σw_i",
            steps=[
                f"Sum of weighted values: Σ(w * x) = {weighted_sum:.4f}",
                f"Sum of weights: Σw = {sum_weights:.4f}",
                f"Weighted mean = {weighted_sum:.4f} / {sum_weights:.4f} = {result:.4f}"
            ],
            metadata={"sum_weights": sum_weights, "weighted_sum": weighted_sum}
        )

    def weighted_price_relatives(self, relatives: List[float], weights: List[float]) -> CalculationResult:
        """
        Calculate CPI via weighted average of price relatives:
        CPI = Σ(W_i * R_i) / ΣW_i
        """
        res = self.weighted_mean(values=relatives, weights=weights)
        res.operation = "weighted_price_relatives"
        res.formula = "CPI = Σ(W_i * R_i) / ΣW_i"
        return res

    def weighted_price_relatives_basket(
        self,
        rel_food: float,
        rel_housing: float,
        rel_fuel: float,
        w_food: float,
        w_housing: float,
        w_fuel: float
    ) -> CalculationResult:
        """Helper for basket questions."""
        return self.weighted_price_relatives(
            relatives=[rel_food, rel_housing, rel_fuel],
            weights=[w_food, w_housing, w_fuel]
        )

    def laspeyres_index(
        self,
        base_prices: List[float],
        current_prices: List[float],
        base_quantities: List[float]
    ) -> CalculationResult:
        """
        Laspeyres Price Index (Base-weighted):
        I_L = (Σ(p_1 * q_0) / Σ(p_0 * q_0)) * 100
        """
        n = len(base_prices)
        if n == 0 or len(current_prices) != n or len(base_quantities) != n:
            raise InvalidStatisticalInputException(
                "Base prices, current prices, and base quantities must have equal non-zero lengths."
            )
        if any(p < 0 for p in base_prices) or any(p < 0 for p in current_prices) or any(q < 0 for q in base_quantities):
            raise InvalidStatisticalInputException("Prices and quantities cannot be negative.")

        numerator = sum(p1 * q0 for p1, q0 in zip(current_prices, base_quantities))
        denominator = sum(p0 * q0 for p0, q0 in zip(base_prices, base_quantities))

        if denominator <= 0:
            raise InvalidStatisticalInputException("Base period expenditure Σ(p_0 * q_0) must be strictly positive.")

        result = round((numerator / denominator) * 100.0, 4)

        return CalculationResult(
            operation="laspeyres_index",
            result=result,
            unit="index_points",
            formula="I_L = (Σ(p_1 * q_0) / Σ(p_0 * q_0)) * 100",
            steps=[
                f"Numerator Σ(p1 * q0) = {numerator:.4f}",
                f"Denominator Σ(p0 * q0) = {denominator:.4f}",
                f"Laspeyres Index = ({numerator:.4f} / {denominator:.4f}) * 100 = {result:.4f}"
            ],
            metadata={"numerator": numerator, "denominator": denominator}
        )

    def laspeyres_index_basket(
        self,
        p0_a: float, p0_b: float,
        p1_a: float, p1_b: float,
        q0_a: float, q0_b: float
    ) -> CalculationResult:
        """Helper for 2-item basket template."""
        return self.laspeyres_index(
            base_prices=[p0_a, p0_b],
            current_prices=[p1_a, p1_b],
            base_quantities=[q0_a, q0_b]
        )

    def paasche_index(
        self,
        base_prices: List[float],
        current_prices: List[float],
        current_quantities: List[float]
    ) -> CalculationResult:
        """
        Paasche Price Index (Current-weighted):
        I_P = (Σ(p_1 * q_1) / Σ(p_0 * q_1)) * 100
        """
        n = len(base_prices)
        if n == 0 or len(current_prices) != n or len(current_quantities) != n:
            raise InvalidStatisticalInputException(
                "Base prices, current prices, and current quantities must have equal non-zero lengths."
            )
        if any(p < 0 for p in base_prices) or any(p < 0 for p in current_prices) or any(q < 0 for q in current_quantities):
            raise InvalidStatisticalInputException("Prices and quantities cannot be negative.")

        numerator = sum(p1 * q1 for p1, q1 in zip(current_prices, current_quantities))
        denominator = sum(p0 * q1 for p0, q1 in zip(base_prices, current_quantities))

        if denominator <= 0:
            raise InvalidStatisticalInputException("Expenditure Σ(p_0 * q_1) must be strictly positive.")

        result = round((numerator / denominator) * 100.0, 4)

        return CalculationResult(
            operation="paasche_index",
            result=result,
            unit="index_points",
            formula="I_P = (Σ(p_1 * q_1) / Σ(p_0 * q_1)) * 100",
            steps=[
                f"Numerator Σ(p1 * q1) = {numerator:.4f}",
                f"Denominator Σ(p0 * q1) = {denominator:.4f}",
                f"Paasche Index = ({numerator:.4f} / {denominator:.4f}) * 100 = {result:.4f}"
            ],
            metadata={"numerator": numerator, "denominator": denominator}
        )

    def fisher_index(self, laspeyres: float, paasche: float) -> CalculationResult:
        """
        Fisher's Ideal Index:
        I_F = sqrt(I_L * I_P)
        """
        if laspeyres is None or paasche is None:
            raise InvalidStatisticalInputException("Both Laspeyres and Paasche index values must be provided.")
        if laspeyres < 0 or paasche < 0:
            raise InvalidStatisticalInputException("Index values cannot be negative.")

        product = laspeyres * paasche
        result = round(math.sqrt(product), 4)

        return CalculationResult(
            operation="fisher_index",
            result=result,
            unit="index_points",
            formula="I_F = sqrt(I_L * I_P)",
            steps=[
                f"Product I_L * I_P = {laspeyres} * {paasche} = {product:.4f}",
                f"Square root = sqrt({product:.4f}) = {result:.4f}"
            ],
            metadata={"laspeyres": laspeyres, "paasche": paasche}
        )

    def real_value(
        self,
        nominal_value: Optional[float] = None,
        price_index: Optional[float] = None,
        nominal_wage: Optional[float] = None,
        cpi_index: Optional[float] = None,
        **kwargs
    ) -> CalculationResult:
        """
        Calculate Real Economic Value deflated by Price Index:
        Real_Value = (Nominal_Value / Price_Index) * 100
        """
        nom = nominal_value if nominal_value is not None else nominal_wage
        idx = price_index if price_index is not None else cpi_index

        if nom is None or idx is None:
            raise InvalidStatisticalInputException("Nominal value and price index must be provided.")
        if idx <= 0:
            raise InvalidStatisticalInputException("Price index must be strictly positive.", details={"price_index": idx})

        real = (nom / idx) * 100.0
        result = round(real, 2)

        return CalculationResult(
            operation="real_value",
            result=result,
            unit="deflated_currency",
            formula="Real_Value = (Nominal_Value / Price_Index) * 100",
            steps=[
                f"Deflation factor = {nom} / {idx} = {nom/idx:.6f}",
                f"Multiply by 100 = {result:.2f}"
            ],
            metadata={"nominal_value": nom, "price_index": idx}
        )

price_stats_module = PriceStatisticsModule()
