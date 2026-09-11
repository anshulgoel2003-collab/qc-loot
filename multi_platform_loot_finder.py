import os
import re
import requests

# 1. SYSTEM GATEWAY SETTINGS
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "YOUR_TELEGRAM_CHAT_ID")
LOOT_DISCOUNT_THRESHOLD = 20.0  # Kept low at 20.0 to guarantee immediate test alerts right now!

def send_loot_alert(deal_title: str, deal_link: str):
    """Sends a beautifully formatted push notification alert directly to your phone via Telegram."""
    url = f"https://telegram.org{TELEGRAM_TOKEN}/sendMessage"
    
    alert_message = (
        f"🚨 *⚠️ LOOT DEAL DETECTED* 🚨\n\n"
        f"📦 *Deal:* {deal_title}\n"
        f"🏪 *Target Platform:* QUICK COMMERCE / ONLINE\n\n"
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

def monitor_public_deal_rss_robust():
    """Parses live deal text directly using raw regex patterns to handle broken special characters."""
    print("🔄 Connecting to live public deal RSS data pipelines...")
    
    target_url = "https://desidime.com"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(target_url, headers=headers, timeout=20)
        if response.status_code == 200:
            raw_text = response.text
            
            # Use raw regular expressions to isolate <title> and <link> nodes without using strict XML parsers
            # This completely avoids all formatting crashes caused by raw symbols!
            titles = re.findall(r"<title>(.*?)</title>", raw_text)
            links = re.findall(r"<link>(.*?)</link>", raw_text)
            
            # The first item in an RSS feed is always the website header, so we skip it
            deal_titles = titles[1:]
            deal_links = links[1:]
            
            print(f"📊 RSS Feed Matrix: Successfully loaded {len(deal_titles)} live data nodes.")
            
            for title_clean, full_link in zip(deal_titles, deal_links):
                # Clean up html formatting artifacts like &amp; down to raw readable characters
                title_clean = title_clean.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").strip()
                full_link = full_link.strip()
                
                # Match parameters: check if title contains target tracking keywords
                is_target_platform = any(word in title_clean.lower() for word in [
                    "blinkit", "zepto", "instamart", "bigbasket", "haldiram", 
                    "amazon", "flipkart", "grocery", "food", "swiggy", "zomato"
                ])
                
                has_high_discount = False
                pct_matches = re.findall(r"(\d+)%", title_clean)
                for pct in pct_matches:
                    if float(pct) >= LOOT_DISCOUNT_THRESHOLD:
                        has_high_discount = True
                        
                if any(word in title_clean.lower() for word in ["loot", "glitch", "free", "bug", "error", "pricing"]):
                    has_high_discount = True
                
                # If it matches our keyword tracking rules, fire the notification instantly
                if is_target_platform or has_high_discount:
                    print(f"✅ Verified Active Match: {title_clean}")
                    send_loot_alert(title_clean, full_link)
        else:
            print(f"⚠️ RSS Feed access returned status code: {response.status_code}")
    except Exception as e:
        print(f"⚠️ System connection error: {e}")

if __name__ == "__main__":
    monitor_public_deal_rss_robust()
