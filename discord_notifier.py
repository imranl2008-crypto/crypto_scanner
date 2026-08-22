import requests

def send_discord_alert(webhook_url, signal):
    if not webhook_url or "YOUR_DISCORD" in webhook_url:
        print("Discord Webhook URL not configured. Printing alert layout instead:")
        print(signal)
        return
        
    setup = signal['setup']
    emoji = "🟢" if signal['type'] == 'support' else "🔴"
    
    embed = {
        "title": f"{emoji} S&R Alert: {signal['pair']}",
        "color": 3066993 if signal['type'] == 'support' else 15158332,
        "fields": [
            {"name": "Level Type", "value": f"{signal['type'].upper()} @ {signal['level']}", "inline": True},
            {"name": "Current Price", "value": str(signal['price']), "inline": True},
            {"name": "Distance", "value": f"{signal['distance_pct']}%", "inline": True},
            {"name": "Entry Price", "value": str(setup['entry']), "inline": True},
            {"name": "Stop Loss", "value": str(setup['stop_loss']), "inline": True},
            {"name": "Target", "value": str(setup['target']), "inline": True},
            {"name": "Risk:Reward", "value": f"1:{setup['risk_reward']}", "inline": True}
        ],
        "footer": {"text": "Crypto Price Action S&R Model"}
    }
    
    payload = {"embeds": [embed]}
    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        if response.status_code not in [200, 204]:
            print(f"Failed to send Discord alert: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error sending Discord webhook: {e}")
