import os
import requests
import google.generativeai as genai
from flask import Flask, render_template_string, request

app = Flask(__name__)

# --- API SOZLAMALARI ---
# Render'dagi 'Environment' bo'limiga kiritgan kalitlaringizni o'qiydi
GEMINI_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyCl-dBQmgQTJWgA5LR0Fy5Wiq7HLxaHK2Y")
WAQI_TOKEN = os.getenv("WAQI_TOKEN", "68f561578e030386d0800b656708306059b02a46")

# Gemini 3 (yoki eng so'nggi barqaror versiya) sozlamasi
genai.configure(api_key=GEMINI_KEY)
ai_model = genai.GenerativeModel('gemini-1.5-flash') # Hozirgi eng tezkor va bepul model

@app.route('/')
def home():
    city = request.args.get('city', 'Tashkent')
    data = {"aqi": "--", "temp": "--", "hum": "--", "pm25": "--", "status": "Offline"}

    # 1. HAVO MA'LUMOTINI OLISH
    try:
        url = f"https://api.waqi.info/feed/{city}/?token={WAQI_TOKEN}"
        r = requests.get(url, timeout=10).json()
        if r['status'] == 'ok':
            res = r['data']
            data = {
                "aqi": res['aqi'],
                "temp": res['iaqi'].get('t', {}).get('v', 20),
                "hum": res['iaqi'].get('h', {}).get('v', 35),
                "pm25": res['iaqi'].get('pm25', {}).get('v', 10),
                "status": "Online"
            }
    except Exception as e:
        data["status"] = f"Error: {str(e)}"

    # 2. AI TAHLILI (Eng yangi prompt mantiqi)
    try:
        prompt = f"Havo ma'lumotlari: Shahar {city}, AQI {data['aqi']}, PM2.5 {data['pm25']}. Ushbu holatni professional ekolog sifatida qisqa tahlil qil."
        response = ai_model.generate_content(prompt)
        ai_msg = response.text.strip()
    except:
        ai_msg = "AI tahlili vaqtincha mavjud emas (API limit)."

    return render_template_string("""
    <!DOCTYPE html>
    <html lang="uz">
    <head>
        <meta charset="UTF-8">
        <title>Eco AI Pro Max</title>
        <style>
            body { background: #050505; color: #fff; font-family: 'Segoe UI', sans-serif; text-align: center; padding: 50px; }
            .card { background: linear-gradient(145deg, #111, #1a1a1a); padding: 40px; border-radius: 30px; 
                    border: 1px solid #00f2fe; box-shadow: 0 0 30px rgba(0,242,254,0.2); display: inline-block; width: 90%; max-width: 500px; }
            .aqi-val { font-size: 100px; color: #00f2fe; text-shadow: 0 0 20px rgba(0,242,254,0.5); }
            .grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px; margin-top: 30px; }
            .item { background: #222; padding: 15px; border-radius: 15px; font-size: 14px; }
            .ai-box { background: rgba(0,242,254,0.05); padding: 20px; border-radius: 20px; border-left: 5px solid #00f2fe; margin: 25px 0; text-align: left; }
        </style>
    </head>
    <body>
        <div class="card">
            <h2 style="margin:0; letter-spacing:5px;">{{ city.upper() }}</h2>
            <div class="aqi-val">{{ data.aqi }}</div>
            <p style="color: #666;">AQI INDEX</p>
            <div class="ai-box"><b>AI TAHLILI:</b><br><i>"{{ ai_msg }}"</i></div>
            <div class="grid">
                <div class="item">TEMP<br><b>{{ data.temp }}°C</b></div>
                <div class="item">NAMLYK<br><b>{{ data.hum }}%</b></div>
                <div class="item">PM2.5<br><b>{{ data.pm25 }}</b></div>
            </div>
        </div>
        <p style="color:#222; font-size:12px; margin-top:20px;">System: {{ data.status }}</p>
    </body>
    </html>
    """, data=data, ai_msg=ai_msg, city=city)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
