import ccxt


def get_top_coins_universe(limit=300, quote="USDT"):
    """
    Returns a list of dicts: [{'pair': 'BTC/USDT', 'volume': 123456.0}, ...]
    sorted by 24h quote volume, descending.
    """
    print(f"Fetching top {limit} coins from KuCoin...")
    exchange = ccxt.kucoin({
        'enableRateLimit': True
    })
    exchange.load_markets()

    all_tickers = exchange.fetch_tickers()

    symbols_data = []
    for symbol, market in exchange.markets.items():
        if market.get('spot') and market.get('quote') == quote and market.get('active'):
            ticker = all_tickers.get(symbol)
            if not ticker:
                continue
            quote_volume = ticker.get('quoteVolume') or 0
            symbols_data.append({
                'pair': symbol,
                'volume': quote_volume
            })

    symbols_data.sort(key=lambda x: x['volume'], reverse=True)
    top_coins = symbols_data[:limit]

    print(f"Successfully loaded {len(top_coins)} coins from KuCoin.")
    return top_coins