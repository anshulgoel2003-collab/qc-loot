import http.client
import json

def run_direct_ping():
    print("🔄 Initializing completely fresh diagnostic check...")
    
    # 1. Clean hardcoded credentials
    bot_token = "8883600849:AAHYq4WPcKEIIBvSiNXwdacw-PgVP7I6paU"
    
    # ⚠️ REPLACE THE VALUE BELOW WITH YOUR 9-10 DIGIT NUMBER CODE FROM @userinfobot!
    chat_id = "1848239469" 
    
    # 2. Set up the payload text
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
    
    # 3. Use standard lower-level network sockets to bypass all internal url parser typos
    print("🚀 Firing connection handshake to api.telegram.org...")
    connection = http.client.HTTPSConnection("api.telegram.org")
    headers = {"Content-type": "application/json"}
    
    try:
        connection.request("POST", f"/bot{bot_token}/sendMessage", json.dumps(payload), headers)
        response = connection.getresponse()
        response_data = response.read().decode()
        
        print(f"📊 Server Response Code: {response.status}")
        if response.status == 200:
            print("🎉 SUCCESS! The alert has officially hit your Telegram chat thread!")
        else:
            print(f"❌ Error Detail: {response_data}")
            print("👉 Check if you pressed 'Start' inside your chat with @loothidalo_bot on Telegram.")
    except Exception as e:
        print(f"⚠️ Network transmission failed: {e}")
    finally:
        connection.close()

if __name__ == "__main__":
    run_direct_ping()
