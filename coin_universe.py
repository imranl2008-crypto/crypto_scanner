import time
import requests
import ccxt

def get_binance_symbols():
    exchange = ccxt.binance()
    exchange.load_markets()
    return list(exchange.markets.keys())

def get_top_coins_universe(limit=300):
    print(f"Fetching top {limit} coins from CoinGecko...")
    binance_symbols = get_binance_symbols()
    valid_pairs = []
    
    url = "https://api.coingecko.com/api/v3/coins/markets"
    per_page = 250
    pages = (limit // per_page) + 1
    
    collected = []
    for page in range(1, pages + 1):
        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": per_page,
            "page": page,
            "sparkline": "false"
        }
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                collected.extend(data)
                time.sleep(1.2)
            else:
                print(f"CoinGecko error: {response.status_code}")
                break
        except Exception as e:
            print(f"Error fetching CoinGecko market data: {e}")
            break
            
    collected = collected[:limit]
    
    for coin in collected:
        symbol_upper = coin['symbol'].upper()
        pair = f"{symbol_upper}/USDT"
        if pair in binance_symbols:
            valid_pairs.append({
                "coin_id": coin['id'],
                "symbol": symbol_upper,
                "pair": pair,
                "market_cap_rank": coin.get('market_cap_rank')
            })
            
    print(f"Mapped {len(valid_pairs)} coins to Binance pairs.")
    return valid_pairs
