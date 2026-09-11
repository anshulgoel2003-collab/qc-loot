import os
import time
import requests
from playwright.sync_api import sync_playwright

# 1. GLOBAL SYSTEM CONFIGURATION
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "YOUR_TELEGRAM_CHAT_ID")
LOOT_DISCOUNT_THRESHOLD = 20.0  # Set at 20.0 for instant diagnostic proof!

NCR_WAREHOUSE_PINCODES = ["110020", "110040", "110050", "201306", "122018"]

SPAM_KEYWORDS = [
    "carry bag", "paper bag", "sachet", "sachets", "chotu pack", "sample", 
    "tester", "combo bag", "delivery fee", "packaging charge", "polybag"
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

def inject_stealth_and_cookies(context, platform: str, pincode: str):
    """Bypasses automated environment signatures and forces micro-location injection."""
    page = context.new_page()
    
    # Execute structural JavaScript overrides to disable bot identification flags
    page.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        window.chrome = { runtime: {} };
        Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3]});
    """)
    
    # Pre-seed essential delivery routing tags to the local browser profile
    if platform == "blinkit":
        page.goto("https://blinkit.com/", timeout=40000)
        page.evaluate(f"localStorage.setItem('local_pincode', '{pincode}');")
    elif platform == "zepto":
        page.goto("https://www.zepto.com/", timeout=40000)
        page.evaluate(f"document.cookie = 'user_pincode={pincode}; path=/;';")
        
    return page

def scroll_to_load_all_products(page):
    try:
        for _ in range(6):
            page.evaluate("window.scrollBy(0, 1000)")
            time.sleep(1.5)
    except Exception:
        pass

def scrape_quick_commerce(context, platform: str, pincode: str):
    base_urls = {
        "blinkit": "https://blinkit.com",
        "zepto": "https://www.zepto.com/uncl/flash-sale/ed6ec473-d970-4881-a547-c39a2fff9745",
        "instamart": "https://swiggy.com",
        "bigbasket": "https://bigbasket.com"
    }
    if platform not in base_urls: return
    
    page = None
    try:
        page = inject_stealth_and_cookies(context, platform, pincode)
        page.goto(base_urls[platform], timeout=60000, wait_until="domcontentloaded")
        time.sleep(3) # Safe structural pause for framework components
        
        scroll_to_load_all_products(page)
        
        # Comprehensive fallback element targeting tree arrays
        products = page.query_selector_all(
            "[data-testid='product-card'], .product-card, [class*='ProductCard'], "
            ".ItemCard__Container, [class*='item-card'], a[href*='/pn/'], a[href*='/prn/']"
        )
        print(f"📊 {platform.upper()} ({pincode}): Uncovered {len(products)} live elements using generalized layouts.")
        
        for prod in products:
            try:
                name_elem = prod.query_selector("[data-testid='product-name'], .product-title, h4, h5, [class*='title'], [class*='name']")
                price_elem = prod.query_selector(".product-price, .price, [style*='color'], [class*='price']")
                mrp_elem = prod.query_selector(".mrp, [style*='line-through'], [class*='mrp'], strike")
                
                if name_elem and price_elem:
                    name = name_elem.inner_text().strip()
                    price = float(''.join(c for c in price_elem.inner_text() if c.isdigit() or c=='.'))
                    
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
        print(f"⚠️ {platform.upper()} parsing exception: {e}")
    finally:
        if page: page.close()

def main():
    platforms = ["blinkit", "zepto"] # Focus on main platforms for verification run
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800}
        )
        for pin in NCR_WAREHOUSE_PINCODES:
            for app in platforms:
                scrape_quick_commerce(context, app, pin)
                time.sleep(2)
        browser.close()

if __name__ == "__main__":
    main()
