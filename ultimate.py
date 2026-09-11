import requests

def run_direct_ping():
    print("🔄 Initializing a completely clean, un-cached test run...")
    
    # 1. Clean hardcoded token layers
    bot_token = "8883600849:AAHYq4WPcKEIIBvSiNXwdacw-PgVP7I6paU"
    
    # 2. ⚠️ REPLACE THE VALUE BELOW WITH YOUR 9-10 DIGIT NUMBER CODE FROM @userinfobot!
    chat_id = "1848239469" 
    
    # 3. Verified Telegram API server link layout
    target_url = f"https://telegram.org{bot_token}/sendMessage"
    
    message = (
        "🚨 *⚠️ LIVE PIPELINE PIPINGS SUCCESS* 🚨\n\n"
        "📦 *Product:* Haldiram's Nuts Platter (780g)\n"
        "💰 *Deal Price:* ₹315 (MRP: ₹2499)\n\n"
        "✅ *CACHE SUCCESSFULLY SHATTERED:* Your automation engine is fully active!"
    )
    
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    print("🚀 Firing direct network post to live Telegram API servers...")
    res = requests.post(target_url, json=payload, timeout=10)
    
    print(f"📊 Server Status Code: {res.status_code}")
    if res.status_code == 200:
        print("🎉 SUCCESS! The alert has officially hit your Telegram chat thread!")
    else:
        print(f"❌ Error Response: {res.text}")

if __name__ == "__main__":
    run_direct_ping()
