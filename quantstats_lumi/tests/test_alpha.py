import unittest
from quantstats_lumi import stats  # Adjust the import path based on your project structure
import pandas as pd
import numpy as np  # Add this import statement

class TestAlpha(unittest.TestCase):
    
    def test_alpha_positive_returns(self):
        portfolio_returns = [0.01, 0.02, 0.015, 0.03, 0.025]
        benchmark_returns = [0.008, 0.018, 0.013, 0.028, 0.022]
        rf = 0.001
        # Manually calculate expected alpha
        excess_portfolio = pd.Series(portfolio_returns) - rf
        excess_benchmark = pd.Series(benchmark_returns) - rf
        covariance = np.cov(excess_portfolio, excess_benchmark)[0, 1]
        variance = np.var(excess_benchmark)
        beta = covariance / variance
        expected_alpha = excess_portfolio.mean() - beta * excess_benchmark.mean()
        result = stats.alpha(portfolio_returns, benchmark_returns, rf)
        self.assertAlmostEqual(result, expected_alpha, places=4)
    
    def test_alpha_negative_returns(self):
        portfolio_returns = [-0.01, -0.02, -0.015, -0.03, -0.025]
        benchmark_returns = [-0.008, -0.018, -0.013, -0.028, -0.022]
        rf = 0.001
        # Manually calculate expected alpha
        excess_portfolio = pd.Series(portfolio_returns) - rf
        excess_benchmark = pd.Series(benchmark_returns) - rf
        covariance = np.cov(excess_portfolio, excess_benchmark)[0, 1]
        variance = np.var(excess_benchmark)
        beta = covariance / variance
        expected_alpha = excess_portfolio.mean() - beta * excess_benchmark.mean()
        result = stats.alpha(portfolio_returns, benchmark_returns, rf)
        self.assertAlmostEqual(result, expected_alpha, places=4)

    def test_alpha_mixed_returns(self):
        portfolio_returns = [0.01, -0.02, 0.015, -0.03, 0.025]
        benchmark_returns = [0.008, -0.018, 0.013, -0.028, 0.022]
        rf = 0.001
        # Manually calculate expected alpha
        excess_portfolio = pd.Series(portfolio_returns) - rf
        excess_benchmark = pd.Series(benchmark_returns) - rf
        covariance = np.cov(excess_portfolio, excess_benchmark)[0, 1]
        variance = np.var(excess_benchmark)
        beta = covariance / variance
        expected_alpha = excess_portfolio.mean() - beta * excess_benchmark.mean()
        result = stats.alpha(portfolio_returns, benchmark_returns, rf)
        self.assertAlmostEqual(result, expected_alpha, places=4)
    
    def test_alpha_non_numeric_input(self):
        portfolio_returns = ["a", "b", "c"]
        benchmark_returns = [0.01, 0.02, 0.015]
        with self.assertRaises(ValueError):
            stats.alpha(portfolio_returns, benchmark_returns)
    
    def test_alpha_empty_input(self):
        portfolio_returns = []
        benchmark_returns = [0.01, 0.02, 0.015]
        with self.assertRaises(ValueError):
            stats.alpha(portfolio_returns, benchmark_returns)
    
    def test_alpha_realistic_scenario(self):
        # Simulated realistic returns
        portfolio_returns = [0.001, 0.002, 0.003, 0.002, 0.001, -0.001, 0.002, 0.001, 0.002, 0.003]
        benchmark_returns = [0.0008, 0.0018, 0.0025, 0.002, 0.0015, -0.0008, 0.0022, 0.0012, 0.0018, 0.0025]
        rf = 0.001
        # Manually calculate expected alpha
        excess_portfolio = pd.Series(portfolio_returns) - rf
        excess_benchmark = pd.Series(benchmark_returns) - rf
        covariance = np.cov(excess_portfolio, excess_benchmark)[0, 1]
        variance = np.var(excess_benchmark)
        beta = covariance / variance
        expected_alpha = excess_portfolio.mean() - beta * excess_benchmark.mean()
        result = stats.alpha(portfolio_returns, benchmark_returns, rf)
        self.assertAlmostEqual(result, expected_alpha, places=4)

if __name__ == '__main__':
    unittest.main()