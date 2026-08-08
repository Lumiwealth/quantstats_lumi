import math

import numpy as np
import pandas as pd
import pytest

from quantstats_lumi import stats

# Reference values computed with the numguard reference implementation of
# Bailey & Lopez de Prado (2014), fed the same pandas sample moments
# (ddof=1 Sharpe, sample skew, excess kurtosis + 3).
RETURNS = pd.Series(
    [0.003 + 0.01 * math.sin(i) + 0.004 * math.cos(3 * i) for i in range(90)]
)


def test_expected_max_sharpe_matches_reference():
    assert stats.expected_max_sharpe(25, 0.1) == pytest.approx(
        0.19971498869597204, abs=1e-9
    )
    assert stats.expected_max_sharpe(1, 0.1) == 0.0
    with pytest.raises(ValueError):
        stats.expected_max_sharpe(0, 0.1)


def test_deflated_sharpe_matches_reference():
    assert stats.deflated_sharpe_ratio(RETURNS, trials=25) == pytest.approx(
        0.9644939726778046, abs=1e-7
    )
    assert stats.deflated_sharpe_ratio(RETURNS, trials=250) == pytest.approx(
        0.8377547697411925, abs=1e-7
    )


def test_single_trial_reduces_to_no_deflation():
    # with one trial the bar is zero: pure probabilistic Sharpe vs 0
    assert stats.deflated_sharpe_ratio(RETURNS, trials=1) == pytest.approx(
        0.9999130107460131, abs=1e-7
    )


def test_deflation_is_monotonic_in_trials():
    values = [
        stats.deflated_sharpe_ratio(RETURNS, trials=n) for n in (1, 10, 100, 1000)
    ]
    assert all(values[i] > values[i + 1] for i in range(len(values) - 1))


def test_insufficient_observations_returns_nan():
    assert np.isnan(stats.deflated_sharpe_ratio(RETURNS.head(2), trials=10))
