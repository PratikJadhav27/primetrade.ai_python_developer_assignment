import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger():
    """
    Configures and returns a logger for the trading bot.
    Logs are written to 'trading_bot.log' and standard output.
    """
    logger = logging.getLogger("TradingBot")
    logger.setLevel(logging.DEBUG)  # Capture all levels, filter at handlers

    # Formatter for log messages
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # File handler (Rotating to prevent huge files)
    file_handler = RotatingFileHandler(
        "trading_bot.log", maxBytes=5*1024*1024, backupCount=2
    )
    file_handler.setLevel(logging.DEBUG)  # Write everything to file
    file_handler.setFormatter(formatter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)  # Only warnings/errors to console
    console_handler.setFormatter(formatter)

    # Avoid duplicate logs if setup_logger is called multiple times
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

# Create a singleton logger instance to be used across the bot
logger = setup_logger()
