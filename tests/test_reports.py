import os
import tempfile

import numpy as np
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


def test_html_tearsheet_formats_large_metrics_with_commas():
    index = pd.date_range(start="2026-04-07", periods=45, freq="D")
    returns = pd.Series([0.0, -0.10, 2.4] + [0.0] * 42, index=index)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp:
        output_file_path = tmp.name

    try:
        metrics = reports.html(returns, output=output_file_path)
        with open(output_file_path, "r", encoding="utf-8") as f:
            html = f.read()

        assert "," in metrics.loc["CAGR% (Annual Return)", "Strategy"]
        assert "," in metrics.loc["RoMaD", "Strategy"]
        assert metrics.loc["CAGR% (Annual Return)", "Strategy"] in html
        assert metrics.loc["RoMaD", "Strategy"] in html
    finally:
        os.remove(output_file_path)


def test_html_tearsheet_parameters_render_full_width_after_metrics():
    index = pd.date_range(start="2026-04-07", periods=30, freq="D")
    returns = pd.Series([0.01, -0.02, 0.03, 0.01, -0.01] * 6, index=index)
    parameters = {
        "agent_portfolio_manager_agent_model": "gemini-3.1-flash-lite",
        "long_parameter_name_that_should_wrap_instead_of_clip": "<wrapped value>",
    }

    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp:
        output_file_path = tmp.name

    try:
        reports.html(returns, output=output_file_path, parameters=parameters)
        with open(output_file_path, "r", encoding="utf-8") as f:
            html = f.read()

        assert '<div id="bottom-sections">' in html
        assert html.index("Key Performance Metrics") < html.index("Parameters Used")
        assert "long_parameter_name_that_should_wrap_instead_of_clip" in html
        assert "&lt;wrapped value&gt;" in html
    finally:
        os.remove(output_file_path)


def test_html_tearsheet_summary_honors_match_dates_false():
    index = pd.date_range(start="2026-04-06", periods=3, freq="D")
    returns = pd.Series([0.0, -0.01, 0.10], index=index)
    benchmark = pd.Series([0.0, 0.0, 0.01], index=index)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp:
        output_file_path = tmp.name

    try:
        metrics = reports.html(
            returns,
            benchmark=benchmark,
            output=output_file_path,
            match_dates=False,
        )
        payload = reports.metrics_json(
            returns,
            benchmark=benchmark,
            summary_only=True,
            match_dates=False,
        )

        assert metrics.loc["Total Return", "Strategy"] == "9%"
        assert payload["scalar_metrics"]["Total Return"]["Strategy"] == 0.09
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
    sharpe_metric = result["scalar_metrics"].get("Sharpe")
    assert isinstance(sharpe_metric, dict)
    assert len(sharpe_metric.keys()) >= 2


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


def test_metrics_json_summary_only():
    index = pd.date_range(start="2020-01-01", periods=120, freq="B")
    returns = pd.Series([0.002] * 60 + [-0.001] * 60, index=index)

    result = reports.metrics_json(returns, summary_only=True)

    assert "metadata" in result
    assert "scalar_metrics" in result
    assert "time_series" not in result
    assert "aggregated" not in result
    assert "drawdowns" not in result
    assert "summary_tables" in result
    assert result["metadata"]["summary_only"] is True


def test_metrics_json_summary_only_percent_values_use_raw_decimals():
    index = pd.date_range(start="2020-01-01", periods=260, freq="B")
    returns = pd.Series([0.001] * 130 + [-0.0008] * 130, index=index)
    benchmark = pd.Series([0.0007] * 130 + [-0.0006] * 130, index=index)

    result = reports.metrics_json(
        returns,
        benchmark=benchmark,
        summary_only=True,
        rf=0.0369,
    )
    scalar_metrics = result["scalar_metrics"]

    risk_free = scalar_metrics["Risk-Free Rate"]
    assert isinstance(risk_free, dict)
    assert abs(risk_free["Strategy"] - 0.0369) < 1e-12

    positive_months = scalar_metrics["Percent Positive Months"]
    assert isinstance(positive_months, dict)
    assert abs(positive_months["Strategy"] - 0.5) < 1e-12


def test_metrics_json_summary_only_matches_internal_tearsheet_rows_for_key_metrics():
    index = pd.date_range(start="2020-01-01", periods=320, freq="B")
    rng = np.random.default_rng(42)
    strategy = pd.Series(rng.normal(0.0006, 0.01, len(index)), index=index, name="Strategy")
    benchmark = pd.Series(
        (strategy * 0.45).to_numpy() + rng.normal(0.0002, 0.009, len(index)),
        index=index,
        name="Benchmark",
    )

    table = reports.metrics(
        strategy,
        benchmark=benchmark,
        display=False,
        mode="full",
        internal="True",
    )
    payload = reports.metrics_json(
        strategy,
        benchmark=benchmark,
        summary_only=True,
    )
    scalar_metrics = payload["scalar_metrics"]

    def _to_decimal(metric_name, raw_value):
        if raw_value in (None, "", "-"):
            return None
        text = str(raw_value).strip().replace(",", "")
        if text.endswith("%"):
            numeric = float(text[:-1]) / 100.0
        else:
            numeric = float(text)
        if metric_name == "Percent Positive Months" and abs(numeric) > 1.0:
            numeric = numeric / 100.0
        return numeric

    key_metrics = [
        "Total Return",
        "CAGR% (Annual Return)",
        "Max Drawdown",
        "Risk-Free Rate",
        "Correlation",
        "Treynor Ratio",
        "Percent Positive Months",
    ]
    for metric in key_metrics:
        table_value = _to_decimal(metric, table.loc[metric, "Strategy"])
        json_value = scalar_metrics.get(metric)
        if isinstance(json_value, dict):
            json_value = json_value.get("Strategy")
        assert table_value is not None
        assert json_value is not None
        assert abs(float(json_value) - float(table_value)) < 1e-6, metric

    total_return = scalar_metrics["Total Return"]["Strategy"]
    assert total_return != 0.0


