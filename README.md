# Binance Futures Testnet Trading Bot

This is a Python-based trading bot that interfaces with the Binance Futures Testnet (USDT-M) to place MARKET, LIMIT, and STOP_MARKET orders.

## Features
- **Core Requirements**: Places Market and Limit orders, supports BUY/SELL.
- **Enhanced CLI**: Built with `Typer` and `Rich` for input validation and beautiful terminal output.
- **Logging**: Implements a RotatingFileHandler to log all API requests and errors into `trading_bot.log`.
- **Bonus Implementation**: Added `STOP_MARKET` orders and an enhanced CLI UX.

## Setup Instructions

### 1. Prerequisites
- Python 3.8+
- A Binance Futures Testnet account. 
- API Key and API Secret from your testnet account.

### 2. Installation
Clone or unzip the repository, then navigate into the project directory.

```bash
# Create a virtual environment (optional but recommended)
python -m venv venv
# Activate the virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration
Copy the sample environment file to `.env` and fill in your API credentials.

```bash
cp .env.example .env
```
Edit `.env` to include your Binance Futures Testnet keys:
```env
BINANCE_API_KEY=your_testnet_api_key_here
BINANCE_API_SECRET=your_testnet_api_secret_here
```

## How to Run Examples

You can see all available commands and arguments by running:
```bash
python cli.py --help
```

### 1. Place a MARKET Order
Buy 0.01 BTC at the current market price:
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

### 2. Place a LIMIT Order
Sell 0.01 BTC at a specific price (e.g., 90000):
```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 90000
```

### 3. Place a STOP_MARKET Order (Bonus)
Place a Stop Market Sell order triggered when the price drops to 85000:
```bash
python cli.py --symbol BTCUSDT --side SELL --type STOP_MARKET --quantity 0.01 --stop-price 85000
```

## Logs
All bot activity, including successful API requests, validation errors, and network exceptions, are logged to `trading_bot.log`. This file will be created automatically in the root directory upon the first execution.

## Assumptions & Known Limitations
- The testnet base URL is handled internally by the `python-binance` library when initialized with `testnet=True`.
- Limit orders default to `timeInForce='GTC'` (Good Till Cancelled), which is standard for Binance.
- **Geographical API Limitations:** Due to recent FIU India compliance regulations, Indian KYC-verified Binance accounts are restricted from accessing Futures trading. The new unified Binance Demo environment (`demo.binance.com`) inherits these live account restrictions. Consequently, the "Enable Futures" API permission is completely hidden/disabled for Indian testnet accounts, making it impossible to generate functional Futures API keys in this region without using a non-KYC international account or a VPN during account creation. The provided log files demonstrate successful execution under an unrestricted environment.
