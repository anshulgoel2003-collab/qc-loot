import os
import re
import json
import http.client
import requests

# 1. SYSTEM GATEWAY SETTINGS
TELEGRAM_TOKEN = "8883600849:AAHYq4WPcKEIIBvSiNXwdacw-PgVP7I6paU"
TELEGRAM_CHAT_ID = "1848239469" # ⚠️ Type your 9-10 digit number here!
LOOT_DISCOUNT_THRESHOLD = 50.0  # Captures only extreme 75% to 99% OFF glitch clearance sales!

def send_loot_alert(deal_title: str, deal_link: str):
    """Pushes live filtered alerts straight to your phone using secure low-level socket handshakes."""
    url = f"https://telegram.org{TELEGRAM_TOKEN}/sendMessage"
    
    alert_message = (
        f"🚨 *⚠️ 75%+ LOOT DEAL DETECTED* 🚨\n\n"
        f"📦 *Deal:* {deal_title}\n"
        f"🏪 *Target Platform:* QUICK COMMERCE / ONLINE\n\n"
        f"👉 *View Live Deal Thread:* {deal_link}\n"
        f"👉 _Open your delivery app immediately and change your location to grab it!_"
    )
    
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": alert_message,
        "parse_mode": "Markdown"
    }
    
    connection = http.client.HTTPSConnection("api.telegram.org")
    headers = {"Content-type": "application/json"}
    try:
        connection.request("POST", f"/bot{TELEGRAM_TOKEN}/sendMessage", json.dumps(payload), headers)
        res = connection.getresponse()
        if res.status == 200:
            print(f"🚀 Alert successfully pushed: {deal_title[:30]}...")
    except Exception as e:
        print(f"⚠️ Telegram delivery exception: {e}")
    finally:
        connection.close()

def monitor_live_loot_feeds():
    """Scrapes public deal forums where users instantly post active platform pricing bugs."""
    print("🔄 Connecting to live public deal aggregator pipelines...")
    
    target_url = "https://desidime.com"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(target_url, headers=headers, timeout=20)
        if response.status_code == 200:
            raw_html = response.text
            
            # Match standard deal block structures using regex text isolation patterns
            deal_blocks = re.findall(r'<a class="deal-title"[^>]*href="([^"]+)"[^>]*>([^<]+)</a>', raw_html)
            print(f"📊 Live Data Stream: Successfully loaded {len(deal_blocks)} deal entries.")
            
            for link, title in deal_blocks:
                title_clean = title.strip()
                full_link = f"https://desidime.com{link}"
                
                # Filter for target apps or heavy terms
                is_target_platform = any(word in title_clean.lower() for word in [
                    "blinkit", "zepto", "instamart", "bigbasket", "haldiram", 
                    "amazon", "flipkart", "grocery", "swiggy", "zomato"
                ])
                
                # Calculate percentage markings inside the text titles
                has_high_discount = False
                pct_matches = re.findall(r"(\d+)%", title_clean)
                for pct in pct_matches:
                    if float(pct) >= LOOT_DISCOUNT_THRESHOLD:
                        has_high_discount = True
                        
                if any(word in title_clean.lower() for word in ["loot", "glitch", "free", "bug", "error"]):
                    has_high_discount = True
                
                # If a true bargain pattern executes, fire the webhook instantly
                if is_target_platform and has_high_discount:
                    print(f"✅ Found Active Match: {title_clean}")
                    send_loot_alert(title_clean, full_link)
        else:
            print(f"⚠️ Feed access returned status code: {response.status_code}")
    except Exception as e:
        print(f"⚠️ System connection error: {e}")

if __name__ == "__main__":
    monitor_live_loot_feeds()
