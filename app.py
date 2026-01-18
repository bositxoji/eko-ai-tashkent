import os
import requests
import google.generativeai as genai
from flask import Flask, render_template_string, request

app = Flask(__name__)

# --- KONFIGURATSIYA ---
# Siz bergan Google AI Studio API kaliti
GEMINI_API_KEY = "AIzaSyCl-dBQmgQTJWgA5LR0Fy5Wiq7HLxaHK2Y" 
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Havo ma'lumotlari uchun ishonchli token
WAQI_TOKEN = "68f561578e030386d0800b656708306059b02a46"

def get_ai_expert_advice(city, data, lang):
    """ Gemini AI orqali haqiqiy ekologik tahlil olish """
    # AI uchun kontekst yaratish
    prompt = f"""
    Sen Global Eco-AI aqlli tizimisan. 
    Ma'lumotlar: Shahar: {city}, AQI: {data['aqi']}, Harorat: {data['temp']}°C, Namlik: {data['hum']}%.
    Vazifang: Ushbu raqamlarni inson tushunadigan tilda tahlil qil va foydali maslahat ber. 
    Til: {lang}. Javobing juda qisqa (2-3 jumla), aqlli va do'stona bo'lsin.
    """
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return "AI tizimi hozircha ma'lumotlarni tahlil qila olmadi, lekin datchiklar ishlamoqda."

@app.route('/')
def home():
    city = request.args.get('city', 'tashkent')
    lang = request.args.get('lang', 'uz')
    
    try:
        # 1. Havo sifati ma'lumotlarini olish
        r = requests.get(f"https://api.waqi.info/feed/{city}/?token={WAQI_TOKEN}", timeout=7).json()
        if r['status'] == 'ok':
            res = r['data']
            data = {
                "aqi": res['aqi'],
                "temp": res['iaqi'].get('t', {}).get('v', "N/A"),
                "hum": res['iaqi'].get('h', {}).get('v', "N/A"),
                "pm25": res['iaqi'].get('pm25', {}).get('v', "N/A"),
                "city": city.upper()
            }
            # 2. Gemini AI tahlilini olish
            ai_comment = get_ai_expert_advice(city, data, lang)
        else:
            return "Xato: Bunday shahar topilmadi yoki API limiti tugadi."
    except Exception:
        return "Tizim ulanishida xatolik yuz berdi."

    # --- ULTRA MODERN UI (HTML/CSS) ---
    html_template = """
    <!DOCTYPE html>
    <html lang="{{ lang }}">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Eco-AI World Pro</title>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            :root { --primary: #00d2ff; --secondary: #3a7bd5; --dark: #0f172a; }
            body { 
                background: var(--dark); 
                color: #f8fafc; 
                font-family: 'Inter', system-ui, sans-serif; 
                margin: 0; 
                display: flex; 
                justify-content: center; 
                min-height: 100vh;
                background-image: radial-gradient(circle at top right, #1e293b, #0f172a);
            }
            .dashboard { width: 90%; max-width: 900px; padding: 40px 20px; }
            .nav { display: flex; justify-content: space-between; align-items: center; margin-bottom: 40px; }
            
            .ai-status { 
                background: rgba(0, 210, 255, 0.1); 
                border: 1px solid var(--primary); 
                padding: 6px 15px; 
                border-radius: 50px; 
                font-size: 12px; 
                color: var(--primary);
                font-weight: bold;
                text-transform: uppercase;
            }

            .main-card {
                background: rgba(30, 41, 59, 0.5);
                backdrop-filter: blur(20px);
                border: 1px solid rgba(255,255,255,0.1);
                border-radius: 32px;
                padding: 40px;
                box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5);
            }

            .city-name { font-size: 48px; font-weight: 800; margin: 0; letter-spacing: -1px; }
            .aqi-value { 
                font-size: 82px; 
                font-weight: 900; 
                background: linear-gradient(to right, #00d2ff, #94fbab);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin: 10px 0;
            }

            .stats-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-top: 30px; }
            .stat-item { background: rgba(255,255,255,0.03); padding: 20px; border-radius: 20px; text-align: center; }
            .stat-item i { color: var(--primary); margin-bottom: 10px; font-size: 20px; }
            .stat-label { display: block; font-size: 11px; text-transform: uppercase; opacity: 0.6; }
            .stat-val { font-size: 20px; font-weight: bold; }

            .ai-insight {
                margin-top: 30px;
                background: linear-gradient(135deg, rgba(58, 123, 213, 0.2), rgba(0, 210, 255, 0.1));
                border-left: 4px solid var(--primary);
                padding: 25px;
                border-radius: 0 20px 20px 0;
                position: relative;
            }
            .ai-insight i { position: absolute; top: -10px; left: -10px; background: var(--primary); color: #000; padding: 8px; border-radius: 50%; font-size:
