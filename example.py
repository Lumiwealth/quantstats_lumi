import pandas as pd
import quantstats_lumi.reports as reports
import os

# Create a simple returns series with a DatetimeIndex
index = pd.date_range(start='2022-01-01', periods=5, freq='M')
returns = pd.Series([0.02, -0.02, 0.03, -0.01, 0.02], index=index)

# Specify the output file path
output_file_path = "report.html"

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

# Generate the HTML report
reports.html(returns, output=output_file_path, parameters=example_parameters)

# Open the HTML file in a browser to visually inspect the output
os.system(f"open {output_file_path}")
