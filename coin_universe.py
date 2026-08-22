import ccxt

def get_top_coins_universe(limit=300, quote="USDT"):
    print(f"Fetching top {limit} coins from Bybit...")
    exchange = ccxt.bybit({
        'enableRateLimit': True
    })
    exchange.load_markets()
    
    # Filter for active spot markets with the given quote currency
    symbols_data = []
    for symbol, market in exchange.markets.items():
        if market.get('spot') and market.get('quote') == quote and market.get('active'):
            try:
                # Fetch 24hr ticker to get volume
                ticker = exchange.fetch_ticker(symbol)
                quote_volume = ticker.get('quoteVolume') or 0
                symbols_data.append({
                    'symbol': symbol,
                    'volume': quote_volume
                })
            except Exception:
                continue
                
    # Sort by 24h volume descending and pick top N
    symbols_data.sort(key=lambda x: x['volume'], reverse=True)
    top_symbols = [item['symbol'] for item in symbols_data[:limit]]
    
    print(f"Successfully loaded {len(top_symbols)} coins from Bybit.")
    return top_symbols
