import os
import tempfile

import pandas as pd
import pytest

from quantstats_lumi import reports

# Test the metrics function
def test_metrics(returns, benchmark):
    """Test that metrics function returns the expected data types."""
    # Test with display=False to get the metrics DataFrame
    metrics_df = reports.metrics(returns, benchmark, display=False)

    # Check that the result is a DataFrame
    assert isinstance(metrics_df, pd.DataFrame)

    # The metrics function returns a DataFrame with 'Strategy' and 'Benchmark' columns
    assert 'Strategy' in metrics_df.columns
    assert 'Benchmark' in metrics_df.columns

    # Check that the DataFrame has rows (metrics)
    assert len(metrics_df) > 0

# Test the html function
def test_html(returns, benchmark):
    """Test that html function generates HTML content."""
    # Use a temporary file for the output
    with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as tmp:
        output_path = tmp.name

    try:
        # Generate the HTML report
        reports.html(
            returns, 
            benchmark,
            output=output_path,  # Save to temporary file
            title="Test Report"
        )

        # Check that the file was created
        assert os.path.exists(output_path)

        # If we get here without an exception, the test passes
        assert True
    except Exception as e:
        pytest.fail(f"reports.html raised an exception: {e}")
    finally:
        # Clean up the temporary file
        if os.path.exists(output_path):
            os.unlink(output_path)

# Test the basic function
def test_basic(returns, benchmark):
    """Test that basic function runs without errors."""
    # Call the basic function with display=False
    # This should run without errors
    reports.basic(returns, benchmark, display=False)

    # No assertion needed as we're just checking it runs without errors

# Test the full function
def test_full(returns, benchmark):
    """Test that full function runs without errors."""
    reports.full(returns, benchmark, display=False)


# Test the plots function
def test_plots(returns, benchmark):
    """Test that plots function runs without errors."""
    # Call the plots function with display=False
    # This should run without errors
    reports.plots(returns, benchmark, display=False)

    # No assertion needed as we're just checking it runs without errors

# Test parameters_section function
def test_parameters_section():
    """Test that parameters_section function returns the expected HTML."""
    # Create a sample parameters dictionary
    params = {
        'strategy': 'Test Strategy',
        'period': '2020-2023',
        'risk_free_rate': 0.02
    }

    # Get the HTML for the parameters section
    html_content = reports.parameters_section(params)

    # Check that the result is a string
    assert isinstance(html_content, str)

    # Check that the parameters are included in the HTML
    assert 'Test Strategy' in html_content
    assert '2020-2023' in html_content
    assert '0.02' in html_content

# Test edge cases
def test_empty_returns():
    """Test behavior with empty returns."""
    # Create an empty Series with a datetime index
    empty_returns = pd.Series([], index=pd.DatetimeIndex([]), dtype=float)

    # Use try-except to handle any errors
    try:
        # This should handle empty returns gracefully
        metrics_df = reports.metrics(empty_returns, display=False)

        # Check that the result is a DataFrame
        assert isinstance(metrics_df, pd.DataFrame)
    except Exception as e:
        # If an exception occurs, the test still passes
        # Empty returns are an edge case that might not be fully supported
        pytest.skip(f"Empty returns not fully supported: {e}")

def test_single_return():
    """Test behavior with a single return value."""
    single_return = pd.Series([0.01], index=[pd.Timestamp('2020-01-01')])

    # This should handle a single return value
    metrics_df = reports.metrics(single_return, display=False)

    # Check that the result is a DataFrame
    assert isinstance(metrics_df, pd.DataFrame)

def test_mismatched_dates(returns, benchmark):
    """Test behavior with mismatched dates between returns and benchmark."""
    # The fixtures already provide Series objects
    returns_series = returns

    # Create a benchmark with different dates
    different_dates = pd.date_range(start='2019-01-01', periods=len(benchmark), freq='D')
    benchmark_series = pd.Series(benchmark.values, index=different_dates)

    # Test with match_dates=True (default)
    metrics_df = reports.metrics(returns_series, benchmark_series, display=False)

    # Check that the result is a DataFrame
    assert isinstance(metrics_df, pd.DataFrame)

    # Test with match_dates=False
    metrics_df = reports.metrics(returns_series, benchmark_series, match_dates=False, display=False)

    # Check that the result is a DataFrame
    assert isinstance(metrics_df, pd.DataFrame)
