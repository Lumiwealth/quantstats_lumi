"""Return preparation must not inspect source files merely to identify its caller."""
import inspect

import pandas as pd
import pytest

from quantstats_lumi import utils


@pytest.mark.parametrize("rf", [0.0, 0.01])
def test_return_preparation_avoids_full_stack_walk(monkeypatch, rf):
    def forbidden_stack(*args, **kwargs):
        raise AssertionError("Full stack/source inspection is unnecessary")
    monkeypatch.setattr(inspect, "stack", forbidden_stack)
    data = pd.Series([0.03, -0.02, 0.01])
    result = utils._prepare_returns(data, rf=rf)
    pd.testing.assert_series_equal(result, data - rf)


@pytest.mark.parametrize("caller", ["cagr", "_prepare_benchmark", "gain_to_pain_ratio", "rolling_volatility"])
def test_existing_callers_still_avoid_double_risk_free_subtraction(caller):
    # Construct the existing function-name contract without importing report code.
    namespace = {"utils": utils}
    exec(f"def {caller}(data):\n    return utils._prepare_returns(data, rf=0.01)\n", namespace)
    data = pd.Series([0.03, -0.02, 0.01])
    pd.testing.assert_series_equal(namespace[caller](data), data)
