import pandas as pd
import numpy as np
from typing import Tuple

class MovingAverageCrossover:
    def __init__(self, short_window: int = 50, long_window: int = 200):
        """
        Initialize MA Crossover strategy
        :param short_window: Short-term moving average period
        :param long_window: Long-term moving average period
        """
        self.short_window = short_window
        self.long_window = long_window

    def calculate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate trading signals based on moving average crossover
        :param data: DataFrame with 'Close' price column
        :return: DataFrame with signals
        """
        # Make a copy of the data
        signals = data.copy()
        
        # Calculate moving averages
        signals['SMA_short'] = signals['Close'].rolling(window=self.short_window).mean()
        signals['SMA_long'] = signals['Close'].rolling(window=self.long_window).mean()
        
        # Generate signals
        signals['Signal'] = 0
        signals.loc[signals['SMA_short'] > signals['SMA_long'], 'Signal'] = 1  # Buy signal
        signals.loc[signals['SMA_short'] < signals['SMA_long'], 'Signal'] = -1  # Sell signal
        
        # Generate actual trading orders (signal changes)
        signals['Position'] = signals['Signal'].diff()
        
        return signals

    def backtest(self, data: pd.DataFrame, initial_capital: float = 100000.0) -> Tuple[pd.DataFrame, dict]:
        """
        Backtest the strategy
        :param data: DataFrame with OHLC data
        :param initial_capital: Initial capital for backtesting
        :return: DataFrame with positions and portfolio value, performance metrics
        """
        signals = self.calculate_signals(data)
        
        # Initialize positions and portfolio
        positions = pd.DataFrame(index=signals.index).fillna(0.0)
        positions['Stock'] = signals['Signal']  # 1 for long, -1 for short, 0 for no position
        
        # Initialize portfolio value
        portfolio = pd.DataFrame(index=signals.index)
        portfolio['Position'] = positions['Stock'] * signals['Close']
        portfolio['Cash'] = initial_capital - (positions['Stock'].diff() * signals['Close']).cumsum()
        portfolio['Total'] = portfolio['Cash'] + portfolio['Position']
        
        # Calculate metrics
        returns = portfolio['Total'].pct_change()
        metrics = {
            'Total Return': (portfolio['Total'][-1] - initial_capital) / initial_capital * 100,
            'Sharpe Ratio': np.sqrt(252) * returns.mean() / returns.std(),
            'Max Drawdown': (portfolio['Total'] / portfolio['Total'].cummax() - 1).min() * 100
        }
        
        return portfolio, metrics

if __name__ == "__main__":
    # Example usage
    from data_collection.stock_data import StockDataCollector
    
    # Fetch some historical data
    collector = StockDataCollector("AAPL")
    data = collector.fetch_historical_data(period="2y")
    
    # Initialize and run strategy
    strategy = MovingAverageCrossover(short_window=50, long_window=200)
    portfolio, metrics = strategy.backtest(data)
    
    print("\nBacktest Results:")
    for metric, value in metrics.items():
        print(f"{metric}: {value:.2f}")

