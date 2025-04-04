import os
import yaml
from typing import Dict, Any
from dataclasses import dataclass
from datetime import datetime

@dataclass
class TradingConfig:
    symbols: list[str]
    initial_capital: float
    max_position_size_pct: float
    max_portfolio_risk_pct: float
    max_positions: int
    stop_loss_pct: float

@dataclass
class StrategyConfig:
    short_window: int
    long_window: int
    min_volume: int

@dataclass
class DataConfig:
    default_period: str
    default_interval: str
    data_source: str

class AppConfig:
    def __init__(self):
        """
        Initialize application configuration
        """
        self.config_dir = os.path.dirname(__file__)
        self.config_file = os.path.join(self.config_dir, 'config.yaml')
        self.config_data = self._load_config()

        # Initialize configuration objects
        self.trading = self._init_trading_config()
        self.strategy = self._init_strategy_config()
        self.data = self._init_data_config()

    def _load_config(self) -> Dict[str, Any]:
        """
        Load configuration from YAML file
        """
        if not os.path.exists(self.config_file):
            self._create_default_config()

        with open(self.config_file, 'r') as f:
            return yaml.safe_load(f)

    def _create_default_config(self) -> None:
        """
        Create default configuration file
        """
        default_config = {
            'trading': {
                'symbols': ['AAPL', 'MSFT', 'GOOGL'],
                'initial_capital': 100000.0,
                'max_position_size_pct': 0.02,
                'max_portfolio_risk_pct': 0.05,
                'max_positions': 5,
                'stop_loss_pct': 0.02
            },
            'strategy': {
                'short_window': 50,
                'long_window': 200,
                'min_volume': 1000000
            },
            'data': {
                'default_period': '1d',
                'default_interval': '5m',
                'data_source': 'yfinance'
            }
        }

        with open(self.config_file, 'w') as f:
            yaml.dump(default_config, f, default_flow_style=False)

    def _init_trading_config(self) -> TradingConfig:
        """
        Initialize trading configuration
        """
        trading_data = self.config_data['trading']
        return TradingConfig(
            symbols=trading_data['symbols'],
            initial_capital=trading_data['initial_capital'],
            max_position_size_pct=trading_data['max_position_size_pct'],
            max_portfolio_risk_pct=trading_data['max_portfolio_risk_pct'],
            max_positions=trading_data['max_positions'],
            stop_loss_pct=trading_data['stop_loss_pct']
        )

    def _init_strategy_config(self) -> StrategyConfig:
        """
        Initialize strategy configuration
        """
        strategy_data = self.config_data['strategy']
        return StrategyConfig(
            short_window=strategy_data['short_window'],
            long_window=strategy_data['long_window'],
            min_volume=strategy_data['min_volume']
        )

    def _init_data_config(self) -> DataConfig:
        """
        Initialize data configuration
        """
        data_config = self.config_data['data']
        return DataConfig(
            default_period=data_config['default_period'],
            default_interval=data_config['default_interval'],
            data_source=data_config['data_source']
        )

    def save_config(self) -> None:
        """
        Save current configuration to file
        """
        config_data = {
            'trading': {
                'symbols': self.trading.symbols,
                'initial_capital': self.trading.initial_capital,
                'max_position_size_pct': self.trading.max_position_size_pct,
                'max_portfolio_risk_pct': self.trading.max_portfolio_risk_pct,
                'max_positions': self.trading.max_positions,
                'stop_loss_pct': self.trading.stop_loss_pct
            },
            'strategy': {
                'short_window': self.strategy.short_window,
                'long_window': self.strategy.long_window,
                'min_volume': self.strategy.min_volume
            },
            'data': {
                'default_period': self.data.default_period,
                'default_interval': self.data.default_interval,
                'data_source': self.data.data_source
            }
        }

        with open(self.config_file, 'w') as f:
            yaml.dump(config_data, f, default_flow_style=False)

# Create singleton instance
config = AppConfig()

if __name__ == "__main__":
    # Example usage
    print("Trading Configuration:")
    print(f"Symbols: {config.trading.symbols}")
    print(f"Initial Capital: ${config.trading.initial_capital:,.2f}")
    print(f"Max Position Size: {config.trading.max_position_size_pct*100}%")

    print("\nStrategy Configuration:")
    print(f"Short Window: {config.strategy.short_window}")
    print(f"Long Window: {config.strategy.long_window}")
    print(f"Minimum Volume: {config.strategy.min_volume:,}")

    print("\nData Configuration:")
    print(f"Default Period: {config.data.default_period}")
    print(f"Default Interval: {config.data.default_interval}")
    print(f"Data Source: {config.data.data_source}")

