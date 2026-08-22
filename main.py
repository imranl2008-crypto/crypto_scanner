import time
import sys
import schedule
from config import (
    DISCORD_WEBHOOK_URL, TOP_N_COINS, TIMEFRAME, 
    PROXIMITY_THRESHOLD, ALERT_COOLDOWN_HOURS, MIN_RISK_REWARD, DB_PATH
)
from coin_universe import get_top_coins_universe
from data_fetcher import fetch_ohlcv_data
from levels_engine import compute_support_resistance_levels
from storage import init_db, save_levels, get_levels, check_cooldown, set_cooldown
from signal_engine import process_signals
from discord_notifier import send_discord_alert

def job_recompute_levels():
    print("\n--- Starting Daily Levels Recomputation ---")
    init_db(DB_PATH)
    coins = get_top_coins_universe(TOP_N_COINS)
    
    for coin in coins:
        pair = coin['pair']
        print(f"Computing levels for {pair}...")
        df = fetch_ohlcv_data(pair, timeframe=TIMEFRAME, limit=150)
        if df is not None:
            levels = compute_support_resistance_levels(df)
            save_levels(pair, levels, DB_PATH)
        time.sleep(0.5)
    print("--- Levels Recomputation Complete ---\n")

def job_check_signals():
    print("\n--- Running Candle Close Signal Check ---")
    init_db(DB_PATH)
    coins = get_top_coins_universe(TOP_N_COINS)
    
    for coin in coins:
        pair = coin['pair']
        levels = get_levels(pair, DB_PATH)
        if not levels:
            continue
            
        df = fetch_ohlcv_data(pair, timeframe=TIMEFRAME, limit=50)
        signals = process_signals(pair, df, levels, PROXIMITY_THRESHOLD)
        
        for sig in signals:
            level = sig['level']
            if sig['setup']['risk_reward'] >= MIN_RISK_REWARD:
                if check_cooldown(pair, level, ALERT_COOLDOWN_HOURS, DB_PATH):
                    print(f"Triggering alert for {pair} at level {level}!")
                    send_discord_alert(DISCORD_WEBHOOK_URL, sig)
                    set_cooldown(pair, level, DB_PATH)
                else:
                    print(f"Signal found for {pair} at {level}, but under active cooldown.")
        time.sleep(0.3)
    print("--- Signal Check Complete ---\n")

if __name__ == "__main__":
    init_db(DB_PATH)
    print("Running single-pass test execution...")
    job_recompute_levels()
    job_check_signals()
