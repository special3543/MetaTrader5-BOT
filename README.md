# MetaTrader5-BOT

# Automated Trading with MetaTrader5

This project provides an example of automated trading using Python with the MetaTrader5 platform. The code implements the RSI (Relative Strength Index) and Moving Average strategy on the EUR/USD currency pair.

## Requirements

- Python 3.x
- MetaTrader5 Python package

You can install the required Python package using the following command:

pip install MetaTrader5


## Usage

1. Download and install the MetaTrader5 platform.
2. Download or copy the project files.
3. Run the project in a Python 3.x environment.

```bash
python trading_bot.py

## Strategy Description
The strategy used in this project makes trading decisions based on analyzing RSI and moving average values. The currency pair chosen for trading is EUR/USD. The main principles of the strategy are as follows:

- If the RSI value falls below 30 and the closing price is higher than the moving average, a "BUY" position is opened.
- If the RSI value rises above 70 and the closing price is lower than the moving average, a "SELL" position is opened.
- If there is an existing position and a signal in the opposite direction is received, the position is closed, and a new position is opened.

## Parameters
You can adjust the following parameters in the project file:

- symbol: The currency pair to trade (e.g., "EURUSD").
- lot: The trading volume (in lots).
- moving_avg_period: Moving average period.
- rsi_period: RSI period.
- trade_profit: The target trade profit (in pips).
- stop_loss: The stop-loss level (in pips).

Please adjust these parameters according to your strategy and preferences.


## Disclaimer
This code example is for educational purposes only. Before using it in live trading, please backtest your strategy and carefully evaluate its performance. Risk management strategies and using stop-loss levels are important. Every trading strategy involves risk and can result in losses.