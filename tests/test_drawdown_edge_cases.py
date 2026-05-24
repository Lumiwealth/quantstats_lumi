import numpy as np
import pandas as pd

import quantstats_lumi.stats as stats


def test_max_drawdown_counts_first_negative_return():
    returns = pd.Series(
        [-0.10, 0.00, 0.05],
        index=pd.date_range("2026-01-01", periods=3, freq="D"),
    )

    assert np.isclose(stats.max_drawdown(returns), -0.10)
    assert np.isclose(stats.to_drawdown_series(returns).iloc[0], -0.10)


def test_max_drawdown_counts_first_negative_return_per_dataframe_column():
    returns = pd.DataFrame(
        {
            "first_day_loss": [-0.10, 0.00, 0.05],
            "first_day_gain": [0.10, -0.05, 0.00],
        },
        index=pd.date_range("2026-01-01", periods=3, freq="D"),
    )

    max_dd = stats.max_drawdown(returns)
    dd_series = stats.to_drawdown_series(returns)

    assert np.isclose(max_dd["first_day_loss"], -0.10)
    assert np.isclose(dd_series["first_day_loss"].iloc[0], -0.10)
    assert max_dd["first_day_gain"] < 0
