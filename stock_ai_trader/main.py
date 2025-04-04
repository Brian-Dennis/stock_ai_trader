import argparse
from datetime import datetime
import sys
import os

from config.app_config import config
from config.logging_config import setup_logging, get_logger
from paper_trading.simulator import PaperTradingSimulator
from analytics.performance_analyzer import PerformanceAnalyzer

def parse_arguments():
    """
    Parse command line arguments
    """
    parser = argparse.ArgumentParser(description='Stock AI Trading System')
    parser.add_argument('--mode', choices=['backtest', 'paper_trade'], default='paper_trade',
                      help='Trading mode: backtest or paper trade')
    parser.add_argument('--period', default=None,
                      help='Trading period (e.g., 1d, 5d, 1mo)')
    parser.add_argument('--interval', default=None,
                      help='Data interval (e.g., 1m, 5m, 15m)')
    parser.add_argument('--symbols', nargs='+', default=None,
                      help='List of stock symbols to trade')
    
    return parser.parse_args()

def run_trading_system(args):
    """
    Run the trading system with the specified configuration
    """
    # Setup logging
    setup_logging()
    logger = get_logger(__name__)
    
    try:
        # Use command line arguments if provided, otherwise use config
        period = args.period or config.data.default_period
        interval = args.interval or config.data.default_interval
        symbols = args.symbols or config.trading.symbols
        
        logger.info(f"Starting trading system in {args.mode} mode")
        logger.info(f"Trading symbols: {symbols}")
        logger.info(f"Period: {period}, Interval: {interval}")
        
        # Initialize simulator with configuration
        simulator = PaperTradingSimulator(
            symbols=symbols,
            initial_capital=config.trading.initial_capital,
            strategy_params={
                'short_window': config.strategy.short_window,
                'long_window': config.strategy.long_window
            }
        )
        
        # Run simulation
        simulator.run_simulation(period=period, interval=interval)
        
        # Analyze performance
        analyzer = PerformanceAnalyzer(
            trade_log=simulator.trade_log,
            initial_capital=config.trading.initial_capital
        )
        
        # Generate and display report
        report = analyzer.generate_report()
        print("\nTrading Session Report:")
        print("=" * 50)
        print(report)
        
        logger.info("Trading session completed successfully")
        
        return 0
        
    except Exception as e:
        logger.error(f"Error running trading system: {str(e)}", exc_info=True)
        return 1

if __name__ == "__main__":
    # Parse command line arguments
    args = parse_arguments()
    
    # Run the trading system
    sys_exit = run_trading_system(args)
    
    # Exit with appropriate status
    sys.exit(sys_exit)

