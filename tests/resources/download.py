"""Download some data needed for the tests."""
import pandas as pd
import yfinance as yf

if __name__ == '__main__':
    def download_returns(ticker, period="max", proxy=None):
        """Download historical returns for a specified ticker or tickers.

        This function utilizes
        yfinance to fetch adjusted closing prices and calculates daily percentage changes.

        Args:
            ticker: The stock ticker symbol or list of ticker symbols to fetch the data for.
            period: The time period for the data, given either as a string (default is "max")
                or a pandas DatetimeIndex to fetch data for a specific date range.
            proxy: Optional proxy settings to be used for the HTTP requests.

        Returns:
            pandas.Series or pandas.DataFrame: A Series or DataFrame containing the daily percentage
            changes of adjusted closing prices of the specified ticker(s). The structure depends
            on whether a single ticker or multiple tickers are provided.

        """
        params = {"tickers": ticker, "auto_adjust": True, "multi_level_index": False, "progress": False, "proxy": proxy}
        if isinstance(period, pd.DatetimeIndex):
            params["start"] = period[0]
        else:
            params["period"] = period
        dframe = yf.download(**params)["Close"].pct_change()
        dframe = dframe.tz_localize(None)
        return dframe

    stock = download_returns("META")
    stock.to_csv("meta.csv")

    spy = download_returns("SPY")
    spy.to_csv("benchmark.csv")
