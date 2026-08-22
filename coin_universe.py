import ccxt

def get_top_coins_universe(limit=300, quote="USDT"):
    print(f"Fetching top {limit} coins from KuCoin...")
    exchange = ccxt.kucoin({
        'enableRateLimit': True
    })
    exchange.load_markets()
    
    symbols_data = []
    for symbol, market in exchange.markets.items():
        if market.get('spot') and market.get('quote') == quote and market.get('active'):
            try:
                ticker = exchange.fetch_ticker(symbol)
                quote_volume = ticker.get('quoteVolume') or 0
                symbols_data.append({
                    'symbol': symbol,
                    'volume': quote_volume
                })
            except Exception:
                continue
                
    symbols_data.sort(key=lambda x: x['volume'], reverse=True)
    top_symbols = [item['symbol'] for item in symbols_data[:limit]]
    
    print(f"Successfully loaded {len(top_symbols)} coins from KuCoin.")
    return top_symbols
