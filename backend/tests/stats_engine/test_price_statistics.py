import pytest
from app.statistical_engine.stats.price_statistics import price_stats_module
from app.statistical_engine.core.exceptions import InvalidStatisticalInputException

def test_price_relative_normal():
    # Base price 50, current price 65 -> Relative = (65 / 50) * 100 = 130.0%
    res = price_stats_module.price_relative(current_price=65.0, base_price=50.0)
    assert res.result == 130.0
    assert res.unit == "percent"
    assert "P_1 / P_0" in res.formula

def test_price_relative_zero_base_price():
    with pytest.raises(InvalidStatisticalInputException) as exc_info:
        price_stats_module.price_relative(current_price=60.0, base_price=0.0)
    assert exc_info.value.code == "INVALID_STATISTICAL_INPUT"

def test_price_relative_negative_price():
    with pytest.raises(InvalidStatisticalInputException):
        price_stats_module.price_relative(current_price=-10.0, base_price=50.0)

def test_inflation_rate_positive():
    # CPI increased from 150 to 165 -> ((165 - 150) / 150) * 100 = 10.0%
    res = price_stats_module.inflation_rate(current_index=165.0, previous_index=150.0)
    assert res.result == 10.0
    assert res.unit == "percent"

def test_inflation_rate_deflation():
    # Deflation from 200 to 190 -> ((190 - 200) / 200) * 100 = -5.0%
    res = price_stats_module.inflation_rate(current_index=190.0, previous_index=200.0)
    assert res.result == -5.0

def test_inflation_rate_zero_previous_index():
    with pytest.raises(InvalidStatisticalInputException):
        price_stats_module.inflation_rate(current_index=160.0, previous_index=0.0)

def test_weighted_mean_calculation():
    # Values: [110, 120, 130], Weights: [50, 30, 20]
    # Weighted sum = 5500 + 3600 + 2600 = 11700. Sum of weights = 100.
    # Result = 117.0
    res = price_stats_module.weighted_mean(values=[110.0, 120.0, 130.0], weights=[50.0, 30.0, 20.0])
    assert res.result == 117.0

def test_weighted_mean_length_mismatch():
    with pytest.raises(InvalidStatisticalInputException):
        price_stats_module.weighted_mean(values=[100.0, 120.0], weights=[50.0])

def test_weighted_mean_negative_weights():
    with pytest.raises(InvalidStatisticalInputException):
        price_stats_module.weighted_mean(values=[100.0, 120.0], weights=[50.0, -10.0])

def test_laspeyres_index():
    # 2 commodities:
    # Base prices p0 = [10, 20], base quantities q0 = [5, 10] -> p0*q0 = 50 + 200 = 250
    # Current prices p1 = [12, 25] -> p1*q0 = 60 + 250 = 310
    # Laspeyres = (310 / 250) * 100 = 124.0
    res = price_stats_module.laspeyres_index(
        base_prices=[10.0, 20.0],
        current_prices=[12.0, 25.0],
        base_quantities=[5.0, 10.0]
    )
    assert res.result == 124.0

def test_paasche_index():
    # 2 commodities:
    # Base prices p0 = [10, 20], current quantities q1 = [6, 8] -> p0*q1 = 60 + 160 = 220
    # Current prices p1 = [12, 25] -> p1*q1 = 72 + 200 = 272
    # Paasche = (272 / 220) * 100 = 123.6364
    res = price_stats_module.paasche_index(
        base_prices=[10.0, 20.0],
        current_prices=[12.0, 25.0],
        current_quantities=[6.0, 8.0]
    )
    assert abs(res.result - 123.6364) < 0.001

def test_fisher_ideal_index():
    # Laspeyres = 124.0, Paasche = 121.0
    # Fisher = sqrt(124 * 121) = sqrt(15004) = 122.4908
    res = price_stats_module.fisher_index(laspeyres=124.0, paasche=121.0)
    assert abs(res.result - 122.4908) < 0.001
    assert "sqrt" in res.formula

def test_real_value_deflation():
    # Nominal wage 60,000, CPI index 120.0 -> Real value = (60,000 / 120.0) * 100 = 50,000.0
    res = price_stats_module.real_value(nominal_value=60000.0, price_index=120.0)
    assert res.result == 50000.0
    assert res.unit == "deflated_currency"
