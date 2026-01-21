"""global fixtures."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest


@pytest.fixture(scope="session", name="resource_dir")
def resource_fixture():
    """Resource fixture."""
    return Path(__file__).parent / "resources"


@pytest.fixture
def returns(resource_dir) -> pd.DataFrame:
    """Fixture that returns a Series with Meta returns.

    Args:
        resource_dir: The resource_dir fixture containing the path to test resources.

    Returns:
        pd.Series: A Series containing Meta returns.

    """
    return pd.read_csv(resource_dir / "meta.csv", index_col="Date", parse_dates=["Date"]).squeeze()


@pytest.fixture
def benchmark(resource_dir) -> pd.DataFrame:
    """Fixture that returns a Series with benchmark returns.

    Args:
        resource_dir: The resource_dir fixture containing the path to test resources.

    Returns:
        pd.Series: A Series containing SPY benchmark returns.

    """
    return pd.read_csv(resource_dir / "benchmark.csv", index_col="Date", parse_dates=["Date"]).squeeze()
