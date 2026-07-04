import typer
from typing import Optional

def validate_symbol(symbol: str) -> str:
    """Ensure symbol is formatted correctly (e.g., BTCUSDT)."""
    symbol = symbol.upper()
    if not symbol.isalnum():
        raise typer.BadParameter("Symbol must be alphanumeric (e.g., BTCUSDT).")
    return symbol

def validate_side(side: str) -> str:
    """Ensure side is either BUY or SELL."""
    side = side.upper()
    if side not in ["BUY", "SELL"]:
        raise typer.BadParameter("Side must be either 'BUY' or 'SELL'.")
    return side

def validate_order_type(order_type: str) -> str:
    """Ensure order type is valid."""
    order_type = order_type.upper()
    valid_types = ["MARKET", "LIMIT", "STOP_MARKET"]
    if order_type not in valid_types:
        raise typer.BadParameter(f"Order type must be one of {valid_types}.")
    return order_type

def validate_quantity(quantity: float) -> float:
    """Ensure quantity is strictly positive."""
    if quantity <= 0:
        raise typer.BadParameter("Quantity must be greater than 0.")
    return quantity

def validate_price(price: Optional[float], order_type: str, stop_price: Optional[float] = None) -> Optional[float]:
    """Ensure price is provided for LIMIT orders and is strictly positive."""
    order_type = order_type.upper()
    
    if order_type == "LIMIT":
        if price is None:
            raise typer.BadParameter("Price is required for LIMIT orders.")
        if price <= 0:
            raise typer.BadParameter("Price must be greater than 0.")
            
    if order_type == "STOP_MARKET":
        if stop_price is None:
            raise typer.BadParameter("stop_price is required for STOP_MARKET orders.")
        if stop_price <= 0:
            raise typer.BadParameter("stop_price must be greater than 0.")
            
    return price
