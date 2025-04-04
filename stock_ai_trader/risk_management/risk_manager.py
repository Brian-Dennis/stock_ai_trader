from dataclasses import dataclass
from typing import Optional, Dict, List
import pandas as pd

@dataclass
class Position:
    symbol: str
    quantity: int
    entry_price: float
    current_price: float
    stop_loss: float

    @property
    def position_value(self) -> float:
        return self.quantity * self.current_price

    @property
    def unrealized_pnl(self) -> float:
        return self.quantity * (self.current_price - self.entry_price)

    @property
    def stop_loss_pct(self) -> float:
        return (self.stop_loss - self.entry_price) / self.entry_price * 100

class RiskManager:
    def __init__(self,
                initial_capital: float,
                max_position_size_pct: float = 0.02,  # 2% max per position
                max_portfolio_risk_pct: float = 0.05,  # 5% max portfolio risk
                max_positions: int = 5,
                stop_loss_pct: float = 0.03):  # 3% stop loss
        self.initial_capital = initial_capital
        self.current_capital = initial_capital
        self.max_position_size_pct = max_position_size_pct
        self.max_portfolio_risk_pct = max_portfolio_risk_pct
        self.max_positions = max_positions
        self.stop_loss_pct = stop_loss_pct
        self.positions: Dict[str, Position] = {}

    def calculate_position_size(self, price: float) -> int:
        """
        Calculate the maximum position size based on risk parameters
        """
        max_position_value = self.current_capital * self.max_position_size_pct
        return int(max_position_value / price)

    def can_open_position(self, symbol: str, price: float) -> tuple[bool, str]:
        """
        Check if a new position can be opened based on risk rules
        """
        # Check maximum positions limit
        if len(self.positions) >= self.max_positions:
            return False, "Maximum number of positions reached"

        # Calculate potential position value
        position_size = self.calculate_position_size(price)
        position_value = position_size * price

        # Check if position size exceeds maximum risk
        if position_value > self.current_capital * self.max_position_size_pct:
            return False, "Position size exceeds maximum risk threshold"

        # Calculate total portfolio risk including this position
        total_risk = sum(pos.position_value for pos in self.positions.values())
        total_risk += position_value

        if total_risk > self.current_capital * self.max_portfolio_risk_pct:
            return False, "Total portfolio risk would exceed maximum threshold"

        return True, "Position can be opened"

    def open_position(self, symbol: str, price: float) -> Optional[Position]:
        """
        Open a new position if risk parameters allow
        """
        can_open, message = self.can_open_position(symbol, price)
        if not can_open:
            print(f"Cannot open position: {message}")
            return None

        position_size = self.calculate_position_size(price)
        stop_loss = price * (1 - self.stop_loss_pct)

        position = Position(
            symbol=symbol,
            quantity=position_size,
            entry_price=price,
            current_price=price,
            stop_loss=stop_loss
        )

        self.positions[symbol] = position
        return position

    def update_position(self, symbol: str, current_price: float) -> None:
        """
        Update position with current price and check stop loss
        """
        if symbol not in self.positions:
            return

        position = self.positions[symbol]
        position.current_price = current_price

        # Check stop loss
        if current_price <= position.stop_loss:
            self.close_position(symbol)
            print(f"Stop loss triggered for {symbol}")

    def close_position(self, symbol: str) -> Optional[float]:
        """
        Close a position and return realized P&L
        """
        if symbol not in self.positions:
            return None

        position = self.positions.pop(symbol)
        pnl = position.unrealized_pnl
        self.current_capital += pnl
        return pnl

    def get_portfolio_status(self) -> Dict:
        """
        Get current portfolio status and risk metrics
        """
        total_value = self.current_capital
        positions_value = sum(pos.position_value for pos in self.positions.values())
        total_value += positions_value

        return {
            "total_value": total_value,
            "cash": self.current_capital,
            "positions_value": positions_value,
            "number_of_positions": len(self.positions),
            "portfolio_return": (total_value - self.initial_capital) / self.initial_capital * 100
        }

if __name__ == "__main__":
    # Example usage
    risk_manager = RiskManager(initial_capital=100000)
    
    # Try to open a position
    position = risk_manager.open_position("AAPL", price=150.0)
    if position:
        print(f"Opened position: {position}")
        
        # Update position with new price
        risk_manager.update_position("AAPL", current_price=148.0)
        
        # Get portfolio status
        status = risk_manager.get_portfolio_status()
        print("\nPortfolio Status:")
        for key, value in status.items():
            print(f"{key}: {value}")

