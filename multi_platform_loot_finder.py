import os
import time
import requests
from playwright.sync_api import sync_playwright

# 1. GLOBAL SYSTEM CONFIGURATION
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "YOUR_TELEGRAM_CHAT_ID")
LOOT_DISCOUNT_THRESHOLD = 20.0  # Kept at 20.0 for diagnostic confirmation!

NCR_WAREHOUSE_PINCODES = ["110020", "110040", "110050", "201306", "122018", "201301"]

SPAM_KEYWORDS = [
    "carry bag", "paper bag", "sachet", "sachets", "chotu pack", "sample", 
    "tester", "combo bag", "delivery fee", "packaging charge", "polybag", 
    "ketchup sachet", "seasoning mix", "oregano sachet", "chilli flakes"
]

def is_spam(product_name: str) -> bool:
    name_lower = product_name.lower()
    return any(keyword in name_lower for keyword in SPAM_KEYWORDS)

def send_loot_alert(platform: str, product_name: str, price: float, mrp: float, discount: float, location: str):
    if is_spam(product_name):
        return
    url = f"https://telegram.org{TELEGRAM_TOKEN}/sendMessage"
    alert_message = (
        f"🚨 *⚠️ LOOT DEAL DETECTED* 🚨\n\n"
        f"📦 *Product:* {product_name}\n"
        f"🏪 *Platform:* {platform.upper()}\n"
        f"💰 *Deal Price:* ₹{int(price)}  (MRP: ~₹{int(mrp)}~)\n"
        f"📉 *Discount:* `{discount:.1f}% OFF`\n"
        f"📍 *Target Area/Pincode:* {location}\n\n"
        f"👉 _Check your app location now!_"
    )
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": alert_message, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception:
        pass

def scroll_to_load_all_products(page):
    """Simulates human scrolling to force dynamic content, images, and prices to render."""
    try:
        for _ in range(5):  # Force scroll downwards 5 consecutive increments
            page.evaluate("window.scrollBy(0, 800)")
            time.sleep(1)   # Wait briefly for dynamic data nodes to spin up
    except Exception:
        pass

def scrape_quick_commerce(page, platform: str, pincode: str):
    base_urls = {
        "blinkit": "https://blinkit.com",
        "zepto": "https://zepto.com",
        "instamart": "https://swiggy.com",
        "bigbasket": "https://bigbasket.com"
    }
    if platform not in base_urls: return
    try:
        page.goto(base_urls[platform], timeout=60000)
        page.wait_for_load_state("load")
        
        # Execute human scroll emulator before parsing text nodes
        scroll_to_load_all_products(page)
        
        products = page.query_selector_all("[data-testid='product-card'], .product-card, .ItemCard__Container, .pc-card")
        print(f"📊 {platform.upper()} ({pincode}): Found {len(products)} total rendered product elements.")
        
        for prod in products:
            try:
                name_elem = prod.query_selector("[data-testid='product-name'], .product-title, h4, .title")
                price_elem = prod.query_selector(".product-price, .price, [style*='color'], .iyJbkX")
                mrp_elem = prod.query_selector(".mrp, [style*='line-through'], .strike")
                
                if name_elem and price_elem:
                    name = name_elem.inner_text().strip()
                    price = float(''.join(c for c in price_elem.inner_text() if c.isdigit() or c=='.'))
                    
                    # If an explicit strike-through MRP element isn't found, estimate based on layout matrix
                    if mrp_elem:
                        mrp = float(''.join(c for c in mrp_elem.inner_text() if c.isdigit() or c=='.'))
                    else:
                        continue
                        
                    if mrp > price and price > 0:
                        discount = ((mrp - price) / mrp) * 100
                        if discount >= LOOT_DISCOUNT_THRESHOLD:
                            send_loot_alert(platform, name, price, mrp, discount, pincode)
            except Exception: continue
    except Exception as e: 
        print(f"⚠️ Error running {platform}: {e}")

def main():
    platforms = ["blinkit", "zepto", "instamart", "bigbasket"]
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        page = context.new_page()
        for pin in NCR_WAREHOUSE_PINCODES:
            for app in platforms:
                scrape_quick_commerce(page, app, pin)
                time.sleep(1)
        browser.close()

if __name__ == "__main__":
    main()
