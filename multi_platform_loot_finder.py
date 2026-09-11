import os
import requests

# 1. SYSTEM GATEWAY SETTINGS
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "YOUR_TELEGRAM_CHAT_ID")

def send_loot_alert(deal_title: str):
    """Pushes the message straight to your smartphone via Telegram API."""
    url = f"https://telegram.org{TELEGRAM_TOKEN}/sendMessage"
    
    alert_message = (
        f"🚨 *⚠️ LIVE LOOT ENGINE SUCCESS* 🚨\n\n"
        f"📦 *Simulated Deal Item:* {deal_title}\n"
        f"🏪 *Target Platform:* SYSTEM DIAGNOSTIC COMPLETED\n\n"
        f"✅ _Your cloud-to-phone alert pipeline is 100% verified and active!_"
    )
    
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": alert_message, "parse_mode": "Markdown"}
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            print(f"🚀 SUCCESS! Alert successfully pushed to phone chat!")
        else:
            print(f"❌ Telegram Error Code {response.status_code}: Check your Chat ID or confirm your Bot is started.")
    except Exception as e:
        print(f"⚠️ Network transmission error: {e}")

def run_guaranteed_api_test():
    """Fetches text components from an open, unblockable public API data highway to force a match."""
    print("🔄 Connecting to open public data API streams...")
    
    # Clean, unrestricted global text node endpoint
    target_url = "https://typicode.com"
    
    try:
        response = requests.get(target_url, timeout=15)
        if response.status_code == 200:
            data_items = response.json()
            print(f"📊 Live Data Array: Successfully read {len(data_items)} raw text elements.")
            
            if len(data_items) > 0:
                # Grab the very first text title node from the array
                test_title = data_items[0].get("title", "Premium Festive Loot Basket")
                print(f"✅ Condition met! Forcing immediate alert transmission...")
                send_loot_alert(test_title)
        else:
            print(f"⚠️ Public API returned unexpected status code: {response.status_code}")
    except Exception as e:
        print(f"⚠️ Core connection loop crash: {e}")

if __name__ == "__main__":
    run_guaranteed_api_test()
