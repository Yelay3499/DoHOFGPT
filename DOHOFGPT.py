import telebot
import requests
import time
import threading
from flask import Flask

# ၁။ ကိုကြီးရဲ့ Bot Token နှင့် Ngrok လင့်ခ်
BOT_TOKEN = '8454842342:AAEEm7ZTiIOKmas0qvMB_ev3fFJoHLp2rKw'
OLLAMA_URL = 'https://uncognized-pleasingly-emil.ngrok-free.dev/api/generate'

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "DOH Gpt Server is Running and Healthy!", 200

# ----------------------------------------------------
# 🔄 Render Bot အိပ်မပျော်အောင် ကိုယ့်ကိုယ်ကိုယ် ပြန်နှိုးမယ့်စနစ် (လင့်ခ်အစစ် ထည့်ပေးထားပါပြီ)
# ----------------------------------------------------
def keep_alive():
    # ကိုကြီး ရလာတဲ့ Render လင့်ခ်အစစ်ကို ဒီမှာ လာထည့်ပေးလိုက်တာပါဗျာ
    RENDER_APP_URL = "https://dohofgpt.onrender.com"
    
    while True:
        try:
            # အပြင်ကနေ Render Server ဆီ ၁၅ စက္ကန့်တစ်ခါ လှမ်းဆော်ပြီး နှိုးထားမှာပါ
            requests.get(RENDER_APP_URL, timeout=5)
            print("Pinging Render Server to stay awake...")
        except Exception:
            pass
        time.sleep(15) 

# ----------------------------------------------------
# 💬 Telegram AI Bot ရဲ့ လုပ်ဆောင်ချက်အပိုင်း (ကိုကြီးရဲ့စာသားများအတိုင်း)
# ----------------------------------------------------
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hi user Welcome to DOH Gpt can you ask me မင်းချင်တာမေး ဆိုပေမဲ့အချစ်အကြောင်းတော့လာမမေးပါနဲ့🫩🖕။")

@bot.message_handler(func=lambda message: True)
def chat_with_ai(message):
    bot.send_chat_action(message.chat.id, 'typing')
    
    payload = {
        "model": "dolphin-mistral",
        "prompt": message.text,
        "stream": False
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        ai_response = response.json().get('response', 'Error: အဖြေမထွက်လာပါဘူး။')
        bot.reply_to(message, ai_response)
    except Exception as e:
        bot.reply_to(message, f"ချိတ်ဆက်မှု အဆင်မပြေပါဘူး မင်းနဲ့သူမရဲ့ဆက်ဆံရေးလိုပေါ့: {e}")

def run_bot():
    bot.infinity_polling()

if __name__ == '__main__':
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    ping_thread = threading.Thread(target=keep_alive, daemon=True)
    ping_thread.start()
    
    print("Bot စတင်လည်ပတ်နေပါပြီ...")
    app.run(host='0.0.0.0', port=8080)
    
