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


def test_missing_observations_are_not_counted_as_evidence():
    # `sharpe` fills gaps with zero, `skew` and `kurtosis` skip them. Scored on the
    # union, a gap-ridden series would inherit a larger n -- and n only ever enters
    # to say how much the sample pins down.
    with_gaps = RETURNS.copy()
    with_gaps.iloc[[5, 17, 31, 48, 72]] = np.nan

    assert stats.deflated_sharpe_ratio(
        with_gaps, trials=25
    ) == pytest.approx(stats.deflated_sharpe_ratio(with_gaps.dropna(), trials=25))


def test_padding_with_missing_rows_does_not_raise_the_score():
    padded = pd.concat([RETURNS, pd.Series([np.nan] * 400)], ignore_index=True)

    assert stats.deflated_sharpe_ratio(padded, trials=25) == pytest.approx(
        stats.deflated_sharpe_ratio(RETURNS, trials=25)
    )


def test_each_column_is_judged_on_its_own_dispersion():
    # Reducing the frame to one scalar deviation let a flat column ride on its
    # neighbour's movement -- the same certainty-from-nothing the scalar guard closed.
    frame = pd.DataFrame({"real": RETURNS, "flat": [0.001] * len(RETURNS)})
    result = stats.deflated_sharpe_ratio(frame, trials=25)

    assert isinstance(result, pd.Series)
    assert list(result.index) == ["real", "flat"]
    assert np.isnan(result["flat"])
    assert result["real"] == pytest.approx(
        stats.deflated_sharpe_ratio(RETURNS, trials=25)
    )


def test_a_quiet_column_is_not_failed_by_a_loud_neighbour():
    quiet = pd.Series(np.random.default_rng(1).normal(0, 1e-8, len(RETURNS)))
    frame = pd.DataFrame({"loud": RETURNS * 1000, "quiet": quiet})
    result = stats.deflated_sharpe_ratio(frame, trials=25)

    assert 0 <= result["quiet"] <= 1
    assert result["quiet"] == pytest.approx(
        stats.deflated_sharpe_ratio(quiet, trials=25)
    )


@pytest.mark.parametrize(
    "series",
    [RETURNS.head(2), pd.Series([0.001] * 250), RETURNS],
    ids=["too-short", "no-dispersion", "usable"],
)
def test_an_invalid_trial_count_is_rejected_whatever_the_data(series):
    # Otherwise an unusable series answers nan and the caller never learns that the
    # trial count they passed was the actual problem.
    with pytest.raises(ValueError):
        stats.deflated_sharpe_ratio(series, trials=0)
