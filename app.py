import os
import requests
import certifi # SSL xavfsizlik uchun
import google.generativeai as genai
from flask import Flask, render_template_string, request
from dotenv import load_dotenv

load_dotenv() # .env yoki Render sozlamalarini yuklaydi
app = Flask(__name__)

# Kalitlarni olish
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
WAQI_TOKEN = os.getenv("WAQI_TOKEN")

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/')
def index():
    city = request.args.get('city', 'Tashkent')
    aqi, temp, hum = "--", "--", "--"
    
    try:
        # certifi.where() orqali xavfsiz ulanishni ta'minlaymiz
        url = f"https://api.waqi.info/feed/{city}/?token={WAQI_TOKEN}"
        r = requests.get(url, timeout=10, verify=certifi.where()).json()
        if r['status'] == 'ok':
            res = r['data']
            aqi = res['aqi']
            temp = res['iaqi'].get('t', {}).get('v', 22)
            hum = res['iaqi'].get('h', {}).get('v', 40)
    except Exception as e:
        print(f"Xatolik: {e}")

    # AI tahlili
    ai_msg = "Tahlil yuklanmoqda..."
    try:
        response = model.generate_content(f"Havo AQI {aqi}. 15 ta so'zda maslahat ber.")
        ai_msg = response.text.strip()
    except:
        pass

    return render_template_string("""
    <body style="background:#000; color:#00f2fe; text-align:center; padding:50px; font-family:sans-serif;">
        <h1>{{ city }} MONITOR</h1>
        <div style="font-size:100px;">{{ aqi }}</div>
        <p>Havo Sifati</p>
        <div style="border:1px solid #222; padding:20px; border-radius:15px;">{{ ai_msg }}</div>
    </body>
    """, city=city.upper(), aqi=aqi, ai_msg=ai_msg)
