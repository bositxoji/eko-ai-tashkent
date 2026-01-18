import os
import requests
import time
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# UNIVERSAL AI LOGIC - HAR QANDAY SAVOLGA JAVOB BERADI
def get_ai_response(prompt, lang):
    api_key = "AIzaSyCl-dBQmgQTJWgA5LR0Fy5Wiq7HLxaHK2Y"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [{"text": f"Sen juda aqlli universal yordamchisan. Foydalanuvchi savoliga {lang} tilida mukammal va ilmiy javob ber. Savol: {prompt}"}]
        }]
    }
    
    for _ in range(3): 
        try:
            response = requests.post(url, json=payload, timeout=30)
            data = response.json()
            if 'candidates' in data:
                return data['candidates'][0]['content']['parts'][0]['text']
            elif 'error' in data and data['error']['code'] == 429:
                time.sleep(2)
                continue
        except:
            time.sleep(1)
            continue
    return "Xatolik: AI bilan aloqa o'rnatib bo'lmadi. Iltimos, birozdan so'ng urinib ko'ring."

@app.route('/')
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="uz">
    <head>
        <meta charset="UTF-8">
        <title>ECO-AI-WORLD | A.A Ataxojayev</title>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            :root { --neon: #00f2fe; --bg: #010101; --glass: rgba(255,255,255,0.03); }
            body { background: var(--bg); color: #fff; font-family: 'Inter', sans-serif; margin: 0; }
            nav { display: flex; justify-content: space-between; align-items: center; padding: 10px 40px; background: #000; border-bottom: 2px solid var(--neon); position: sticky; top: 0; z-index: 1000; }
            .header-info { display: flex; align-items: center; gap: 30px; }
            .authors { border-left: 2px solid var(--neon); padding-left: 20px; font-size: 12px; color: #aaa; }
            .authors b { color: var(--neon); font-size: 14px; text-transform: uppercase; }
            .container { max-width: 1300px; margin: auto; padding: 25px; }
            .glass { background: var(--glass); backdrop-filter: blur(15px); border: 1px solid rgba(0,242,254,0.15); border-radius: 20px; padding: 25px; margin-bottom: 30px; }
            h2 { color: var(--neon); text-transform: uppercase; letter-spacing: 2px; border-bottom: 1px solid #222; padding-bottom: 10px; margin-bottom: 20px; font-size: 18px; }
            .city-scroll { display: flex; overflow-x: auto; gap: 15px; padding-bottom: 15px; margin-bottom: 20px; }
            .city-card { min-width: 150px; background: #0a0a0a; border: 1px solid #333; padding: 15px; border-radius: 12px; text-align: center; }
            .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 25px; }
            .lib-link { display: block; color: #ddd; text-decoration: none; padding: 12px; border: 1px solid #222; border-radius: 8px; margin-bottom: 10px; transition: 0.3s; }
            .lib-link:hover { border-color: var(--neon); background: rgba(0,242,254,0.05); }
            #ai-display { min-height: 300px; background: rgba(0,0,0,0.7); border: 1px solid #333; border-radius: 15px; padding: 25px; line-height: 1.8; overflow-y: auto; white-space: pre-wrap; }
            textarea { width: 100%; background: #111; border: 1px solid #444; color: #fff; padding: 15px; border-radius: 12px; margin-top: 15px; box-sizing: border-box; font-size: 16px; outline: none; }
            .btn { background: var(--neon); color: #000; border: none; padding: 12px 25px; border-radius: 8px; font-weight: bold; cursor: pointer; transition: 0.3s; }
            .map-box { height: 450px; border-radius: 20px; overflow: hidden; border: 1px solid var(--neon); margin-bottom: 30px; }
            .lang-btn { background: none; border: 1px solid var(--neon); color: var(--neon); padding: 5px 12px; border-radius: 6px; cursor: pointer; margin-left: 5px; }
            .lang-btn.active { background: var(--neon); color: #000; }
        </style>
    </head>
    <body>
        <nav>
            <div style="font-weight: bold; font-size: 22px;">ECO-AI-WORLD</div>
            <div class="header-info">
                <div class="authors">Muallif: <b>A.A Ataxojayev</b><br>Ilmiy rahbar: <b>E.A Egamberdiev</b></div>
                <div>
                    <button class="lang-btn active" onclick="setLang('uz', this)">UZ</button>
                    <button class="lang-btn" onclick="setLang('ru', this)">RU</button>
                    <button class="lang-btn" onclick="setLang('en', this)">EN</button>
                </div>
            </div>
        </nav>

        <div class="container">
            <h2>🏙️ Shaharlar Monitoringi</h2>
            <div class="city-scroll" id="city-list"></div>

            <div class="map-box">
                <iframe src="
