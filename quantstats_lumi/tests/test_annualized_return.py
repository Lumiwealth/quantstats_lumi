import unittest
from quantstats_lumi import stats  # Adjust the import path based on your project structure
import pandas as pd

class TestAnnualizedReturn(unittest.TestCase):
    
    def test_positive_returns(self):
        returns = [0.01, 0.02, 0.015, 0.03, 0.025]
        # Manually calculate expected annualized return
        total_return = (1 + pd.Series(returns)).prod() - 1
        k = len(returns)
        D_bar = 252
        expected_return = (1 + total_return) ** (D_bar / k) - 1
        result = stats.annualized_return(returns)
        self.assertAlmostEqual(result, expected_return, places=4)
    
    def test_negative_returns(self):
        returns = [-0.01, -0.02, -0.015, -0.03, -0.025]
        # Manually calculate expected annualized return
        total_return = (1 + pd.Series(returns)).prod() - 1
        k = len(returns)
        D_bar = 252
        expected_return = (1 + total_return) ** (D_bar / k) - 1
        result = stats.annualized_return(returns)
        self.assertAlmostEqual(result, expected_return, places=4)

    def test_zero_returns(self):
        returns = [0.0, 0.0, 0.0, 0.0, 0.0]
        expected_return = 0.0
        result = stats.annualized_return(returns)
        self.assertAlmostEqual(result, expected_return, places=4)

    def test_single_day_return(self):
        returns = [0.05]
        # Manually calculate expected annualized return
        total_return = (1 + pd.Series(returns)).prod() - 1
        k = len(returns)
        D_bar = 252
        expected_return = (1 + total_return) ** (D_bar / k) - 1
        result = stats.annualized_return(returns)
        self.assertAlmostEqual(result, expected_return, places=4)

    def test_long_time_series_low_volatility(self):
        # Simulate a more complex series with low volatility and mixed returns over a year
        returns = [0.001, -0.002, 0.003, -0.001, 0.0005, -0.0003, 0.002, 0.001, -0.0015, 0.0007] * 36 + [0.0001] * 5
        # Manually calculate expected annualized return
        total_return = (1 + pd.Series(returns)).prod() - 1
        k = len(returns)
        D_bar = 252
        expected_return = (1 + total_return) ** (D_bar / k) - 1
        result = stats.annualized_return(returns)
        self.assertAlmostEqual(result, expected_return, places=4)
    
    def test_non_numeric_input(self):
        returns = ["a", "b", "c"]
        with self.assertRaises(ValueError):
            stats.annualized_return(returns)
    
    def test_empty_input(self):
        returns = []
        with self.assertRaises(ValueError):
            stats.annualized_return(returns)

if __name__ == '__main__':
    unittest.main()
