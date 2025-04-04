from datetime import datetime
import pandas as pd
from typing import Dict, Optional
import logging
import os

from data_collection.stock_data import StockDataCollector
from strategies.moving_average_strategy import MovingAverageCrossover
from risk_management.risk_manager import RiskManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PaperTradingSimulator:
    def __init__(self,
                symbols: list[str],
                initial_capital: float = 100000.0,
                strategy_params: Optional[Dict] = None):
        """
        Initialize the paper trading simulator
        :param symbols: List of stock symbols to trade
        :param initial_capital: Initial capital for trading
        :param strategy_params: Parameters for the trading strategy
        """
        self.symbols = symbols
        self.initial_capital = initial_capital
        
        # Initialize components
        self.risk_manager = RiskManager(
            initial_capital=initial_capital,
            max_position_size_pct=0.02,  # 2% max per position
            max_portfolio_risk_pct=0.05,  # 5% max portfolio risk
            max_positions=5,
            stop_loss_pct=0.02  # 2% stop loss
        )
        
        # Initialize strategy with default or provided parameters
        strategy_params = strategy_params or {}
        self.strategy = MovingAverageCrossover(
            short_window=strategy_params.get('short_window', 50),
            long_window=strategy_params.get('long_window', 200)
        )
        
        # Initialize data collectors for each symbol
        self.data_collectors = {
            symbol: StockDataCollector(symbol) for symbol in symbols
        }
        
        # Initialize trade log
        self.trade_log = []

    def log_trade(self, symbol: str, action: str, price: float, quantity: int, pnl: Optional[float] = None):
        """
        Log a trade to the trade history
        """
        trade = {
            'timestamp': datetime.now(),
            'symbol': symbol,
            'action': action,
            'price': price,
            'quantity': quantity,
            'pnl': pnl,
            'portfolio_value': self.risk_manager.get_portfolio_status()['total_value']
        }
        self.trade_log.append(trade)
        logger.info(f"Trade executed: {trade}")

    def run_simulation(self, period: str = "1d", interval: str = "5m"):
        """
        Run the paper trading simulation
        :param period: Time period to simulate (e.g., "1d", "5d", "1mo")
        :param interval: Data interval (e.g., "1m", "5m", "15m")
        """
        logger.info("Starting paper trading simulation...")
        
        for symbol in self.symbols:
            # Fetch latest data
            collector = self.data_collectors[symbol]
            data = collector.fetch_historical_data(period=period, interval=interval)
            
            # Generate trading signals
            signals = self.strategy.calculate_signals(data)
            
            # Process each signal
            for timestamp, row in signals.iterrows():
                current_price = row['Close']
                
                # Check for position entry
                if row['Position'] == 1:  # Buy signal
                    position = self.risk_manager.open_position(symbol, current_price)
                    if position:
                        self.log_trade(symbol, 'BUY', current_price, position.quantity)
                
                # Check for position exit
                elif row['Position'] == -1:  # Sell signal
                    pnl = self.risk_manager.close_position(symbol)
                    if pnl is not None:
                        self.log_trade(symbol, 'SELL', current_price, 0, pnl)
                
                # Update existing positions
                self.risk_manager.update_position(symbol, current_price)

    def get_simulation_results(self) -> Dict:
        """
        Get the results of the simulation
        """
        portfolio_status = self.risk_manager.get_portfolio_status()
        
        # Calculate additional metrics
        trades_df = pd.DataFrame(self.trade_log)
        if not trades_df.empty:
            winning_trades = trades_df[trades_df['pnl'] > 0]['pnl'].count()
            total_trades = trades_df['pnl'].count()
            win_rate = winning_trades / total_trades if total_trades > 0 else 0
        else:
            win_rate = 0
        
        results = {
            **portfolio_status,
            'total_trades': len(self.trade_log),
            'win_rate': win_rate * 100,
            'initial_capital': self.initial_capital,
        }
        
        return results

if __name__ == "__main__":
    # Example usage
    symbols = ["AAPL", "MSFT", "GOOGL"]
    simulator = PaperTradingSimulator(
        symbols=symbols,
        initial_capital=100000.0,
        strategy_params={'short_window': 50, 'long_window': 200}
    )
    
    # Run simulation
    simulator.run_simulation(period="1d", interval="5m")
    
    # Print results
    results = simulator.get_simulation_results()
    print("\nSimulation Results:")
    for key, value in results.items():
        print(f"{key}: {value}")

