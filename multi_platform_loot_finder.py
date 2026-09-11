import os
import re
import requests
import xml.etree.ElementTree as ET

# 1. SYSTEM GATEWAY SETTINGS
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "YOUR_TELEGRAM_CHAT_ID")
LOOT_DISCOUNT_THRESHOLD = 20.0  # Set low at 20.0 so you immediately get test alerts right now!

def send_loot_alert(deal_title: str, deal_link: str):
    """Sends a beautifully formatted push notification alert directly to your phone via Telegram."""
    url = f"https://telegram.org{TELEGRAM_TOKEN}/sendMessage"
    
    alert_message = (
        f"🚨 *⚠️ LOOT DEAL DETECTED* 🚨\n\n"
        f"📦 *Deal:* {deal_title}\n"
        f"🏪 *Target Platform:* ONLINE / QUICK COMMERCE\n\n"
        f"👉 *View Live Deal:* {deal_link}\n\n"
        f"👉 _Check your delivery apps immediately to grab it before it sells out!_"
    )
    
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": alert_message, "parse_mode": "Markdown"}
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            print(f"🚀 Alert dispatched successfully for: {deal_title}")
    except Exception as e:
        print(f"⚠️ Telegram alert failed: {e}")

def monitor_public_deal_rss():
    """Scrapes the raw public RSS data highway where deals are published instantly in pure text format."""
    print("🔄 Connecting to live public deal RSS data pipelines...")
    
    # Official public text feed URL that bypasses all web loading blocks
    target_url = "https://desidime.com"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(target_url, headers=headers, timeout=20)
        if response.status_code == 200:
            # Parse the clean XML data structure
            root = ET.fromstring(response.content)
            items = root.findall(".//item")
            print(f"📊 RSS Feed Matrix: Uncovered {len(items)} live deal text components.")
            
            for item in items:
                try:
                    title_elem = item.find("title")
                    link_elem = item.find("link")
                    
                    if title_elem is not None and link_elem is not None:
                        title_clean = title_elem.text.strip()
                        full_link = link_elem.text.strip()
                        
                        # Match parameters: check if title contains key terms or massive percentage drops
                        is_target_platform = any(word in title_clean.lower() for word in ["blinkit", "zepto", "instamart", "bigbasket", "haldiram", "amazon", "flipkart", "grocery", "food"])
                        
                        has_high_discount = False
                        pct_matches = re.findall(r"(\d+)%", title_clean)
                        for pct in pct_matches:
                            if float(pct) >= LOOT_DISCOUNT_THRESHOLD:
                                has_high_discount = True
                                
                        if any(word in title_clean.lower() for word in ["loot", "glitch", "free", "bug", "error"]):
                            has_high_discount = True
                        
                        # If a match executes, trigger the push alert immediately
                        if is_target_platform or has_high_discount:
                            print(f"✅ Hit Verified Feed Item: {title_clean}")
                            send_loot_alert(title_clean, full_link)
                except Exception as inner_e:
                    continue
        else:
            print(f"⚠️ RSS Feed access returned status code: {response.status_code}")
    except Exception as e:
        print(f"⚠️ System connection error: {e}")

if __name__ == "__main__":
    monitor_public_deal_rss()
