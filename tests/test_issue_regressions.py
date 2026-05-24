import builtins

import numpy as np
import pandas as pd

import quantstats_lumi.stats as stats
import quantstats_lumi.utils as utils


def test_omega_accepts_series_without_values_attribute_error():
    returns = pd.Series([0.02, -0.01, 0.03, -0.005])

    result = stats.omega(returns)

    assert np.isfinite(result)


def test_conditional_value_at_risk_dataframe_calculates_each_column():
    rng = np.random.default_rng(42)
    data = pd.Series(rng.normal(0.001, 0.02, 1000))
    returns = pd.DataFrame(
        {
            "strategy": data,
            "benchmark": data * 2,
        }
    )

    cvar = stats.conditional_value_at_risk(returns, confidence=0.95, prepare_returns=False)
    var = stats.value_at_risk(returns, confidence=0.95, prepare_returns=False)

    assert isinstance(cvar, pd.Series)
    assert list(cvar.index) == ["strategy", "benchmark"]
    assert not np.allclose(cvar.to_numpy(), var)
    assert cvar["strategy"] < var[0]
    assert cvar["benchmark"] < var[1]


def test_in_notebook_uses_run_line_magic_for_ipython_9(monkeypatch):
    class ZMQInteractiveShell:
        def __init__(self):
            self.calls = []

        def run_line_magic(self, name, argument):
            self.calls.append((name, argument))

    shell = ZMQInteractiveShell()
    monkeypatch.setattr(builtins, "get_ipython", lambda: shell, raising=False)

    assert utils._in_notebook(matplotlib_inline=True) is True
    assert shell.calls == [("matplotlib", "inline")]
