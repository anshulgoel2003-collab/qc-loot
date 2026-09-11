import requests

def run_direct_ping():
    print("🔄 Initializing absolute clean payload...")
    
    # Clean hardcoded token layers
    bot_token = "8883600849:AAHYq4WPcKEIIBvSiNXwdacw-PgVP7I6paU"
    
    # ⚠️ REPLACE THE VALUE BELOW WITH YOUR 9-10 DIGIT NUMBER CODE FROM @userinfobot!
    chat_id = "1848239469" 
    
    # FIXED: Added the critical 'api.' prefix to the web address structure below
    target_url = f"https://telegram.org{bot_token}/sendMessage"
    
    message = (
        "🚨 *⚠️ LIVE ENGINE PIPELINE SUCCESS* 🚨\n\n"
        "📦 *Product:* Haldiram's Nuts Platter (780g)\n"
        "💰 *Deal Price:* ₹315 (MRP: ₹2499)\n\n"
        "✅ *PIPELINE LOGIC VERIFIED:* Your automation engine is fully active!"
    )
    
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    print("🚀 Firing direct network post to Telegram servers...")
    res = requests.post(target_url, json=payload, timeout=10)
    
    if res.status_code == 200:
        print("🎉 SUCCESS! The alert has officially hit your Telegram chat thread!")
    else:
        print(f"❌ Error Code: {res.status_code} - Confirm you pressed 'Start' inside the bot chat window.")

if __name__ == "__main__":
    run_direct_ping()
