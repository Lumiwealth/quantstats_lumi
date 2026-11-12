"""Nonzero portfolio changes must remain visible in report headlines."""
import pandas as pd
import pytest
import re

from quantstats_lumi import reports


@pytest.mark.parametrize('change,expected', [
    (-0.0018, '-0.18%'),
    (0.0018, '0.18%'),
    (-0.00014, '-0.01%'),
    (0.00014, '0.01%'),
    (-0.0000001, '-1e-05%'),
    (0.0000001, '1e-05%'),
    (0.0, '0%'),
    (0.09, '9%'),
])
def test_small_total_return_keeps_nonzero_precision(change, expected):
    returns = pd.Series([0.0, change, 0.0], index=pd.date_range('2026-04-06', periods=3))
    metrics = reports.metrics(returns, display=False, internal=True, match_dates=False)
    assert metrics.loc['Total Return', 'Strategy'] == expected
    payload = reports.metrics_json(returns, summary_only=True, match_dates=False)
    assert payload['scalar_metrics']['Total Return'] == pytest.approx(float(expected[:-1]) / 100)


def test_html_small_loss_headline_matches_return(tmp_path):
    returns = pd.Series([0.0, -0.0018, 0.0], index=pd.date_range('2026-04-06', periods=3))
    output = tmp_path / 'report.html'
    reports.html(returns, output=str(output), match_dates=False)
    heading = re.search(r'Total Return.*?</div>\s*<h2>([^<]+)</h2>', output.read_text(), re.S)
    assert heading.group(1) == '-0.18%'
