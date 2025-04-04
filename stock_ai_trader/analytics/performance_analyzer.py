import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List
from datetime import datetime
import os

class PerformanceAnalyzer:
    def __init__(self, trade_log: List[Dict], initial_capital: float):
        """
        Initialize the performance analyzer
        :param trade_log: List of trade dictionaries
        :param initial_capital: Initial capital
        """
        self.trade_log = pd.DataFrame(trade_log)
        self.initial_capital = initial_capital
        
        # Create output directory for charts
        self.output_dir = os.path.join(os.path.dirname(__file__), '..', 'output', 'analytics')
        os.makedirs(self.output_dir, exist_ok=True)

    def calculate_metrics(self) -> Dict:
        """
        Calculate various performance metrics
        """
        if self.trade_log.empty:
            return {
                "total_return": 0,
                "win_rate": 0,
                "avg_profit_per_trade": 0,
                "max_drawdown": 0,
                "sharpe_ratio": 0,
                "total_trades": 0
            }

        # Calculate daily returns
        portfolio_values = self.trade_log['portfolio_value'].values
        daily_returns = np.diff(portfolio_values) / portfolio_values[:-1]

        # Calculate metrics
        total_return = (portfolio_values[-1] - self.initial_capital) / self.initial_capital * 100
        winning_trades = self.trade_log[self.trade_log['pnl'] > 0]['pnl'].count()
        total_trades = len(self.trade_log[self.trade_log['pnl'].notna()])
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
        avg_profit = self.trade_log['pnl'].mean() if not self.trade_log['pnl'].empty else 0

        # Calculate maximum drawdown
        cumulative_max = np.maximum.accumulate(portfolio_values)
        drawdowns = (portfolio_values - cumulative_max) / cumulative_max
        max_drawdown = np.min(drawdowns) * 100 if len(drawdowns) > 0 else 0

        # Calculate Sharpe Ratio (assuming risk-free rate of 0.01)
        risk_free_rate = 0.01
        excess_returns = daily_returns - risk_free_rate/252
        sharpe_ratio = np.sqrt(252) * excess_returns.mean() / excess_returns.std() if len(daily_returns) > 0 else 0

        return {
            "total_return": total_return,
            "win_rate": win_rate,
            "avg_profit_per_trade": avg_profit,
            "max_drawdown": max_drawdown,
            "sharpe_ratio": sharpe_ratio,
            "total_trades": total_trades
        }

    def plot_equity_curve(self, save: bool = True) -> None:
        """
        Plot the equity curve
        """
        if self.trade_log.empty:
            return

        plt.figure(figsize=(12, 6))
        plt.plot(self.trade_log['timestamp'], self.trade_log['portfolio_value'],
                label='Portfolio Value', color='blue')
        plt.title('Equity Curve')
        plt.xlabel('Time')
        plt.ylabel('Portfolio Value ($)')
        plt.grid(True)
        plt.legend()

        if save:
            filename = f'equity_curve_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
            plt.savefig(os.path.join(self.output_dir, filename))
            plt.close()
        else:
            plt.show()

    def plot_drawdown(self, save: bool = True) -> None:
        """
        Plot the drawdown chart
        """
        if self.trade_log.empty:
            return

        portfolio_values = self.trade_log['portfolio_value'].values
        cumulative_max = np.maximum.accumulate(portfolio_values)
        drawdowns = (portfolio_values - cumulative_max) / cumulative_max * 100

        plt.figure(figsize=(12, 6))
        plt.plot(self.trade_log['timestamp'], drawdowns, label='Drawdown %', color='red')
        plt.title('Portfolio Drawdown')
        plt.xlabel('Time')
        plt.ylabel('Drawdown (%)')
        plt.grid(True)
        plt.legend()

        if save:
            filename = f'drawdown_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
            plt.savefig(os.path.join(self.output_dir, filename))
            plt.close()
        else:
            plt.show()

    def generate_report(self) -> str:
        """
        Generate a performance report
        """
        metrics = self.calculate_metrics()
        
        # Generate plots
        self.plot_equity_curve()
        self.plot_drawdown()
        
        # Create report
        report = f"""
        Performance Report
        =================
        Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

        Summary Metrics:
        ---------------
        Total Return: {metrics['total_return']:.2f}%
        Win Rate: {metrics['win_rate']:.2f}%
        Average Profit per Trade: ${metrics['avg_profit_per_trade']:.2f}
        Maximum Drawdown: {metrics['max_drawdown']:.2f}%
        Sharpe Ratio: {metrics['sharpe_ratio']:.2f}
        Total Trades: {metrics['total_trades']}

        Charts have been saved to: {self.output_dir}
        """
        
        # Save report to file
        report_file = os.path.join(self.output_dir, 
                                 f'report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt')
        with open(report_file, 'w') as f:
            f.write(report)
        
        return report

if __name__ == "__main__":
    # Example usage
    from paper_trading.simulator import PaperTradingSimulator

    # Run a simulation
    symbols = ["AAPL", "MSFT", "GOOGL"]
    simulator = PaperTradingSimulator(
        symbols=symbols,
        initial_capital=100000.0
    )
    simulator.run_simulation(period="1d", interval="5m")

    # Analyze performance
    analyzer = PerformanceAnalyzer(
        trade_log=simulator.trade_log,
        initial_capital=simulator.initial_capital
    )

    # Generate and print report
    report = analyzer.generate_report()
    print(report)

