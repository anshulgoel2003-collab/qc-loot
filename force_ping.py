import requests

def run_direct_ping():
    print("🔄 Initializing absolute clean payload...")
    
    # Clean hardcoded string layers
    bot_token = "8883600849:AAHYq4WPcKEIIBvSiNXwdacw-PgVP7I6paU"
    
    # ⚠️ REPLACE WITH YOUR 9 OR 10 DIGIT ID FROM @userinfobot (e.g., "584930219")
    chat_id = "1848239469" 
    
    target_url = f"https://telegram.org{bot_token}/sendMessage"
    
    message = (
        "🚨 *⚠️ LIVE ENGINE PIPELINE SUCCESS* 🚨\n\n"
        "📦 *Product:* Haldiram's Nuts Platter (780g)\n"
        "💰 *Deal Price:* ₹315 (MRP: ₹2499)\n\n"
        "✅ *CACHE BROKEN:* Your automation pipeline is 100% active!"
    )
    
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    print("🚀 Firing direct network post...")
    res = requests.post(target_url, json=payload, timeout=10)
    
    if res.status_code == 200:
        print("🎉 SUCCESS! The alert has officially hit your Telegram chat thread!")
    else:
        print(f"❌ Error Code: {res.status_code} - Check if you tapped 'Start' inside the bot chat window.")

if __name__ == "__main__":
    run_direct_ping()
