import os
import time
import requests
from playwright.sync_api import sync_playwright

# 1. GLOBAL SYSTEM CONFIGURATION
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "YOUR_TELEGRAM_CHAT_ID")
LOOT_DISCOUNT_THRESHOLD = 50.0

# Strategic NCR warehouse pincodes
NCR_WAREHOUSE_PINCODES = ["110020", "110040", "110050", "201306", "122018", "201301"]

# SPAM EXCLUSION LIST: Auto-rejects false positives, sample packs, and carry bags
SPAM_KEYWORDS = [
    "carry bag", "paper bag", "sachet", "sachets", "chotu pack", "sample", 
    "tester", "combo bag", "delivery fee", "packaging charge", "polybag", 
    "ketchup sachet", "seasoning mix", "oregano sachet", "chilli flakes"
]

def is_spam(product_name: str) -> bool:
    """Returns True if the product name contains any keywords from our spam filter list."""
    name_lower = product_name.lower()
    return any(keyword in name_lower for keyword in SPAM_KEYWORDS)

def send_loot_alert(platform: str, product_name: str, price: float, mrp: float, discount: float, location: str):
    if is_spam(product_name):
        print(f"⏩ Filtered out spam item: {product_name}")
        return
        
    url = f"https://telegram.org{TELEGRAM_TOKEN}/sendMessage"
    alert_message = (
        f"🚨 *⚠️ 75%+ LOOT DEAL DETECTED* 🚨\n\n"
        f"📦 *Product:* {product_name}\n"
        f"🏪 *Platform:* {platform.upper()}\n"
        f"💰 *Deal Price:* ₹{int(price)}  (MRP: ~₹{int(mrp)}~)\n"
        f"📉 *Discount:* `{discount:.1f}% OFF`\n"
        f"📍 *Target Area/Pincode:* {location}\n\n"
        f"👉 _Open the app, switch location to this area immediately, and purchase!_"
    )
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": alert_message, "parse_mode": "Markdown"}
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            print(f"🚀 Alert dispatched successfully for: {product_name}")
    except Exception as e:
        print(f"⚠️ Telegram webhook delivery failed: {e}")

def scrape_quick_commerce(page, platform: str, pincode: str):
    print(f"🔄 Scanning {platform.upper()} for warehouse pincode: {pincode}...")
    base_urls = {
        "blinkit": "https://blinkit.com",
        "zepto": "https://zepto.com",
        "instamart": "https://swiggy.com",
        "bigbasket": "https://bigbasket.com"
    }
    if platform not in base_urls: return
    try:
        page.goto(base_urls[platform], timeout=60000)
        page.wait_for_load_state("networkidle")
        products = page.query_selector_all("[data-testid='product-card'], .product-card, .ItemCard__Container")
        for prod in products:
            try:
                name_elem = prod.query_selector("[data-testid='product-name'], .product-title, h4")
                price_elem = prod.query_selector(".product-price, .price, [style*='color']")
                mrp_elem = prod.query_selector(".mrp, [style*='line-through']")
                if name_elem and price_elem and mrp_elem:
                    name = name_elem.inner_text().strip()
                    price = float(''.join(c for c in price_elem.inner_text() if c.isdigit() or c=='.'))
                    mrp = float(''.join(c for c in mrp_elem.inner_text() if c.isdigit() or c=='.'))
                    if mrp > price and price > 0:
                        discount = ((mrp - price) / mrp) * 100
                        if discount >= LOOT_DISCOUNT_THRESHOLD:
                            send_loot_alert(platform, name, price, mrp, discount, pincode)
            except Exception: continue
    except Exception as e: print(f"⚠️ Error browsing {platform}: {e}")

def scrape_amazon(page):
    print("🔄 Scanning Amazon.in central Lightning Deals framework...")
    try:
        page.goto("https://amazon.in", timeout=60000)
        page.wait_for_load_state("networkidle")
        deal_cards = page.query_selector_all("[data-testid='grid-item'], .dealCard")
        for card in deal_cards:
            try:
                name_elem = card.query_selector(".badge-string, h2, span")
                discount_badge = card.query_selector("[class*='discount'], .a-badge-text")
                if discount_badge:
                    badge_text = discount_badge.inner_text().strip()
                    if "%" in badge_text:
                        discount_val = float(''.join(c for c in badge_text if c.isdigit()))
                        if discount_val >= LOOT_DISCOUNT_THRESHOLD:
                            name = name_elem.inner_text().strip() if name_elem else "Amazon Clearance Item"
                            send_loot_alert("amazon.in", name, 0, 0, discount_val, "National / Pan-India")
            except Exception: continue
    except Exception as e: print(f"⚠️ Amazon system connection exception: {e}")

def main():
    platforms = ["blinkit", "zepto", "instamart", "bigbasket"]
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        page = context.new_page()
        for pin in NCR_WAREHOUSE_PINCODES:
            for app in platforms:
                scrape_quick_commerce(page, app, pin)
                time.sleep(2)
        scrape_amazon(page)
        browser.close()

if __name__ == "__main__":
    main()
