"""
Standalone test for Discord alert delivery.
Bypasses the entire scan/touch/hold pipeline and calls send_discord_alert()
directly with realistic dummy data, to confirm the webhook + formatting work.
"""

from config import DISCORD_WEBHOOK_URL
from discord_notifier import send_discord_alert

dummy_signal = {
    "pair": "BTC/USDT",
    "type": "support",
    "level": 61250.5,
    "price": 61300.2,
    "distance_pct": 0.08,
    "setup": {
        "entry": 61300.2,
        "stop_loss": 60800.0,
        "target": 62700.0,
        "risk_reward": 2.8
    }
}

print("Sending test alert to Discord...")
send_discord_alert(DISCORD_WEBHOOK_URL, dummy_signal)
print("Done. Check your Discord channel now.")