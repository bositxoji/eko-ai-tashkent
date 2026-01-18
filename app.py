import os
import requests
import certifi
import google.generativeai as genai
from flask import Flask, render_template_string, request

app = Flask(__name__)

# --- API SOZLAMALARI ---
# Render Environment Variables bo'limidan o'qiydi
GEMINI_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyCl-dBQmgQTJWgA5LR0Fy5Wiq7HLxaHK2Y")
WAQI_TOKEN = os.getenv("WAQI_TOKEN", "68f561578e030386d0800b656708306059b02a46")

# Gemini Modelini sozlash
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/')
def index():
    city = request.args.get('city', 'Tashkent')
    
    # Havo ma'lumotlarini olish (Xavfsiz SSL ulanishi bilan)
    aqi, temp, hum, pm25 = "--", "--", "--", "--"
    status = "Offline"
    
    try:
        url = f"https://api.waqi.info/feed/{city}/?token={WAQI_TOKEN}"
        r = requests.get(url, timeout=10, verify=certifi.where()).json()
        if r['status'] == 'ok':
            res = r['data']
            aqi = res['aqi']
            temp = res['iaqi'].get('t', {}).get('v', 22)
            hum = res['iaqi'].get('h', {}).get('v', 40)
            pm25 = res['iaqi'].get('pm25', {}).get('v', 15)
            status = "Online"
    except Exception as e:
        status = f"Error: {str(e)}"

    # AI Tahlili (Gemini 1.5 Flash orqali)
    ai_msg = "AI tizimi hozirda ma'lumotlarni qayta ishlamoqda..."
    try:
        prompt = f"Shahar: {city}, AQI: {aqi}, PM2.5: {pm25}. Havo holatini professional ekolog sifatida 1 ta qisqa o'zbekcha gapda tahlil qil."
        response = model.generate_content(prompt)
        ai_msg = response.text.strip()
    except:
        pass

    return render_template_string("""
    <!DOCTYPE html>
    <html lang="uz">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Neural Eco-Intelligence | {{ city }}</title>
        
        <meta name="description" content="Neural Eco-Intelligence - Real-time air quality monitoring with AI analysis.">
        <meta name="keywords" content="Eco, AI, Air Quality, Tashkent, Gemini, Ecology, Uzbekistan">
        
        <style>
            body { background: #050505; color: #fff; font-family: 'Segoe UI', sans-serif; text-align: center; padding: 50px 20px; margin: 0; }
            .card { background: linear-gradient(145deg, #111, #1a1a1a); padding: 40px; border-radius: 30px; 
                    border: 1px solid #00f2fe; box-shadow: 0 0 30px rgba(0,242,254,0.15); display: inline-block; width: 100%; max-width: 500px; }
            .city-name { font-size: 24px; letter-spacing: 5px; color: #00f2fe; margin: 0; }
            .aqi-val { font-size: 110px; font-weight: bold; color: #00f2fe; text-shadow: 0 0 20px rgba(0,242,254,0.4); margin: 10px 0; }
            .ai-box { background: rgba(0,242,254,0.05); padding: 20px; border-radius: 20px; border-left: 5px solid #00f2fe; margin: 25px 0; text-align: left; line-height: 1.6; }
            .grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px; }
            .item { background: #222; padding: 15px; border-radius: 15px; font-size: 14px; border: 1px solid #333; }
            .item b { font-size: 18px; color: #00f2fe; }
            small { color: #555; font-size: 10px; margin-top: 20px; display: block; }
        </style>
    </head>
    <body>
        <div class="card">
            <p class="city-name">{{ city.upper() }}</p>
            <div class="aqi-val">{{ aqi }}</div>
            <p style="color: #666; margin-top: -15px; letter-spacing: 2px;">AIR QUALITY INDEX</p>
            
            <div class="ai-box">
                <b style="color: #00f2fe; font-size: 12px; letter-spacing: 1px;">AI ECO-ADVISOR:</b><br>
                <i style="color: #ddd;">"{{ ai_msg }}"</i>
            </div>
            
            <div class="grid">
                <div class="item">TEMP<br><b>{{ temp }}°C</b></div>
                <div class="item">HUMIDITY<br><b>{{ hum }}%</b></div>
                <div class="item">PM2.5<br><b>{{ pm25 }}</b></div>
            </div>
        </div>
        <small>System Status: {{ status }} | Powered by Gemini 1.5 Flash</small>
    </body>
    </html>
    """, aqi=aqi, temp=temp, hum=hum, pm25=pm25, ai_msg=ai_msg, city=city, status=status)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
