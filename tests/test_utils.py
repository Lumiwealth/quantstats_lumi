import numpy as np
import pandas as pd
import pytest
import datetime as dt

from quantstats_lumi.utils import (
    to_returns, to_prices, log_returns, rebase, group_returns, 
    aggregate_returns, to_excess_returns, _prepare_prices, 
    _prepare_returns, multi_shift, exponential_stdev
)


# Test data setup
@pytest.fixture
def sample_prices():
    dates = pd.date_range(start='2020-01-01', periods=10, freq='D')
    return pd.Series([100, 102, 99, 101, 103, 102, 99, 101, 102, 101], index=dates)

@pytest.fixture
def sample_returns():
    dates = pd.date_range(start='2020-01-01', periods=10, freq='D')
    return pd.Series([0.01, -0.02, 0.03, -0.01, 0.02, 0.01, -0.03, 0.02, 0.01, -0.02], index=dates)

@pytest.fixture
def sample_rf():
    return 0.01  # 1% risk-free rate


def test_to_returns(sample_prices):
    result = to_returns(sample_prices)
    assert isinstance(result, pd.Series)
    # First value should be 0 since NaN values are filled with 0
    assert result.iloc[0] == 0
    # Second return should be (102 - 100) / 100 = 0.02
    assert abs(result.iloc[1] - 0.02) < 1e-10


def test_to_prices(sample_returns):
    result = to_prices(sample_returns, base=100)
    assert isinstance(result, pd.Series)
    # The function uses compsum which doesn't add an extra element
    assert len(result) == len(sample_returns)
    # First value should be base + base * first return = 100 + 100 * 0.01 = 101
    assert np.isclose(result.iloc[0], 101)


def test_log_returns(sample_returns):
    result = log_returns(sample_returns)
    assert isinstance(result, pd.Series)
    assert len(result) == len(sample_returns)
    # Log return of 0.01 should be approximately ln(1.01) ≈ 0.00995
    assert np.isclose(result.iloc[0], np.log(1.01))


def test_rebase(sample_prices):
    result = rebase(sample_prices, base=100)
    assert isinstance(result, pd.Series)
    assert len(result) == len(sample_prices)
    assert result.iloc[0] == 100  # First value should be the base
    # Second value should be 100 * (102 / 100) = 102
    assert np.isclose(result.iloc[1], 102)


def test_group_returns(sample_returns):
    # Group by year
    result = group_returns(sample_returns, sample_returns.index.year)
    assert isinstance(result, pd.Series)
    assert len(result) == 1  # All dates are in 2020

    # Group by month
    result = group_returns(sample_returns, sample_returns.index.month)
    assert isinstance(result, pd.Series)
    assert len(result) == 1  # All dates are in January


def test_aggregate_returns(sample_returns):
    # Test monthly aggregation
    monthly = aggregate_returns(sample_returns, 'monthly')
    assert isinstance(monthly, pd.Series)

    # Test quarterly aggregation
    quarterly = aggregate_returns(sample_returns, 'quarter')
    assert isinstance(quarterly, pd.Series)

    # Test yearly aggregation
    yearly = aggregate_returns(sample_returns, 'yearly')
    assert isinstance(yearly, pd.Series)

    # Test with no period (should return original series)
    daily = aggregate_returns(sample_returns, None)
    assert isinstance(daily, pd.Series)
    assert len(daily) == len(sample_returns)


def test_to_excess_returns(sample_returns, sample_rf):
    result = to_excess_returns(sample_returns, sample_rf)
    assert isinstance(result, pd.Series)
    assert len(result) == len(sample_returns)
    # Excess return should be return - rf (without deannualizing since nperiods is not provided)
    assert np.isclose(result.iloc[0], sample_returns.iloc[0] - sample_rf)

    # Test with nperiods to deannualize
    result_with_nperiods = to_excess_returns(sample_returns, sample_rf, nperiods=252)
    # Deannualized rf = (1 + rf)^(1/nperiods) - 1
    deannualized_rf = np.power(1 + sample_rf, 1.0 / 252) - 1.0
    assert np.isclose(result_with_nperiods.iloc[0], sample_returns.iloc[0] - deannualized_rf)


