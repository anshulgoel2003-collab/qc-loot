import os
import requests

# 1. DIRECT HARDCODED CREDENTIALS (Bypasses GitHub Settings Vault entirely!)
TELEGRAM_TOKEN = "8883600849:AAHYq4WPcKEIIBvSiNXwdacw-PgVP7I6paU"

# ⚠️ MANUALLY REPLACE THE VALUE BELOW WITH YOUR 9-10 DIGIT NUMBER CODE FROM @userinfobot!
TELEGRAM_CHAT_ID = "1848239469" 

def fire_local_diagnostic_alert():
    """Generates a self-contained test deal in local memory and pushes it directly to Telegram."""
    print("🔄 Initializing local diagnostic engine...")
    
    url = f"https://telegram.org{TELEGRAM_TOKEN}/sendMessage"
    
    # 2. LOCAL TEST PAYLOAD
    test_title = "Haldiram's Premium Nuts Platter Gift Pack (780g)"
    deal_price = 315
    mrp_value = 2499
    discount_pct = 87.4
    active_zone = "110040 (Okhla Warehouse)"
    
    alert_message = (
        f"🚨 *⚠️ SIMULATED 75%+ LOOT DEAL DETECTED* 🚨\n\n"
        f"📦 *Product:* {test_title}\n"
        f"🏪 *Platform:* BLINKIT SYSTEM TEST\n"
        f"💰 *Deal Price:* ₹{deal_price}  (MRP: ~₹{mrp_value}~)\n"
        f"📉 *Discount:* `{discount_pct}% OFF`\n"
        f"📍 *Target Warehouse:* {active_zone}\n\n"
        f"✅ *SUCCESS:* Your automated cloud-to-phone alert pipeline is 100% verified and active!"
    )
    
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": alert_message,
        "parse_mode": "Markdown"
    }
    
    try:
        print("🚀 Executing direct secure webhook transmission to your phone...")
        response = requests.post(url, json=payload, timeout=15)
        
        if response.status_code == 200:
            print(f"🎉 SUCCESS! Alert successfully pushed to chat thread!")
        else:
            print(f"❌ Telegram Error Code {response.status_code}!")
            print(f"👉 Please ensure you pressed the 'Start' button inside your chat with @loothidalo_bot on Telegram.")
    except Exception as e:
        print(f"⚠️ Transmission pipeline connection block: {e}")

if __name__ == "__main__":
    fire_local_diagnostic_alert()
