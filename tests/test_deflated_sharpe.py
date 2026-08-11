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


def test_zero_dispersion_returns_nan():
    # A constant series has no dispersion, so no Sharpe ratio and no deflated one.
    # Its standard deviation is floating-point residue rather than an exact zero, so
    # the ratio comes out finite (~1e16) and reaches the deflation arithmetic, which
    # answered 1.0 -- certainty of an edge, from the one input that cannot show one.
    # Checked across values and lengths, not at one point: the residue depends on both,
    # so a guard calibrated on a single series passes while still leaking elsewhere.
    for value in (1e-7, 1e-4, 0.001, 0.01, 1.0, 100.0):
        for n in (3, 10, 250, 5000):
            series = pd.Series([value] * n)
            assert np.isnan(
                stats.deflated_sharpe_ratio(series, trials=4)
            ), f"leaked at value={value}, n={n}"
    assert np.isnan(stats.deflated_sharpe_ratio(pd.Series([0.0] * 250), trials=4))

    # The guard is relative to the scale of the data: a real but very quiet series
    # still gets a number.
    quiet = pd.Series(np.random.default_rng(1).normal(0, 1e-8, 250))
    assert 0 <= stats.deflated_sharpe_ratio(quiet, trials=4) <= 1
