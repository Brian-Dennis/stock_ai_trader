# Stock AI Trading System

An AI-powered stock trading system that implements automated trading strategies with risk management and performance analytics.

## Features

- Multiple trading strategies support (currently implementing Moving Average Crossover)
- Real-time and historical data fetching using yfinance
- Risk management with position sizing and stop-loss
- Paper trading simulation
- Performance analytics and reporting
- Configurable trading parameters
- Comprehensive logging system

## Project Structure

```
stock_ai_trader/
├── analytics/          # Performance analysis and reporting
├── config/            # Configuration management
├── data_collection/   # Market data collection
├── logs/             # Application logs
├── output/           # Generated reports and charts
├── paper_trading/    # Paper trading simulation
├── risk_management/  # Risk management system
├── strategies/       # Trading strategies
├── main.py          # Main application entry point
└── requirements.txt  # Project dependencies
```

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd stock_ai_trader
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Unix/macOS
   # or
   .\venv\Scripts\activate  # On Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

The system can be configured through the `config/config.yaml` file. Key configuration options include:

- Trading parameters (initial capital, position sizes, risk limits)
- Strategy parameters (moving average windows, minimum volume)
- Data collection settings (default period and interval)

## Usage

Run the system using the main script:

```bash
python main.py --mode paper_trade --symbols AAPL MSFT GOOGL --period 1d --interval 5m
```

### Command Line Arguments

- `--mode`: Trading mode (`backtest` or `paper_trade`)
- `--period`: Trading period (e.g., `1d`, `5d`, `1mo`)
- `--interval`: Data interval (e.g., `1m`, `5m`, `15m`)
- `--symbols`: List of stock symbols to trade

## Output

The system generates:
- Trading logs in the `logs/` directory
- Performance reports in the `output/analytics/` directory
- Equity curves and drawdown charts

## Risk Management

The system implements several risk management features:
- Position sizing based on account risk
- Maximum portfolio exposure limits
- Stop-loss orders
- Maximum number of concurrent positions

## Performance Analytics

The analytics module provides:
- Total return calculation
- Win rate analysis
- Sharpe ratio
- Maximum drawdown
- Equity curve visualization
- Trade log analysis

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This software is for educational purposes only. It is not financial advice and should not be used for actual trading without proper risk management and understanding of the markets.

