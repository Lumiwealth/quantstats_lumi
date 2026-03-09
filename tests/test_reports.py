import os
import tempfile

import pandas as pd

import quantstats_lumi.reports as reports

def test_html_tearsheet():
    # Create a simple returns series with a DatetimeIndex
    index = pd.date_range(start='2022-01-01', periods=5)
    returns = pd.Series([0.01, -0.02, 0.03, -0.04, 0.05], index=index)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp:
        output_file_path = tmp.name
    try:
        reports.html(returns, output=output_file_path)
        assert os.path.exists(output_file_path), "HTML file was not created"
    finally:
        os.remove(output_file_path)

# Test the parameters parameter in the html function
def test_html_tearsheet_parameters():
    # Create a simple returns series with a DatetimeIndex
    index = pd.date_range(start='2022-01-01', periods=5)
    returns = pd.Series([0.01, -0.02, 0.03, -0.04, 0.05], index=index)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp:
        output_file_path = tmp.name

    # Create a set of example parameters
    example_parameters = {
        "symbol": "SPY", # The symbol of the underlying asset
        "idle_holding_symbol": "QQQ", # We will put a portion of the portfolio in this symbol the whole time, set to None to not use this feature
        "idle_holding_pct": 0.25, # The percentage of the portfolio to put in the idle holding symbol
        "days_to_expiry": 0,  # The number of days to expiry 
        "strike_step_size": 1,  # How far apart each strike should be
        "min_wing_size": 2,  # The minimum spread between the wings
        "time_to_start": "10:30",  # The time to start trading
        "max_loss": 0.25,  # The maximum loss to take before getting out of the trade
        "first_adjustment_loss": 0.10,  # The first adjustment to make if the trade goes against us
        "take_profit": 0.15,  # The profit to take before getting out of the trade
        "pct_to_trade": 0.35,  # The percentage of the portfolio to trade
        "time_to_close": "15:30",  # The time to close the trade
        "days_of_week_to_trade": "01234",  # The days of the week to trade, where 0 is Monday and 4 is Friday
        "wing_size_adjustment": 0,  # The amount to adjust the wing size by (0.1 = 10%)
        "max_adx": 40,  # The maximum ADX value to create a butterfly (ADX is a trend strength indicator)
        "min_gamma_risk": 0,  # The minimum gamma risk to take on the trade (it will only take a trade if the gamma risk is greater than this value)
        "expected_iv_collapse": 2.5,  # The expected implied volatility collapse
        "adx_length": 14,  # The length of the ADX indicator
        "take_profit_trailing_stop": 0.02,  # The trailing stop to use for the take profit, after the take profit target is hit, set to None to not use this feature
    }

    try:
        reports.html(returns, output=output_file_path, parameters=example_parameters)
        assert os.path.exists(output_file_path), "HTML file was not created"
    finally:
        os.remove(output_file_path)


def test_metrics_json_basic():
    """Test metrics_json returns expected structure with scalar metrics and time series."""
    index = pd.date_range(start='2020-01-01', periods=500, freq='B')
    returns = pd.Series([0.001] * 250 + [-0.001] * 250, index=index)

    result = reports.metrics_json(returns)

    # Check top-level keys
    assert "metadata" in result
    assert "scalar_metrics" in result
    assert "time_series" in result
    assert "aggregated" in result
    assert "drawdowns" in result

    # Check metadata
    assert result["metadata"]["start_date"] is not None
    assert result["metadata"]["end_date"] is not None
    assert result["metadata"]["total_days"] == 500

    # Check scalar metrics has expected keys
    sm = result["scalar_metrics"]
    assert len(sm) > 10, f"Expected at least 10 scalar metrics, got {len(sm)}"

    # Check time series has expected keys
    ts = result["time_series"]
    assert "cumulative_returns" in ts
    assert "daily_returns" in ts
    assert len(ts["cumulative_returns"]) == 500
    assert len(ts["daily_returns"]) == 500


def test_metrics_json_with_benchmark():
    """Test metrics_json with benchmark returns."""
    index = pd.date_range(start='2020-01-01', periods=200, freq='B')
    returns = pd.Series([0.002] * 200, index=index)
    benchmark = pd.Series([0.001] * 200, index=index)

    result = reports.metrics_json(returns, benchmark=benchmark)

    ts = result["time_series"]
    assert "benchmark_cumulative_returns" in ts
    assert len(ts["benchmark_cumulative_returns"]) > 0


def test_metrics_json_file_output():
    """Test metrics_json writes to file when output path is provided."""
    import json
    index = pd.date_range(start='2020-01-01', periods=100, freq='B')
    returns = pd.Series([0.001] * 100, index=index)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tmp:
        output_path = tmp.name

    try:
        result = reports.metrics_json(returns, output=output_path)
        assert os.path.exists(output_path), "JSON file was not created"

        with open(output_path, "r") as f:
            loaded = json.load(f)

        assert loaded["metadata"]["total_days"] == 100
        assert "scalar_metrics" in loaded
        assert "time_series" in loaded
    finally:
        os.remove(output_path)


def test_metrics_json_drawdowns():
    """Test that drawdown details are included."""
    # Create returns with a clear drawdown
    index = pd.date_range(start='2020-01-01', periods=100, freq='B')
    returns = pd.Series(
        [0.01] * 30 + [-0.03] * 10 + [0.01] * 60,
        index=index
    )

    result = reports.metrics_json(returns)
    assert isinstance(result["drawdowns"], list)
    # Should detect at least one drawdown
    if len(result["drawdowns"]) > 0:
        dd = result["drawdowns"][0]
        assert "start" in dd
        assert "max drawdown" in dd


def test_html_tearsheet_uses_log_scale_chart_instead_of_volatility_matched():
    index = pd.date_range(start="2022-01-01", periods=20, freq="D")
    returns = pd.Series([0.01] * 20, index=index, name="strategy")
    benchmark = pd.Series([0.005] * 20, index=index, name="benchmark")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp:
        output_file_path = tmp.name

    try:
        reports.html(returns, benchmark=benchmark, output=output_file_path)
        with open(output_file_path, "r", encoding="utf-8") as f:
            html = f.read()

        # The tearsheet should no longer include the confusing volatility-matched chart.
        assert "Volatility Matched" not in html
        # The log-scaled chart includes this string in its title.
        assert "Log Scaled" in html
    finally:
        os.remove(output_file_path)
