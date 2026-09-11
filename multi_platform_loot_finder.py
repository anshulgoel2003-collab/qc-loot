import os
import re
import requests

# 1. SYSTEM GATEWAY SETTINGS
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "YOUR_TELEGRAM_CHAT_ID")
LOOT_DISCOUNT_THRESHOLD = 20.0  # Set low at 20.0 to guarantee you get immediate test alerts!

def send_loot_alert(deal_title: str, deal_link: str):
    """Sends a formatted push notification alert directly to your phone via Telegram."""
    url = f"https://telegram.org{TELEGRAM_TOKEN}/sendMessage"
    
    alert_message = (
        f"🚨 *⚠️ LOOT DEAL DETECTED* 🚨\n\n"
        f"📦 *Deal:* {deal_title}\n"
        f"🏪 *Target Platform:* QUICK COMMERCE / ONLINE\n\n"
        f"👉 *View Live Deal Thread:* {deal_link}\n\n"
        f"👉 _Open your delivery app immediately and grab it!_"
    )
    
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": alert_message, "parse_mode": "Markdown"}
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            print(f"🚀 Alert dispatched successfully for: {deal_title}")
    except Exception as e:
        print(f"⚠️ Telegram alert failed: {e}")

def monitor_public_deal_aggregators():
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
            print(f"📊 Aggregator Feed: Uncovered {len(deal_blocks)} live market deal updates.")
            
            for link, title in deal_blocks:
                title_clean = title.strip()
                full_link = f"https://desidime.com{link}"
                
                # Check if the title text matches quick commerce apps or key terms
                is_target_platform = any(word in title_clean.lower() for word in ["blinkit", "zepto", "instamart", "bigbasket", "haldiram", "amazon", "deal", "off"])
                
                # Look for explicit percentage markings in the title text
                has_high_discount = False
                pct_matches = re.findall(r"(\d+)%", title_clean)
                for pct in pct_matches:
                    if float(pct) >= LOOT_DISCOUNT_THRESHOLD:
                        has_high_discount = True
                        
                if "loot" in title_clean.lower() or "glitch" in title_clean.lower() or "free" in title_clean.lower():
                    has_high_discount = True
                
                # If it matches our criteria, fire it to Telegram instantly
                if is_target_platform or has_high_discount:
                    print(f"✅ Found matching feed item: {title_clean}")
                    send_loot_alert(title_clean, full_link)
        else:
            print(f"⚠️ Feed access returned status code: {response.status_code}")
    except Exception as e:
        print(f"⚠️ System connection error: {e}")

if __name__ == "__main__":
    monitor_public_deal_aggregators()
