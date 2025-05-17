import pandas as pd
import quantstats_lumi.reports as reports
import os

# Create a returns series with a DatetimeIndex covering 2 years (24 months)
index = pd.date_range(start='2022-01-31', periods=24, freq='M')
strategy_returns = pd.Series(
    [0.02, -0.01, 0.03, -0.01, 0.02, 0.01, -0.01, 0.015, 0.01, -0.005, 0.02, 0.01,
     0.015, -0.01, 0.02, 0.01, -0.01, 0.02, 0.01, -0.01, 0.015, 0.01, -0.005, 0.02],
    index=index,
    name="Strategy"
)

# Create a benchmark returns series (e.g., a bit less volatile and lower mean)
benchmark_returns = pd.Series(
    [0.012, -0.008, -0.018, -0.007, 0.013, 0.008, -0.006, 0.009, 0.007, -0.003, 0.012, 0.008,
     0.009, -0.006, 0.013, 0.008, -0.006, 0.012, -0.008, -0.006, 0.009, 0.007, -0.003, 0.012],
    index=index,
    name="Benchmark"
)

output_file_path = "report_with_benchmark.html"

example_parameters = {
    "symbol": "SPY",
    "idle_holding_symbol": "QQQ",
    "idle_holding_pct": 0.25,
    "days_to_expiry": 0,
    "strike_step_size": 1,
    "min_wing_size": 2,
    "time_to_start": "10:30",
    "max_loss": 0.25,
    "first_adjustment_loss": 0.10,
    "take_profit": 0.15,
    "pct_to_trade": 0.35,
    "time_to_close": "15:30",
    "days_of_week_to_trade": "01234",
    "wing_size_adjustment": 0,
    "max_adx": 40,
    "min_gamma_risk": 0,
    "expected_iv_collapse": 2.5,
    "adx_length": 14,
    "take_profit_trailing_stop": 0.02,
}

# Generate the HTML report for monthly data (periods_per_year=12) with benchmark
html_result = reports.html(
    strategy_returns,
    benchmark=benchmark_returns,
    output=output_file_path,
    parameters=example_parameters,
    periods_per_year=12
)

print(html_result)
os.system(f"open {output_file_path}")
