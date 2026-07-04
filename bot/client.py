import os
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
from .logging_config import logger

class BinanceTestnetClient:
    """
    Wrapper for the Binance API Client configured for the Futures Testnet.
    """
    def __init__(self, api_key: str = None, api_secret: str = None):
        self.api_key = api_key or os.getenv("BINANCE_API_KEY")
        self.api_secret = api_secret or os.getenv("BINANCE_API_SECRET")
        
        if not self.api_key or not self.api_secret:
            logger.error("API Key or Secret missing. Please provide them via .env or arguments.")
            raise ValueError("BINANCE_API_KEY and BINANCE_API_SECRET are required.")

        try:
            # Initialize Binance client. For futures testnet, testnet=True routes futures endpoints correctly.
            logger.debug("Initializing Binance Client with testnet=True")
            self.client = Client(self.api_key, self.api_secret, testnet=True)
            
            # Test connectivity by pinging the futures server
            self.client.futures_ping()
            logger.info("Successfully connected to Binance Futures Testnet.")
        except BinanceAPIException as e:
            logger.error(f"Binance API Exception during initialization: {e.status_code} - {e.message}")
            raise
        except BinanceRequestException as e:
            logger.error(f"Binance Request Exception during initialization: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during client initialization: {e}")
            raise
            
    def get_client(self) -> Client:
        return self.client
