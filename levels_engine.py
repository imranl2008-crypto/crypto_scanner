import numpy as np
import pandas as pd

def compute_support_resistance_levels(df, num_bins=50):
    if df is None or len(df) < 30:
        return []
        
    price_min, price_max = df['low'].min(), df['high'].max()
    bins = np.linspace(price_min, price_max, num_bins)
    df['price_bin'] = pd.cut(df['close'], bins=bins, labels=False)
    
    volume_profile = df.groupby('price_bin')['volume'].sum()
    hvn_bins = volume_profile.nlargest(5).index.tolist()
    
    hvn_levels = [float((bins[b] + bins[b+1]) / 2) for b in hvn_bins if b + 1 < len(bins)]
    
    pivots = []
    window = 5
    for i in range(window, len(df) - window):
        high_slice = df['high'].iloc[i-window:i+window+1]
        low_slice = df['low'].iloc[i-window:i+window+1]
        
        if df['high'].iloc[i] == high_slice.max():
            pivots.append(('resistance', df['high'].iloc[i]))
        if df['low'].iloc[i] == low_slice.min():
            pivots.append(('support', df['low'].iloc[i]))
            
    raw_levels = hvn_levels + [p[1] for p in pivots]
    if not raw_levels:
        return []
        
    raw_levels.sort()
    clustered = []
    cluster_threshold = (price_max - price_min) * 0.015
    
    current_cluster = [raw_levels[0]]
    for level in raw_levels[1:]:
        if level - current_cluster[-1] <= cluster_threshold:
            current_cluster.append(level)
        else:
            clustered.append(np.mean(current_cluster))
            current_cluster = [level]
    clustered.append(np.mean(current_cluster))
    
    scored_levels = []
    current_price = df['close'].iloc[-1]
    
    for level in clustered:
        touches = 0
        for _, row in df.iterrows():
            if abs(row['low'] - level) / level <= 0.01 or abs(row['high'] - level) / level <= 0.01:
                touches += 1
                
        level_type = 'support' if level < current_price else 'resistance'
        score = touches * 2 + (1 if level in hvn_levels else 0)
        
        scored_levels.append({
            "level": round(level, 4),
            "type": level_type,
            "score": int(score),
            "touches": touches
        })
        
    scored_levels = sorted(scored_levels, key=lambda x: x['score'], reverse=True)
    return scored_levels[:6]
