import os
import requests
import google.generativeai as genai
from flask import Flask, render_template_string, request

app = Flask(__name__)

# --- API KALITLARINI TIZIMDAN OLISH ---
# Bu qism Render-ga kiritgan kalitlaringizni o'qiydi
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
WAQI_TOKEN = os.getenv("WAQI_TOKEN")

# Agar tizimda kalit topilmasa, zahira kalitlarni ishlatadi
if not GEMINI_KEY:
    GEMINI_KEY = "AIzaSyCl-dBQmgQTJWgA5LR0Fy5Wiq7HLxaHK2Y"
if not WAQI_TOKEN:
    WAQI_TOKEN = "68f561578e030386d0800b656708306059b02a46"

genai.configure(api_key=GEMINI_KEY)
ai_model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/')
def home():
    city = request.args.get('city', 'Tashkent')
    
    # 1. HAVO MA'LUMOTINI OLISH
    data = {"aqi": "--", "temp": "--", "hum": "--", "pm25": "--", "status": "Connecting..."}
    try:
        url = f"https://api.waqi.info/feed/{city}/?token={WAQI_TOKEN}"
        r = requests.get(url, timeout=10).json()
        if r['status'] == 'ok':
            res = r['data']
            data = {
                "aqi": res['aqi'],
                "temp": res['iaqi'].get('t', {}).get('v', '--'),
                "hum": res['iaqi'].get('h', {}).get('v', '--'),
                "pm25": res['iaqi'].get('pm25', {}).get('v', '--'),
                "status": "Online"
            }
    except Exception as e:
        data["status"] = f"Error: {str(e)}"

    # 2. AI TAHLILI
    try:
        prompt = f"Shahar: {city}. Havo sifati (AQI): {data['aqi']}. PM2.5 miqdori: {data['pm25']}. Ushbu holatni o'zbek tilida juda qisqa (1 ta gapda) tahlil qiling."
        response = ai_model.generate_content(prompt)
        ai_msg = response.text.strip()
    except:
        ai_msg = "AI hozirda ma'lumotni tahlil qila olmayapti."

    return render_template_string("""
    <!DOCTYPE html>
    <html style="background:#000; color:#fff; font-family:sans-serif;">
    <head>
        <title>Eco AI Pro</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
    </head>
    <body style="text-align:center; padding:20px; display:flex; flex-direction:column; align-items:center; justify-content:center; min-height:100vh;">
        <h1 style="color:#00f2fe; letter-spacing:2px;">{{ city.upper() }} - NEURAL MONITOR</h1>
        <div style="background:#111; padding:40px; border-radius:30px; border:2px solid #222; box-shadow: 0 0 20px rgba(0,242,254,0.1); width:90%; max-width:500px;">
            <div style="font-size:100px; font-weight:bold; color:#00f2fe; margin:0;">{{ data.aqi }}</div>
            <p style="letter-spacing:3px; color:#aaa; margin-bottom:30px;">HAVO SIFATI INDEXI</p>
            <div style="background:#1a1a1a; padding:20px; border-radius:15px; margin-bottom:30px; border-left:4px solid #00f2fe;">
                <p style="font-style:italic; color:#fff; font-size:16px; margin:0;">"{{ ai_msg }}"</p>
            </div>
            <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:15px;">
                <div style="background:#222; padding:15px; border-radius:15px;"><small style="color:#666;">TEMP</small><br><b style="font-size:18px;">{{ data.temp }}°C</b></div>
                <div style="background:#222; padding:15px; border-radius:15px;"><small style="color:#666;">NAMLYK</small><br><b style="font-size:18px;">{{ data.hum }}%</b></div>
                <div style="background:#222; padding:15px; border-radius:15px;"><small style="color:#666;">PM2.5</small><br><b style="font-size:18px;">{{ data.pm25 }}</b></div>
            </div>
        </div>
        <p style="margin-top:25px; font-size:12px; color:#333;">System Status: {{ data.status }} | Engine: Gemini 1.5</p>
    </body>
    </html>
    """, data=data, ai_msg=ai_msg, city=city)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
