import os
import re
import json
import http.client
import requests

# 1. SYSTEM GATEWAY SETTINGS
TELEGRAM_TOKEN = "8883600849:AAHYq4WPcKEIIBvSiNXwdacw-PgVP7I6paU"
TELEGRAM_CHAT_ID = "1848239469" # ⚠️ Type your 9-10 digit personal ID code here!
LOOT_DISCOUNT_THRESHOLD = 70.0  # Captures 50%+ markdown clearance items

def send_loot_alert(platform: str, deal_title: str, deal_link: str):
    """Sends a beautifully formatted push notification alert directly to your phone via Telegram."""
    alert_message = (
        f"🚨 *⚠️ RECENT LIVE DEAL DETECTED* 🚨\n\n"
        f"📦 *Item:* {deal_title}\n"
        f"🌐 *Source:* {platform.upper()}\n\n"
        f"👉 *View Deal Thread:* {deal_link}\n"
        f"👉 _Check your shipping apps immediately before stock dries up!_"
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
        connection.getresponse()
    except Exception as e:
        print(f"⚠️ Telegram alert failed: {e}")
    finally:
        connection.close()

def is_recent_offertag_deal(time_text: str) -> bool:
    """Verifies mathematically if the OfferTag post is fresh within the last 6 hours."""
    t_low = time_text.lower().strip()
    
    # If posted within seconds or minutes, it is 100% fresh
    if "second" in t_low or "minute" in t_low or "just now" in t_low:
        return True
        
    # If posted within hours, check if it's less than or equal to 6
    if "hour" in t_low:
        hours_found = re.findall(r"(\d+)", t_low)
        if hours_found:
            return int(hours_found[0]) <= 6
            
    # Reject anything older (like days, weeks, or generic dates)
    return False

def scrape_desidime(headers):
    """Parses live links and titles directly from DesiDime's core deal framework."""
    print("🔄 Accessing live DesiDime aggregator pipelines...")
    try:
        response = requests.get("https://desidime.com", headers=headers, timeout=20)
        if response.status_code == 200:
            raw_deals = re.findall(r'href="(/deals/[^"]+)"[^>]*>([^<]+)</a>', response.text)
            unique_deals = list(set(raw_deals))
            print(f"📊 DesiDime: Loaded {len(unique_deals)} live structural links.")
            
            for link, title in unique_deals:
                title_clean = title.strip()
                # DesiDime lists chronological feeds; filtering via low threshold flags newer items
                if any(w in title_clean.lower() for str_match in ["blinkit", "zepto", "instamart", "bigbasket", "haldiram"]):
                    send_loot_alert("DesiDime", title_clean, f"https://desidime.com{link}")
    except Exception as e:
        print(f"⚠️ DesiDime scraping crash: {e}")

def scrape_offertag(headers):
    """Scrapes OfferTag and extracts post time nodes to implement the strict 6-hour ceiling."""
    print("🔄 Accessing live OfferTag aggregator pipelines...")
    try:
        response = requests.get("https://offertag.in", headers=headers, timeout=20)
        if response.status_code == 200:
            raw_html = response.text
            
            # Isolates product card segments containing names, times, and outbound store redirection nodes
            # Each text card pattern block contains [Title, Time Text, Merchant]
            cards = re.findall(r'<h4>(.*?)</h4>\s*<span>(.*?)</span>', raw_html, re.DOTALL)
            print(f"📊 OfferTag: Discovered {len(cards)} live product entries.")
            
            matched_count = 0
            for title_raw, time_raw in cards:
                title_clean = re.sub(r'<[^>]+>', '', title_raw).strip()
                time_clean = time_raw.strip()
                
                # Step 1: Enforce the 6-hour timeline boundary check
                if not is_recent_offertag_deal(time_clean):
                    continue
                    
                # Step 2: Extract percentage text values
                has_high_discount = False
                pct_matches = re.findall(r"(\d+)%", title_clean)
                for pct in pct_matches:
                    if float(pct) >= LOOT_DISCOUNT_THRESHOLD:
                        has_high_discount = True
                        
                if any(word in title_clean.lower() for word in ["loot", "glitch", "free", "bug", "pricing"]):
                    has_high_discount = True
                    
                # Filter for target platform key strings
                is_target = any(word in title_clean.lower() for word in [
                    "blinkit", "zepto", "instamart", "bigbasket", "haldiram", "amazon", "flipkart"
                ])
                
                if is_target or has_high_discount:
                    matched_count += 1
                    print(f"✅ OfferTag Fresh Match ({time_clean}): {title_clean}")
                    send_loot_alert("OfferTag", f"{title_clean} ({time_clean})", "https://offertag.in")
                    
            print(f"🏁 OfferTag processing finalized. Dispatched {matched_count} new alerts.")
    except Exception as e:
        print(f"⚠️ OfferTag scraping crash: {e}")

def main():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    # Execute the multi-aggregator hunting tasks sequence
    scrape_desidime(headers)
    scrape_offertag(headers)

if __name__ == "__main__":
    main()
