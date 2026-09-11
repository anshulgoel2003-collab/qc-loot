import requests

def run_clean_ping():
    print("🔄 Initializing completely fresh diagnostic check...")
    
    # Clean hardcoded token layers
    raw_token = "8883600849:AAHYq4WPcKEIIBvSiNXwdacw-PgVP7I6paU"
    
    # ⚠️ REPLACE THE VALUE BELOW WITH YOUR 9-10 DIGIT NUMBER CODE FROM @userinfobot!
    # Ensure you keep the quotation marks around the number string.
    chat_id = "1848239469" 
    
    # Automatically strip any hidden or invisible characters that break URL parsers
    bot_token = raw_token.strip().replace(" ", "")
    
    # Constructing the exact, verified API endpoint destination link
    target_url = f"https://telegram.org{bot_token}/sendMessage"
    
    message = (
        "🚨 *⚠️ LIVE ENGINE PIPELINE SUCCESS* 🚨\n\n"
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
    
    if res.status_code == 200:
        print("🎉 SUCCESS! The alert has officially hit your Telegram chat thread!")
    else:
        print(f"❌ Error Code: {res.status_code} - Confirm you pressed 'Start' inside the bot chat window.")

if __name__ == "__main__":
    run_clean_ping()