def test_metrics_json_summary_only_has_no_percent_strings_in_scalar_values():
    index = pd.date_range(start="2020-01-01", periods=260, freq="B")
    returns = pd.Series([0.002] * 130 + [-0.0015] * 130, index=index)
    benchmark = pd.Series([0.0017] * 130 + [-0.0010] * 130, index=index)

    payload = reports.metrics_json(
        returns,
        benchmark=benchmark,
        summary_only=True,
    )
    scalar_metrics = payload["scalar_metrics"]

    for _, raw_metric_val in scalar_metrics.items():
        values = raw_metric_val.values() if isinstance(raw_metric_val, dict) else [raw_metric_val]
        for value in values:
            if isinstance(value, str):
                assert "%" not in value


def test_metrics_json_custom_metrics():
    index = pd.date_range(start="2020-01-01", periods=80, freq="B")
    returns = pd.Series([0.001] * 80, index=index)

    result = reports.metrics_json(
        returns,
        summary_only=True,
        custom_metrics={"Custom Edge Score": 42.5},
    )

    assert "Custom Edge Score" in result["scalar_metrics"]
    assert result["scalar_metrics"]["Custom Edge Score"] == 42.5


def test_metrics_json_custom_metrics_preserve_numeric_scalars():
    index = pd.date_range(start="2020-01-01", periods=80, freq="B")
    returns = pd.Series([0.001, -0.002, 0.003, -0.001] * 20, index=index)

    result = reports.metrics_json(
        returns,
        summary_only=True,
        custom_metrics={
            "Custom Return Observation Count": int(returns.shape[0]),
            "Custom Mean Absolute Daily Return": float(returns.abs().mean()),
        },
    )

    scalar_metrics = result["scalar_metrics"]
    assert scalar_metrics["Custom Return Observation Count"] == 80
    assert abs(
        float(scalar_metrics["Custom Mean Absolute Daily Return"]) - float(returns.abs().mean())
    ) < 1e-12


def test_metrics_json_output_is_strict_json_with_non_finite_summary_values():
    import json

    index = pd.date_range(start="2020-01-01", periods=40, freq="B")
    returns = pd.Series([0.0] * 40, index=index)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tmp:
        output_path = tmp.name

    try:
        result = reports.metrics_json(
            returns,
            summary_only=True,
            output=output_path,
            custom_metrics={
                "Custom Missing": float("nan"),
                "Nested Nonfinite": {"Strategy": float("inf")},
            },
        )

        assert result["scalar_metrics"]["Custom Missing"] == "-"
        assert result["scalar_metrics"]["Nested Nonfinite"]["Strategy"] == "-"

        with open(output_path, "r", encoding="utf-8") as handle:
            raw = handle.read()
        assert "NaN" not in raw
        assert "Infinity" not in raw
        loaded = json.loads(raw)
        assert loaded["scalar_metrics"]["Custom Missing"] == "-"
    finally:
        os.remove(output_path)


def test_json_sanitize_recursively_removes_non_finite_numbers():
    payload = {
        "plain": float("nan"),
        "nested": [{"value": np.float64("inf")}],
        "array": np.array([1.0, np.nan, -np.inf]),
    }

    assert reports._json_sanitize(payload) == {
        "plain": None,
        "nested": [{"value": None}],
        "array": [1.0, None, None],
    }


def test_summary_only_scalar_metrics_covers_metrics_table_rows():
    index = pd.date_range(start="2020-01-01", periods=260, freq="B")
    returns = pd.Series([0.001] * 130 + [-0.0012] * 130, index=index, name="Strategy")
    benchmark = pd.Series([0.0008] * 130 + [-0.0005] * 130, index=index, name="Benchmark")

    mtrx = reports.metrics(returns, benchmark=benchmark, display=False, mode="full")
    payload = reports.metrics_json(returns, benchmark=benchmark, summary_only=True)
    scalar_metrics = payload["scalar_metrics"]

    # Ignore intentional section separator rows.
    metric_rows = [str(idx) for idx in mtrx.index if not str(idx).startswith("~")]
    missing = [row for row in metric_rows if row not in scalar_metrics]
    assert not missing, f"Missing summary scalar metrics for rows: {missing}"


def test_metrics_table_includes_new_tearsheet_metrics():
    index = pd.date_range(start="2020-01-01", periods=260, freq="B")
    returns = pd.Series([0.001] * 130 + [-0.0012] * 130, index=index)

    table = reports.metrics(returns, display=False, mode="full")

    assert "Worst 1-Month Return" in table.index
    assert "Annualized Return on Risk Capital" in table.index
    assert "Worst 3-Month Return" in table.index
    assert "Time to Recovery (Days)" in table.index
    assert "5th Percentile Tail Loss" in table.index
    assert "Time Underwater (Days)" in table.index
    assert "Percent Positive Months" in table.index


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
