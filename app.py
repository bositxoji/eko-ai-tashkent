import os
import requests
import google.generativeai as genai
from flask import Flask, render_template_string, request

app = Flask(__name__)

# RENDER'DAGI KALITLARNI O'QISH
# Agar kalitlar topilmasa, xato bermasligi uchun default qiymat berilgan
GEMINI_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyCl-dBQmgQTJWgA5LR0Fy5Wiq7HLxaHK2Y")
WAQI_TOKEN = os.getenv("WAQI_TOKEN", "68f561578e030386d0800b656708306059b02a46")

genai.configure(api_key=GEMINI_KEY)
ai_model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/')
def home():
    city = request.args.get('city', 'Tashkent')
    data = {"aqi": "--", "temp": "--", "hum": "--", "pm25": "--"}

    try:
        # Havo ma'lumotlarini olish
        url = f"https://api.waqi.info/feed/{city}/?token={WAQI_TOKEN}"
        r = requests.get(url, timeout=5).json()
        if r['status'] == 'ok':
            res = r['data']
            data = {
                "aqi": res['aqi'],
                "temp": res['iaqi'].get('t', {}).get('v', 22),
                "hum": res['iaqi'].get('h', {}).get('v', 45),
                "pm25": res['iaqi'].get('pm25', {}).get('v', 15)
            }
    except:
        pass

    # AI Tahlili
    try:
        prompt = f"Shahar: {city}, AQI: {data['aqi']}. Havo holatini 1 ta qisqa jumlada tahlil qil."
        response = ai_model.generate_content(prompt)
        ai_msg = response.text.strip()
    except:
        ai_msg = "AI tahlili yuklanmoqda..."

    return render_template_string("""
    <body style="background:#000; color:#00f2fe; text-align:center; font-family:sans-serif; padding-top:100px;">
        <h1>{{ city.upper() }} MONITOR</h1>
        <div style="font-size:80px;">{{ data.aqi }}</div>
        <p>Havo Sifati Indeksi</p>
        <div style="background:#111; padding:20px; border-radius:15px; display:inline-block; margin:20px;">
            <i>"{{ ai_msg }}"</i>
        </div>
        <br>
        <div style="display:flex; justify-content:center; gap:20px;">
            <div>TEMP: {{ data.temp }}°C</div>
            <div>HUM: {{ data.hum }}%</div>
        </div>
    </body>
    """, data=data, ai_msg=ai_msg, city=city)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
