import MetaTrader5 as mt5
import time
import pandas as pd

def calculate_RSI(data, period):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).fillna(0)
    loss = (delta.where(delta < 0, 0).abs()).fillna(0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_SMA(data, period):
    return data.rolling(window=period).mean()

def close_position(position_id):
    position_info = mt5.positions_get(ticket=position_id)
    if position_info is not None and len(position_info) > 0:
        close_request = {
            "position": position_id,
            "action": mt5.TRADE_ACTION_DEAL,
        }
        result = mt5.order_send(close_request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print("Close order failed, retcode={}".format(result.retcode))
        else:
            time.sleep(3)
            position_info = mt5.positions_get(ticket=position_id)
            if position_info is not None and len(position_info) > 0:
                print("Closed position profit: ", position_info[0].profit)

symbol = "EURUSD"
lot = 0.5
moving_avg_period = 12
rsi_period = 14
trade_profit = 50  # Trade profit değeri
stop_loss = trade_profit / 2  # Stop loss değeri

timeframe = mt5.TIMEFRAME_M15

if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

position_id = None
position_type = None

while True:
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, rsi_period + moving_avg_period)
    data = pd.DataFrame(rates, columns=['time', 'open', 'high', 'low', 'close', 'tick_volume', 'spread', 'real_volume'])
    data['time'] = pd.to_datetime(data['time'], unit='s')
    data['rsi'] = calculate_RSI(data['close'], rsi_period)
    data['sma'] = calculate_SMA(data['close'], moving_avg_period)

    last_rsi = data['rsi'].iloc[-1]
    moving_avg = data['sma'].iloc[-1]
    last_close = data['close'].iloc[-1]

    if last_rsi <= 30 and last_close > moving_avg:
        if position_type != 'BUY':
            print("RSI and Moving Average conditions met for BUY.")
            if position_id is not None:
                print("Closing SELL position.")
                close_position(position_id)

            take_profit = last_close + trade_profit
            stop_loss_level = last_close - stop_loss

            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": lot,
                "type": mt5.ORDER_TYPE_BUY,
                "price": last_close,
                "magic": 234000,
                "comment": "python script open",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
                "tp": take_profit,
                "sl": stop_loss_level
            }
            result = mt5.order_send(request)
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                print("Buy order_send failed, retcode={}".format(result.retcode))
            else:
                print("BUY order passed. Position ID: ", result.order)
                position_id = result.order
                position_type = 'BUY'

    elif last_rsi >= 70 and last_close < moving_avg:
        if position_type != 'SELL':
            print("RSI and Moving Average conditions met for SELL.")
            if position_id is not None:
                print("Closing BUY position.")
                close_position(position_id)

            take_profit = last_close - trade_profit
            stop_loss_level = last_close + stop_loss

            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": lot,
                "type": mt5.ORDER_TYPE_SELL,
                "price": last_close,
                "magic": 234000,
                "comment": "python script open",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
                "tp": take_profit,
                "sl": stop_loss_level
            }
            result = mt5.order_send(request)
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                print("Sell order_send failed, retcode={}".format(result.retcode))
            else:
                print("SELL order passed. Position ID: ", result.order)
                position_id = result.order
                position_type = 'SELL'

    print("Last RSI: ", last_rsi)
    print("Moving Average: ", moving_avg)
    print("Last Close: ", last_close)

    time.sleep(10)
