import os
import re
import json
import http.client
import requests

# 1. SYSTEM GATEWAY SETTINGS
TELEGRAM_TOKEN = "8883600849:AAHYq4WPcKEIIBvSiNXwdacw-PgVP7I6paU"
TELEGRAM_CHAT_ID = "1848239469" # ⚠️ Type your 9-10 digit personal ID code here!
LOOT_DISCOUNT_THRESHOLD = 50.0  # Set at 50.0 for wide-ranging festive discount updates!

def send_loot_alert(deal_title: str, deal_link: str):
    """Sends a beautifully formatted push notification alert directly to your phone via Telegram."""
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": f"🚨 *⚠️ LIVE DEAL DETECTED* 🚨\n\n📦 *Item:* {deal_title}\n🏪 *Platform:* ONLINE / QUICK COMMERCE\n\n👉 *View Deal:* {deal_link}",
        "parse_mode": "Markdown"
    }
    
    connection = http.client.HTTPSConnection("api.telegram.org")
    headers = {"Content-type": "application/json"}
    try:
        connection.request("POST", f"/bot{TELEGRAM_TOKEN}/sendMessage", json.dumps(payload), headers)
        connection.getresponse()
    except Exception as e:
        print(f"⚠️ Telegram alert failed: {e}")
    finally:
        connection.close()

def monitor_live_loot_feeds():
    """Bypasses dynamic web layout blocks using a tag-free global data stream search."""
    print("🔄 Connecting to live public deal aggregator pipelines...")
    
    target_url = "https://www.desidime.com/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(target_url, headers=headers, timeout=20)
        if response.status_code == 200:
            raw_html = response.text
            
            # Bulletproof Fallback: Isolate all dynamic link patterns pointing directly to deal nodes
            raw_deals = re.findall(r'href="(/deals/[^"]+)"[^>]*>([^<]+)</a>', raw_html)
            
            # De-duplicate elements to clean data streams
            unique_deals = list(set(raw_deals))
            print(f"📊 Live Data Stream: Successfully loaded {len(unique_deals)} structural deal items.")
            
            matched_count = 0
            for link, title in unique_deals:
                title_clean = title.strip()
                full_link = f"https://www.desidime.com{link}"
                
                # Broad capture targeting across all consumer categories and brands
                is_target = any(word in title_clean.lower() for word in [
                    "blinkit", "zepto", "instamart", "bigbasket", "haldiram", 
                    "amazon", "flipkart", "grocery", "off", "sale", "rs", "₹"
                ])
                
                has_high_discount = False
                pct_matches = re.findall(r"(\d+)%", title_clean)
                for pct in pct_matches:
                    if float(pct) >= LOOT_DISCOUNT_THRESHOLD:
                        has_high_discount = True
                        
                if any(word in title_clean.lower() for word in ["loot", "glitch", "free", "bug", "price"]):
                    has_high_discount = True
                
                if is_target or has_high_discount:
                    matched_count += 1
                    print(f"✅ Found Active Match: {title_clean}")
                    send_loot_alert(title_clean, full_link)
                    
            print(f"🏁 Finished. Dispatched {matched_count} matching alerts to your phone.")
        else:
            print(f"⚠️ Feed access returned status code: {response.status_code}")
    except Exception as e:
        print(f"⚠️ System connection error: {e}")

if __name__ == "__main__":
    monitor_live_loot_feeds()
