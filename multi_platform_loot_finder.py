import os
import re
import requests

# 1. SYSTEM GATEWAY SETTINGS
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "YOUR_TELEGRAM_CHAT_ID")
LOOT_DISCOUNT_THRESHOLD = 20.0  # Set at 20.0 to guarantee immediate push notifications!

def send_loot_alert(deal_title: str):
    """Sends a formatted push notification alert directly to your phone via Telegram."""
    url = f"https://telegram.org{TELEGRAM_TOKEN}/sendMessage"
    
    alert_message = (
        f"🚨 *⚠️ LOOT DEAL ALERT* 🚨\n\n"
        f"📦 *Deal Details:* {deal_title}\n\n"
        f"👉 _Check your quick commerce or shopping apps immediately to verify stock!_"
    )
    
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": alert_message, "parse_mode": "Markdown"}
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            print(f"🚀 Alert successfully pushed to phone: {deal_title[:30]}...")
    except Exception as e:
        print(f"⚠️ Telegram webhook alert failed: {e}")

def monitor_public_deal_channel():
    """Scrapes raw text streams from public web-mirrors of prominent deal hunter feeds."""
    print("🔄 Connecting to live public deal text data streams...")
    
    # Accessing an open, raw web mirror of a major community deal broadcasting channel
    target_url = "https://t.me"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(target_url, headers=headers, timeout=20)
        if response.status_code == 200:
            raw_html = response.text
            
            # Isolate the text data blocks representing individual message updates
            messages = re.findall(r'<div class="tgme_widget_message_text[^>]*>(.*?)</div>', raw_html, re.DOTALL)
            print(f"📊 Live Data Stream: Successfully loaded {len(messages)} deal updates.")
            
            for msg in messages:
                # Strip out basic html formatting elements like line breaks or link anchors
                clean_text = re.sub(r'<[^>]+>', ' ', msg)
                clean_text = clean_text.replace("&amp;", "&").replace("  ", " ").strip()
                
                if not clean_text:
                    continue
                
                # Check for target tracking keywords
                is_target_platform = any(word in clean_text.lower() for word in [
                    "blinkit", "zepto", "instamart", "bigbasket", "haldiram", 
                    "amazon", "flipkart", "grocery", "loot", "glitch", "free"
                ])
                
                # Verify percentage parameters
                has_high_discount = False
                pct_matches = re.findall(r"(\d+)%", clean_text)
                for pct in pct_matches:
                    if float(pct) >= LOOT_DISCOUNT_THRESHOLD:
                        has_high_discount = True
                        
                if any(word in clean_text.lower() for word in ["loot", "glitch", "free", "bug", "error"]):
                    has_high_discount = True
                
                # If a true bargain pattern executes, fire the webhook instantly
                if is_target_platform or has_high_discount:
                    # Shorten text strings down to match standard scannable messaging formats
                    display_text = clean_text[:150] + "..." if len(clean_text) > 150 else clean_text
                    print(f"✅ Found Active Match: {display_text}")
                    send_loot_alert(display_text)
        else:
            print(f"⚠️ Feed access returned status code: {response.status_code}")
    except Exception as e:
        print(f"⚠️ System connection error: {e}")

if __name__ == "__main__":
    monitor_public_deal_channel()
