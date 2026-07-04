from typing import Optional, Dict, Any
from binance.exceptions import BinanceAPIException, BinanceRequestException
from .client import BinanceTestnetClient
from .logging_config import logger

def place_order(
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: Optional[float] = None,
    stop_price: Optional[float] = None
) -> Dict[str, Any]:
    """
    Places an order on the Binance Futures Testnet.
    
    Returns:
        dict: The order response details from the API.
    Raises:
        Exception: If the order placement fails.
    """
    try:
        client_wrapper = BinanceTestnetClient()
        client = client_wrapper.get_client()

        order_params = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity
        }

        # Handle specific parameters for different order types
        if order_type == "LIMIT":
            order_params["price"] = price
            order_params["timeInForce"] = "GTC"  # Good Till Cancelled is required for LIMIT orders
            
        elif order_type == "STOP_MARKET":
            order_params["stopPrice"] = stop_price

        logger.info(f"Sending order request: {order_params}")

        # Place the order using python-binance futures endpoint
        response = client.futures_create_order(**order_params)
        
        logger.info(f"Order placed successfully. Response: {response}")
        return response

    except BinanceAPIException as e:
        logger.error(f"Binance API Error while placing order: {e.status_code} - {e.message}")
        raise
    except BinanceRequestException as e:
        logger.error(f"Network error while placing order: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise
