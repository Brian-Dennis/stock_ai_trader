import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os

class StockDataCollector:
    def __init__(self, symbol):
        self.symbol = symbol
        self.ticker = yf.Ticker(symbol)
        self.data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        os.makedirs(self.data_dir, exist_ok=True)

    def fetch_historical_data(self, period="1y", interval="1d"):
        """
        Fetch historical data for the specified symbol
        :param period: Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        :param interval: Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        :return: pandas DataFrame with historical data
        """
        data = self.ticker.history(period=period, interval=interval)
        return data

    def save_data(self, data, filename=None):
        """
        Save the data to a CSV file
        :param data: pandas DataFrame to save
        :param filename: name of the file (optional)
        """
        if filename is None:
            filename = f"{self.symbol}_{datetime.now().strftime('%Y%m%d')}.csv"
        
        filepath = os.path.join(self.data_dir, filename)
        data.to_csv(filepath)
        print(f"Data saved to {filepath}")

    def fetch_and_save_data(self, period="1y", interval="1d"):
        """
        Fetch and save historical data in one go
        """
        data = self.fetch_historical_data(period, interval)
        self.save_data(data)
        return data

if __name__ == "__main__":
    # Example usage
    collector = StockDataCollector("AAPL")
    data = collector.fetch_and_save_data()
    print(f"Fetched {len(data)} records for AAPL")

