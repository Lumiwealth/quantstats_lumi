import pandas as pd
import re
import quantstats_lumi.reports as reports
import tempfile
import os

def test_summary_metrics_match_metrics_table():
    # 12 months, 3% per month compounded
    index = pd.date_range(start='2022-01-31', periods=12, freq='M')
    returns = pd.Series([0.03]*12, index=index, name="Strategy")
    parameters = {"test_param": 2}
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp:
        html_path = tmp.name
    try:
        reports.html(
            returns,
            benchmark=None,
            output=html_path,
            parameters=parameters,
            periods_per_year=12
        )
        with open(html_path, "r", encoding="utf-8") as f:
            html = f.read()
        # Extract summary CAGR
        summary_match = re.search(r'Annual Return.*?<h1>([\d\.\-%]+)</h1>', html, re.DOTALL)
        assert summary_match, "Summary CAGR not found"
        summary_cagr = summary_match.group(1)
        # Extract metrics table CAGR (look for "CAGR" row)
        metrics_match = re.search(r'CAGR.*?<td[^>]*>([\d\.\-%]+)</td>', html, re.DOTALL)
        assert metrics_match, "Metrics table CAGR not found"
        table_cagr = metrics_match.group(1)
        # Remove percent signs and compare
        summary_cagr_val = float(summary_cagr.replace('%',''))
        table_cagr_val = float(table_cagr.replace('%',''))
        assert abs(summary_cagr_val - table_cagr_val) < 0.01
    finally:
        os.remove(html_path)
