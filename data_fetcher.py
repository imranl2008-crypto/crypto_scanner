import ccxt
import pandas as pd

def fetch_ohlcv_data(pair, timeframe='6h', limit=200):
    exchange = ccxt.binance({'enableRateLimit': True})
    try:
        ohlcv = exchange.fetch_ohlcv(pair, timeframe=timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df
    except Exception as e:
        print(f"Error fetching OHLCV for {pair}: {e}")
        return None
