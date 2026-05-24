import telebot
import requests
import time
import threading

# BotFather ဆီကရတဲ့ ကိုကြီးရဲ့ Telegram Bot Token ကို ဒီမှာ ထည့်ပါ
BOT_TOKEN = '8454842342:AAEEm7ZTiIOKmas0qvMB_ev3fFJoHLp2rKw'

# Colab က ခုနတင်ထွက်လာတဲ့ Ngrok လင့်ခ်
OLLAMA_URL = 'https://uncognized-pleasingly-emil.ngrok-free.dev/api/generate'

bot = telebot.TeleBot(BOT_TOKEN)

# ----------------------------------------------------
# 🔄 Render Bot အိပ်မပျော်အောင် ကိုယ့်ကိုယ်ကိုယ် ပြန်နှိုးမယ့်စနစ် (Self-Ping)
# ----------------------------------------------------
def keep_alive():
    # Render က Deploy ပြီးရင် ပေးမယ့် URL လင့်ခ် (ဥပမာ - https://my-bot.onrender.com)
    # လောလောဆယ် Render လင့်ခ်မရသေးခင် localhost နဲ့ စမ်းထားပါမယ်
    RENDER_APP_URL = "http://localhost:8080" 
    
    while True:
        try:
            # Render Server မအိပ်ပျော်သွားအောင် ၁၅ စက္ကန့်တစ်ခါ Request လှမ်းပို့နေမှာပါ
            requests.get(RENDER_APP_URL, timeout=5)
            print("Pinging Render Server to stay awake...")
        except Exception:
            # Render မှာ Web Service ဖြစ်လို့ ပထမပိုင်း ပို့မရလည်း အကြောင်းမဟုတ်ပါဘူး၊ ဆက်ပို့နေမှာပါ
            pass
        time.sleep(15) # ၁၅ စက္ကန့်တစ်ခါ နှိုးစက်ပေးခြင်း

# Background မှာ အလုပ်လုပ်ဖို့ Thread တစ်ခု သီးသန့်မောင်းထားမယ်
ping_thread = threading.Thread(target=keep_alive, daemon=True)
ping_thread.start()
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

if __name__ == '__main__':
    print("Bot စတင်လည်ပတ်နေပါပြီ...")
    bot.infinity_polling()
    