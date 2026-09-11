import os
import time
import requests
from playwright.sync_api import sync_playwright

# 1. SYSTEM GATEWAY SETTINGS
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "YOUR_TELEGRAM_CHAT_ID")
LOOT_DISCOUNT_THRESHOLD = 20.0  # Kept at 20.0 to guarantee you get test alerts right now!

NCR_WAREHOUSE_PINCODES = ["110020", "110040", "110050", "201306", "122018"]
SPAM_KEYWORDS = ["carry bag", "paper bag", "sachet", "polybag", "sample", "tester"]

def is_spam(name: str) -> bool:
    return any(w in name.lower() for w in SPAM_KEYWORDS)

def send_loot_alert(platform: str, name: str, price: float, mrp: float, discount: float, pin: str):
    if is_spam(name): return
    url = f"https://telegram.org{TELEGRAM_TOKEN}/sendMessage"
    msg = (
        f"🚨 *⚠️ LOOT DEAL DETECTED* 🚨\n\n"
        f"📦 *Product:* {name}\n"
        f"🏪 *Platform:* {platform.upper()}\n"
        f"💰 *Deal Price:* ₹{int(price)}  (MRP: ~₹{int(mrp)}~)\n"
        f"📉 *Discount:* `{discount:.1f}% OFF`\n"
        f"📍 *Pincode:* {pin}\n"
    )
    try: requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown"}, timeout=10)
    except: pass

def scrape_blinkit_via_search(context, pincode: str):
    """Bypasses deep category blocks by mimicking a real search engine user."""
    page = context.new_page()
    try:
        # Step 1: Open Homepage smoothly
        print(f"🏠 Opening Blinkit Homepage for pin {pincode}...")
        page.goto("https://blinkit.com/", timeout=60000, wait_until="networkidle")
        
        # Inject location criteria to local browser cache
        page.evaluate(f"localStorage.setItem('local_pincode', '{pincode}');")
        page.goto("https://blinkit.com/", timeout=40000, wait_until="domcontentloaded")
        
        # Step 2: Use the Search Box like a real human shopper
        search_box = page.query_selector("input[placeholder*='Search'], input[type='text']")
        if search_box:
            search_box.click()
            search_box.fill("gift pack")
            search_box.press("Enter")
            time.sleep(5)  # Let dynamic results load fully
            
            # Scroll down slightly to trigger images and discount elements
            page.evaluate("window.scrollBy(0, 1200)")
            time.sleep(2)
            
            # Step 3: Target absolute text layers rather than fragile CSS classes
            items = page.query_selector_all("a[href*='/prn/'], a[href*='/pn/'], [class*='ProductCard']")
            print(f"📊 BLINKIT ({pincode}): Successfully pulled {len(items)} products using search parameters.")
            
            for item in items:
                try:
                    text_content = item.inner_text().split("\n")
                    if len(text_content) >= 3:
                        name = text_content[0].strip()
                        
                        # Find price tracking structures within the card stack
                        prices = [float(''.join(c for c in t if c.isdigit())) for t in text_content if "₹" in t]
                        if len(prices) >= 2:
                            current_price, mrp = prices[0], prices[1]
                            if mrp > current_price and current_price > 0:
                                discount = ((mrp - current_price) / mrp) * 100
                                if discount >= LOOT_DISCOUNT_THRESHOLD:
                                    send_loot_alert("blinkit", name, current_price, mrp, discount, pincode)
                except: continue
    except Exception as e:
        print(f"⚠️ Search tracking exception: {e}")
    finally:
        page.close()

def main():
    print("🤖 Launching Invisible Search-Based Scraping Fleet...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={"width": 1440, "height": 900}
        )
        for pin in NCR_WAREHOUSE_PINCODES:
            scrape_blinkit_via_search(context, pin)
            time.sleep(3)
        browser.close()

if __name__ == "__main__":
    main()
