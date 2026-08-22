import ccxt
import pandas as pd

def fetch_ohlcv_data(symbol, timeframe="6h", limit=100):
    exchange = ccxt.gate({
        'enableRateLimit': True
    })
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df
    except Exception as e:
        print(f"Error fetching data for {symbol} from Gate.io: {e}")
        return None
