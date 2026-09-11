import os
import re
import time
import requests
from playwright.sync_api import sync_playwright

# 1. SYSTEM GATEWAY SETTINGS
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "YOUR_TELEGRAM_CHAT_ID")
LOOT_DISCOUNT_THRESHOLD = 20.0  # Kept at 20.0 to guarantee immediate push notifications!

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
    try: 
        requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown"}, timeout=10)
    except: 
        pass

def scrape_blinkit_via_search(context, pincode: str):
    """Bypasses web walls by mimicking search routing and applying loose text extraction regex."""
    page = context.new_page()
    try:
        print(f"🏠 Loading Blinkit and configuring warehouse sector profile: {pincode}...")
        page.goto("https://blinkit.com", timeout=60000, wait_until="commit")
        
        # Inject target pincode directly to active storage
        page.evaluate(f"localStorage.setItem('local_pincode', '{pincode}');")
        page.goto("https://blinkit.com", timeout=40000, wait_until="domcontentloaded")
        time.sleep(2)
        
        # Interact with the search field framework
        search_box = page.query_selector("input[placeholder*='Search'], input[type='text']")
        if search_box:
            search_box.click()
            search_box.fill("gift pack")
            search_box.press("Enter")
            time.sleep(5)  # Safe structural pause for dynamic shelf content to load
            
            # Scroll downwards to expand hidden grid elements
            page.evaluate("window.scrollBy(0, 1000)")
            time.sleep(2)
            
            # Target broad anchored product links
            items = page.query_selector_all("a[href*='/prn/'], a[href*='/pn/'], [class*='ProductCard']")
            print(f"📊 BLINKIT ({pincode}): Detected {len(items)} raw interactive element blocks.")
            
            for item in items:
                try:
                    raw_text = item.inner_text().strip()
                    if not raw_text or "₹" not in raw_text:
                        continue
                        
                    lines = [line.strip() for line in raw_text.split("\n") if line.strip()]
                    product_name = lines[0] # Grab the very first line as the identifier string
                    
                    # Regex logic: Pull out all numbers that come directly after a Rupee symbol
                    found_prices = [float(num) for num in re.findall(r"₹\s*([\d,]+)", raw_text)]
                    
                    if len(found_prices) >= 2:
                        # Sort array data: the smaller value is always the sale price, the larger is the MRP
                        current_price = min(found_prices)
                        mrp = max(found_prices)
                        
                        if mrp > current_price and current_price > 0:
                            discount = ((mrp - current_price) / mrp) * 100
                            if discount >= LOOT_DISCOUNT_THRESHOLD:
                                print(f"✅ Matched Condition: {product_name} ({discount:.1f}% OFF)")
                                send_loot_alert("blinkit", product_name, current_price, mrp, discount, pincode)
                except: 
                    continue
    except Exception as e:
        print(f"⚠️ App automation tracking exception: {e}")
    finally:
        page.close()

def main():
    print("🤖 Launching Regex-Based Search Scraper Engine...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={"width": 1440, "height": 900}
        )
        for pin in NCR_WAREHOUSE_PINCODES:
            scrape_blinkit_via_search(context, pin)
            time.sleep(2)
        browser.close()

if __name__ == "__main__":
    main()
