import requests

def get_top_coins_universe(limit=300, quote="USDT"):
    print(f"Fetching top {limit} coins from CoinGecko...")
    top_symbols = []
    per_page = 250
    pages = (limit // per_page) + (1 if limit % per_page != 0 else 0)
    
    for page in range(1, pages + 1):
        url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page={per_page}&page={page}&sparkline=false"
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                for coin in data:
                    symbol = coin['symbol'].upper() + f"/{quote}"
                    if symbol not in top_symbols:
                        top_symbols.append(symbol)
            else:
                print(f"CoinGecko API error on page {page}: {response.status_code}")
        except Exception as e:
            print(f"Error fetching CoinGecko data: {e}")
            
    top_symbols = top_symbols[:limit]
    print(f"Successfully loaded {len(top_symbols)} coins from CoinGecko.")
    return top_symbols
