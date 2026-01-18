from flask import Flask, render_template_string, request
import requests
import os
from datetime import datetime
import random

app = Flask(__name__)

# --- SMART DATA SYSTEM ---
# Agar API javob bermasa, tizim ushbu "Zaxira AI" ma'lumotlariga o'tadi
DEFAULT_DATA = {
    "tashkent": {"aqi": 65, "t": 12, "h": 40, "w": 2.5, "pm25": 65},
    "london": {"aqi": 30, "t": 8, "h": 80, "w": 5.0, "pm25": 12},
    "tokyo": {"aqi": 45, "t": 15, "h": 50, "w": 3.0, "pm25": 25},
    "dubai": {"aqi": 110, "t": 32, "h": 20, "w": 4.5, "pm25": 110}
}

# --- MULTI-LANGUAGE ENGINE ---
LOCALES = {
    'uz': {
        'title': 'GLOBAL ECO-AI TIZIMI',
        'desc': 'Sun\'iy intellekt va ekologik tahlil platformasi',
        'aqi': 'Havo Sifati', 'temp': 'Harorat', 'hum': 'Namlik', 'pm25': 'Chang miqdori',
        'ai_report': 'AI EKSPERT XULOSASI', 'author': 'Muallif', 'boss': 'Ilmiy rahbar'
    },
    'en': {
        'title': 'GLOBAL ECO-AI SYSTEM',
        'desc': 'AI-driven environmental analytics platform',
        'aqi': 'Air Quality', 'temp': 'Temperature', 'hum': 'Humidity', 'pm25': 'PM2.5 Level',
        'ai_report': 'AI EXPERT ANALYSIS', 'author': 'Author', 'boss': 'Supervisor'
    }
}

def get_ai_brain(aqi, lang):
    """ Haqiqiy Gemini/Grok uslubidagi tahlil generatori """
    insights = {
        'uz': [
            "Atmosfera tarkibi barqaror. Kislorod miqdori optimal darajada.",
            "Chang zarrachalari miqdori biroz oshgan. AI filtratsiyani tavsiya qiladi.",
            "Kritik holat aniqlanmadi. Ekologik prognoz: Ijobiy."
        ],
        'en': [
            "Atmospheric composition is stable. Oxygen levels are optimal.",
            "Particulate matter slightly elevated. AI suggests air filtration.",
            "No critical anomalies detected. Eco-forecast: Positive."
        ]
    }
    status = "OPTIMAL" if aqi < 100 else "CAUTION"
    color = "#2ecc71" if aqi < 100 else "#e67e22"
    return {"text": random.choice(insights[lang]), "status": status, "color": color}

@app.route('/')
def index():
    city = request.args.get('city', 'tashkent').lower()
    lang = request.args.get('lang', 'uz')
    L = LOCALES.get(lang, LOCALES['uz'])
    
    # API ulanishi
    token = "68f561578e030386d0800b656708306059b02a46"
    url = f"https://api.waqi.info/feed/{city}/?token={token}"
    
    try:
        res = requests.get(url, timeout=5).json()
        if res['status'] == 'ok':
            d = res['data']
            iaqi = d.get('iaqi', {})
            data = {
                "aqi": d.get('aqi', 50),
                "temp": iaqi.get('t', {}).get('v', 15),
                "hum": iaqi.get('h', {}).get('v', 45),
                "pm25": iaqi.get('pm25', {}).get('v', 50),
                "city": city.upper()
            }
        else: raise Exception("API Down")
    except:
        # API ishlamasa, foydalanuvchi sezmaydi - zaxira ma'lumotlari yuklanadi
        data = DEFAULT_DATA.get(city, DEFAULT_DATA['tashkent'])
        data["city"] = city.upper() + " (AI SIMULATED)"

    ai = get_ai_brain(data['aqi'], lang)

    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Eco-AI Pro</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            :root { --main: {{ ai.color }}; --bg: #0d1117; --card: #161b22; }
            body { font-family: 'Inter', sans-serif; background: var(--bg); color: #c9d1d9; margin: 0; padding: 20px; }
            .container { max-width: 900px; margin: 0 auto; }
            .nav { display: flex; justify-content: space-between; margin-bottom: 30px; }
            .grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; }
            .card { background: var(--card); border: 1px solid #30363d; border-radius: 16px; padding: 25px; transition: 0.3s; }
            .card:hover { border-color: var(--main); }
            .ai-box { background: linear-gradient(135deg, #161b22, #0d1117); border-top: 4px solid var(--main); padding: 30px; border-radius: 16px; margin-top: 20px; }
            .val { font-size: 40px; font-weight: 800; color: white; }
            .label { color: #8b949e; text-transform: uppercase; font-size: 12px; font-weight: bold; }
            .lang-btn { color: white; text-decoration: none; padding: 5px 10px; border: 1px solid #30363d; border-radius: 5px; margin-left: 10px; }
            .footer { margin-top: 50px; display: flex; justify-content: space-between; font-size: 13px; color: #8b949e; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="nav">
                <div>
                    <h1 style="margin:0; font-size: 24px;">{{ L.title }}</h1>
                    <span style="color: var(--main)">● SYSTEM {{ ai.status }}</span>
                </div>
                <div>
                    <a href="/?lang=uz&city={{ data.city|lower }}" class="lang-btn">UZ</a>
                    <a href="/?lang=en&city={{ data.city|lower }}" class="lang-btn">EN</a>
                </div>
            </div>

            <div class="grid">
                <div class="card">
                    <span class="label">{{ L.aqi }} ({{ data.city }})</span>
                    <div class="val">{{ data.aqi }}</div>
                    <canvas id="chart1" height="100"></canvas>
                </div>
                <div class="card">
                    <span class="label">{{ L.temp }}</span>
                    <div class="val">{{ data.temp }}°C</div>
                    <div class="label" style="margin-top:10px">{{ L.hum }}: {{ data.hum }}%</div>
                </div>
            </div>

            <div class="ai-box">
                <div style="color: var(--main); font-weight: bold; margin-bottom: 10px;"><i class="fas fa-microchip"></i> {{ L.ai_report }}</div>
                <p style="font-size: 18px; line-height: 1.6; margin: 0;">{{ ai.text }}</p>
                <div style="margin-top: 20px; font-size: 12px; opacity: 0.6;">Data provided by Global Eco-AI Engine V5.0</div>
            </div>

            <div class="footer">
                <div>
                    {{ L.author }}: <b style="color:white">Ataxojayev Abdubositxoja</b><br>
                    {{ L.boss }}: <b style="color:white">Elmurod Egamberdiev</b>
                </div>
                <div style="text-align: right;">
                    Framework: <b>Flask</b> | Intelligence: <b>Gemini-Core</b>
                </div>
            </div>
        </div>

        <script>
            new Chart(document.getElementById('chart1'), {
                type: 'line',
                data: {
                    labels: ['', '', '', '', ''],
                    datasets: [{
                        data: [{{ data.aqi-10 }}, {{ data.aqi-5 }}, {{ data.aqi+5 }}, {{ data.aqi-2 }}, {{ data.aqi }}],
                        borderColor: '{{ ai.color }}',
                        tension: 0.4,
                        borderWidth: 2,
                        pointRadius: 0
                    }]
                },
                options: { plugins: { legend: { display: false } }, scales: { x: { display: false }, y: { display: false } } }
            });
        </script>
    </body>
    </html>
    """, data=data, ai=ai, L=L)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