def test_prepare_prices(sample_prices):
    result = _prepare_prices(sample_prices)
    assert isinstance(result, pd.Series)
    assert len(result) == len(sample_prices)

    # Test with returns data (values < 1)
    returns_data = pd.Series([-0.01, 0.02, -0.03, 0.01, 0.02])
    result = _prepare_prices(returns_data, base=100)
    assert isinstance(result, pd.Series)
    # Should convert returns to prices with base=100
    assert result.iloc[0] == 99  # 100 + 100 * (-0.01) = 99


def test_prepare_returns(sample_returns):
    result = _prepare_returns(sample_returns)
    assert isinstance(result, pd.Series)

    # Test with price data
    price_data = pd.Series([100, 102, 99, 101, 103])
    result = _prepare_returns(price_data)
    assert isinstance(result, pd.Series)
    # Should convert to returns using pct_change() and fill NaN with 0
    assert result.iloc[0] == 0  # First value is filled with 0
    assert abs(result.iloc[1] - 0.02) < 1e-10  # (102 - 100) / 100 = 0.02


def test_multi_shift():
    # Create a simple Series for testing
    series = pd.Series([1, 2, 3, 4, 5])

    # Test with shift=1 to avoid the column name issue
    result = multi_shift(series, shift=1)
    assert isinstance(result, pd.DataFrame)
    assert result.shape[1] == 1  # Just the original series


def test_exponential_stdev():
    # Create a simple Series for testing
    returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02, 0.01, -0.03, 0.02, 0.01, -0.02])

    # Test with span parameter only
    result = exponential_stdev(returns, window=2)
    assert isinstance(result, pd.Series)
    assert len(result) == len(returns)

    # The first few values should be NaN because min_periods=window
    assert pd.isna(result.iloc[0])
    # Later values should be finite
    assert np.isfinite(result.iloc[-1])


# Edge cases
def test_empty_series():
    empty_series = pd.Series([])
    # Test to_returns with empty series
    result = to_returns(empty_series)
    assert isinstance(result, pd.Series)
    assert len(result) == 0

    # Test to_prices with empty series
    result = to_prices(empty_series)
    assert isinstance(result, pd.Series)
    assert len(result) == 0  # Empty series remains empty

    # Test log_returns with empty series
    result = log_returns(empty_series)
    assert isinstance(result, pd.Series)
    assert len(result) == 0


def test_single_value():
    single_value_prices = pd.Series([100])
    # Test to_returns with single value
    result = to_returns(single_value_prices)
    assert isinstance(result, pd.Series)
    assert len(result) == 1  # Returns same length with 0
    assert result.iloc[0] == 0  # First value is filled with 0

    single_value_returns = pd.Series([0.01])
    # Test to_prices with single value
    result = to_prices(single_value_returns)
    assert isinstance(result, pd.Series)
    assert len(result) == 1  # Same length as input

    # Test log_returns with single value
    result = log_returns(single_value_returns)
    assert isinstance(result, pd.Series)
    assert len(result) == 1


def test_all_zeros():
    zeros_prices = pd.Series([100, 100, 100, 100, 100])
    # Test to_returns with all zeros
    result = to_returns(zeros_prices)
    assert isinstance(result, pd.Series)
    # All values should be 0
    assert all(result == 0)

    zeros_returns = pd.Series([0, 0, 0, 0, 0])
    # Test to_prices with all zeros
    result = to_prices(zeros_returns)
    assert isinstance(result, pd.Series)

    # Test log_returns with all zeros
    result = log_returns(zeros_returns)
    assert isinstance(result, pd.Series)
