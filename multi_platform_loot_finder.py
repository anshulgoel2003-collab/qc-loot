import os
import re
import time
import requests
from playwright.sync_api import sync_playwright

# 1. SYSTEM GATEWAY SETTINGS
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "YOUR_TELEGRAM_CHAT_ID")
LOOT_DISCOUNT_THRESHOLD = 20.0  # Kept at 20.0 to guarantee immediate smartphone alert triggers!

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
    """Uses direct UI interactions to completely bypass dynamic element name shifts."""
    page = context.new_page()
    try:
        print(f"🏠 Loading Blinkit and configuring warehouse sector profile: {pincode}...")
        page.goto("https://blinkit.com/", timeout=40000, wait_until="domcontentloaded")
        
        # Inject target pincode directly to active storage profile cache
        page.evaluate(f"localStorage.setItem('local_pincode', '{pincode}');")
        page.goto("https://blinkit.com/", timeout=40000, wait_until="domcontentloaded")
        time.sleep(4)
        
        # --- BULLETPROOF SEARCH WORKAROUND ---
        # Instead of text selector queries, we force a physical mouse-click right in the middle 
        # of the upper search strip banner layout area to open the active dynamic typing node.
        print("🎯 Executing visual UI interaction on main search track layout...")
        page.mouse.click(600, 45) # Targets standard center-top coordinates of desktop search strips
        time.sleep(2)
        
        # Focus on the actively selected keyboard element and type the search criteria directly
        page.keyboard.type("gift pack")
        page.keyboard.press("Enter")
        print("🔍 Query pushed via keyboard array simulation. Loading shelf cards...")
        time.sleep(7)  
        
        # Force a lazy scroll down to trigger items to compile text streams
        page.evaluate("window.scrollBy(0, 1500)")
        time.sleep(3)
        
        # Target any interactive standard product links broadly to capture raw items
        items = page.query_selector_all("a[href*='/prn/'], a[href*='/pn/'], [class*='Card'], [href*='/p/']")
        print(f"📊 BLINKIT ({pincode}): Uncovered {len(items)} product elements.")
        
        for item in items:
            try:
                raw_text = item.inner_text().strip()
                if not raw_text or "₹" not in raw_text:
                    continue
                    
                lines = [line.strip() for line in raw_text.split("\n") if line.strip()]
                if not lines: continue
                product_name = lines[0] # Set the top textual line block as product identifier
                
                # Sanitize thousand-separator formatting out of string array values
                clean_text = raw_text.replace(",", "")
                found_prices = [float(num) for num in re.findall(r"₹\s*([\d.]+)", clean_text)]
                
                if len(found_prices) >= 2:
                    current_price = min(found_prices)
                    mrp = max(found_prices)
                    
                    if mrp > current_price and current_price > 0:
                        discount = ((mrp - current_price) / mrp) * 100
                        if discount >= LOOT_DISCOUNT_THRESHOLD:
                            print(f"✅ Hit Target: {product_name} ({discount:.1f}% OFF)")
                            send_loot_alert("blinkit", product_name, current_price, mrp, discount, pincode)
            except: 
                continue
    except Exception as e:
        print(f"⚠️ App automation tracking exception: {e}")
    finally:
        page.close()

def main():
    print("🤖 Launching Visual UI-Based Search Scraper Engine...")
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
