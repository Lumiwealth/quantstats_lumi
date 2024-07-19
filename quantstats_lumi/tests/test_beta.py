import unittest
from quantstats_lumi import stats  # Adjust the import path based on your project structure
import pandas as pd

class TestBeta(unittest.TestCase):
    
    def test_beta_positive_returns(self):
        portfolio_returns = [0.01, 0.02, 0.015, 0.03, 0.025]
        benchmark_returns = [0.008, 0.018, 0.013, 0.028, 0.022]
        # Manually calculate expected beta
        returns_df = pd.DataFrame({"portfolio": portfolio_returns, "benchmark": benchmark_returns}).dropna()
        covariance = returns_df['portfolio'].cov(returns_df['benchmark'])
        variance = returns_df['benchmark'].var()
        expected_beta = covariance / variance
        result = stats.beta(portfolio_returns, benchmark_returns)
        self.assertAlmostEqual(result, expected_beta, places=4)
    
    def test_beta_negative_returns(self):
        portfolio_returns = [-0.01, -0.02, -0.015, -0.03, -0.025]
        benchmark_returns = [-0.008, -0.018, -0.013, -0.028, -0.022]
        # Manually calculate expected beta
        returns_df = pd.DataFrame({"portfolio": portfolio_returns, "benchmark": benchmark_returns}).dropna()
        covariance = returns_df['portfolio'].cov(returns_df['benchmark'])
        variance = returns_df['benchmark'].var()
        expected_beta = covariance / variance
        result = stats.beta(portfolio_returns, benchmark_returns)
        self.assertAlmostEqual(result, expected_beta, places=4)

    def test_beta_mixed_returns(self):
        portfolio_returns = [0.01, -0.02, 0.015, -0.03, 0.025]
        benchmark_returns = [0.008, -0.018, 0.013, -0.028, 0.022]
        # Manually calculate expected beta
        returns_df = pd.DataFrame({"portfolio": portfolio_returns, "benchmark": benchmark_returns}).dropna()
        covariance = returns_df['portfolio'].cov(returns_df['benchmark'])
        variance = returns_df['benchmark'].var()
        expected_beta = covariance / variance
        result = stats.beta(portfolio_returns, benchmark_returns)
        self.assertAlmostEqual(result, expected_beta, places=4)
    
    def test_beta_non_numeric_input(self):
        portfolio_returns = ["a", "b", "c"]
        benchmark_returns = [0.01, 0.02, 0.015]
        with self.assertRaises(ValueError):
            stats.beta(portfolio_returns, benchmark_returns)
    
    def test_beta_empty_input(self):
        portfolio_returns = []
        benchmark_returns = [0.01, 0.02, 0.015]
        with self.assertRaises(ValueError):
            stats.beta(portfolio_returns, benchmark_returns)
    
    def test_beta_realistic_scenario(self):
        # Simulated realistic returns
        portfolio_returns = [0.001, 0.002, 0.003, 0.002, 0.001, -0.001, 0.002, 0.001, 0.002, 0.003]
        benchmark_returns = [0.0008, 0.0018, 0.0025, 0.002, 0.0015, -0.0008, 0.0022, 0.0012, 0.0018, 0.0025]
        # Manually calculate expected beta
        returns_df = pd.DataFrame({"portfolio": portfolio_returns, "benchmark": benchmark_returns}).dropna()
        covariance = returns_df['portfolio'].cov(returns_df['benchmark'])
        variance = returns_df['benchmark'].var()
        expected_beta = covariance / variance
        result = stats.beta(portfolio_returns, benchmark_returns)
        self.assertAlmostEqual(result, expected_beta, places=4)

if __name__ == '__main__':
    unittest.main()