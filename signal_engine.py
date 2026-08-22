import numpy as np
import pandas as pd

def calculate_atr(df, period=14):
    high_low = df['high'] - df['low']
    high_close = np.abs(df['high'] - df['close'].shift())
    low_close = np.abs(df['low'] - df['close'].shift())
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = ranges.max(axis=1)
    return true_range.rolling(period).mean().iloc[-1]

def process_signals(pair, df, levels, proximity_threshold=0.005):
    if df is None or len(df) < 15:
        return []
        
    current_price = df['close'].iloc[-1]
    prev_close = df['close'].iloc[-2]
    atr = calculate_atr(df)
    signals = []
    
    for l_data in levels:
        level = l_data['level']
        l_type = l_data['type']
        
        distance = abs(current_price - level) / level
        if distance <= proximity_threshold:
            is_hold = False
            if l_type == 'support' and current_price >= level and prev_close <= current_price:
                is_hold = True
            elif l_type == 'resistance' and current_price <= level and prev_close >= current_price:
                is_hold = True
            
            if is_hold:
                if l_type == 'support':
                    entry = current_price
                    stop_loss = level - (1.5 * atr)
                    target = entry + (2.5 * (entry - stop_loss))
                else:
                    entry = current_price
                    stop_loss = level + (1.5 * atr)
                    target = entry - (2.5 * (stop_loss - entry))
                    
                risk = abs(entry - stop_loss)
                reward = abs(target - entry)
                rr = round(reward / risk, 2) if risk > 0 else 0
                
                signals.append({
                    "pair": pair,
                    "level": level,
                    "type": l_type,
                    "price": current_price,
                    "distance_pct": round(distance * 100, 2),
                    "setup": {
                        "entry": round(entry, 4),
                        "stop_loss": round(stop_loss, 4),
                        "target": round(target, 4),
                        "risk_reward": rr
                    }
                })
    return signals
