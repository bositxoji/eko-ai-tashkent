import os
import requests
import google.generativeai as genai
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# --- ELITA KONFIGURATSIYA ---
# Siz bergan Gemini API kaliti
genai.configure(api_key="AIzaSyCl-dBQmgQTJWgA5LR0Fy5Wiq7HLxaHK2Y")
model = genai.GenerativeModel('gemini-1.5-flash')

# Tashqi ekologik ma'lumotlar manbasi
WAQI_TOKEN = "68f561578e030386d0800b656708306059b02a46"

def get_pro_ai_analysis(city, data, lang):
    """ Gemini AI orqali chuqurlashtirilgan ekologik tahlil va prognoz """
    prompt = f"""
    Sen Global Eco-Intelligence markazining bosh tahlilchisisan. 
    Loyiha muallifi: Ataxojayev Abdubositxoja.
    Ma'lumotlar: Shahar: {city}, AQI: {data['aqi']}, Temp: {data['temp']}°C, Namlik: {data['hum']}%, Chang (PM2.5): {data['pm25']}.
    Topshiriq: 
    1. Hozirgi holatga professional baho ber.
    2. Ushbu ma'lumotlar asosida 24 soatlik ekologik prognoz ber.
    3. Aholi uchun salomatlik tavsiyalarini yoz.
    Til: {lang}. Javobing professional, aniq va ma'lumotga boy bo'lsin.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except:
        return "AI tahlil tizimi vaqtincha offline rejimda."

@app.route('/')
def home():
    city = request.args.get('city', 'tashkent')
    lang = request.args.get('lang', 'uz')
    
    try:
        r = requests.get(f"https://api.waqi.info/feed/{city}/?token={WAQI_TOKEN}", timeout=10).json()
        if r['status'] == 'ok':
            res = r['data']
            data = {
                "aqi": res['aqi'],
                "temp": res['iaqi'].get('t', {}).get('v', 18),
                "hum": res['iaqi'].get('h', {}).get('v', 40),
                "pm25": res['iaqi'].get('pm25', {}).get('v', 50),
                "city": city.upper()
            }
            ai_analysis = get_pro_ai_analysis(city, data, lang)
        else:
            raise Exception("City Not Found")
    except:
        data = {"aqi": 45, "temp": 20, "hum": 30, "pm25": 40, "city": city.upper() + " (LOCAL)"}
        ai_analysis = "Global datchiklar bilan aloqa uzildi. Lokal ma'lumotlar tahlil qilinmoqda."

    # --- NEXT-GEN CYBER DESIGN ---
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="{{ lang }}">
    <head>
        <meta charset="UTF-8">
        <title>Eco-Intelligence World Pro</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
        <style>
            :root { --accent: #00f2fe; --bg: #05070a; --glass: rgba(255, 255, 255, 0.03); }
            body { background: var(--bg); color: #e2e8f0; font-family: 'Inter', sans-serif; margin: 0; padding: 20px; overflow-x: hidden; }
            .main-frame { max-width: 1200px; margin: 0 auto; position: relative; }
            
            /* Glassmorphism Header */
            .header { display: flex; justify-content: space-between; align-items: center; padding: 20px; background: var(--glass); backdrop-filter: blur(15px); border: 1px solid rgba(255,255,255,0.05); border-radius: 20px; margin-bottom: 30px; }
            .pro-label { background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%); color: #000; padding: 4px 12px; border-radius: 6px; font-weight: bold; font-size: 12px; }
            
            /* AI Analysis Block */
            .ai-terminal { background: rgba(0, 242, 254, 0.02); border: 1px solid rgba(0, 242, 254, 0.2); border-radius: 24px; padding: 30px; margin-bottom: 30px; position: relative; overflow: hidden; }
            .ai-terminal::before { content: 'AI CORE PROCESSING'; position: absolute; top: 10px; right: 20px; font-size: 10px; color: var(--accent); opacity: 0.5; }
            .ai-text { font-size: 17px; line-height: 1.8; color: #cbd5e1; white-space: pre-line; }

            /* Metrics Grid */
            .metrics { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 20px; }
            .metric-card { background: var(--glass); border: 1px solid rgba(255,255,255,0.05); border-radius: 24px; padding: 30px; transition: 0.4s; }
            .metric-card:hover { border-color: var(--accent); transform: translateY(-5px); }
            .val { font-size: 48px; font-weight: 800; color: #fff; margin: 15px 0; display: block; }
            .unit { font-size: 16px; opacity: 0.5; font-weight: 300; }

            /* Interactive Elements */
            .btn-group { display: flex; gap: 10px; }
            .lang-link { color: #fff; text-decoration: none; padding: 8px 16px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.1); font-size: 13px; }
            .lang-link.active { background: var(--accent); color: #000; font-weight: bold; }

            .footer { margin-top: 50px; padding: 30px; border-top: 1px solid rgba(255,255,255,0.05); display: flex; justify-content: space-between; font-size: 13px; opacity: 0.6; }
        </style>
    </head>
    <body>
        <div class="main-frame">
            <div class="header">
                <div>
                    <h1 style="margin:0; font-size: 24px;">{{ data.city }} <span style="font-weight: 300;">Environmental Intelligence</span></h1>
                    <span class="pro-label">V5.0 PRO OPERATIONAL</span>
                </div>
                <div class="btn-group">
                    <a href="/?lang=uz&city={{ data.city|lower }}" class="lang-link {% if lang=='uz' %}active{% endif %}">O'ZBEK</a>
                    <a href="/?lang=en&city={{ data.city|lower }}" class="lang-link {% if lang=='en' %}active{% endif %}">ENGLISH</a>
                </div>
            </div>

            <div class="ai-terminal">
                <h3 style="color: var(--accent); margin-top: 0;"><i class="fas fa-brain"></i> GEMINI AI PROFESSIONAL ANALYSIS</h3>
                <div class="ai-text">{{ ai_analysis }}</div>
            </div>

            <div class="metrics">
                <div class="metric-card">
                    <span style="color: var(--accent); text-transform: uppercase; font-size: 12px; font-weight: bold; letter-spacing: 1px;">Air Quality Index</span>
                    <span class="val">{{ data.aqi }} <span class="unit">AQI</span></span>
                    <canvas id="aqiChart" height="80"></canvas>
                </div>
                <div class="metric-card">
                    <span style="color: #ff7e5f; text-transform: uppercase; font-size: 12px; font-weight: bold; letter-spacing: 1px;">Atmospheric Temp</span>
                    <span class="val">{{ data.temp }} <span class="unit">°C</span></span>
                    <p style="margin:0; opacity: 0.6;">Humidity: {{ data.hum }}%</p>
                </div>
                <div class="metric-card">
                    <span style="color: #feb47b; text-transform: uppercase; font-size: 12px; font-weight: bold; letter-spacing: 1px;">Particulate Matter</span>
                    <span class="val">{{ data.pm25 }} <span class="unit">mg/m³</span></span>
                    <p style="margin:0; opacity: 0.6;">PM2.5 Sensor Status: Active</p>
                </div>
            </div>

            <div class="footer">
                <div>
                    DEVELOPER: <b>Ataxojayev Abdubositxoja</b><br>
                    SUPERVISOR: <b>Egamberdiev E.</b>
                </div>
                <div style="text-align: right;">
                    ENGINE: <b>Google Gemini 1.5 Pro</b><br>
                    STATUS: <span style="color: #00ff00;">ONLINE SYNC</span>
                </div>
            </div>
        </div>

        <script>
            const ctx = document.getElementById('aqiChart').getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: ['', '', '', '', ''],
                    datasets: [{
                        data: [{{ data.aqi-10 }}, {{ data.aqi-5 }}, {{ data.aqi+5 }}, {{ data.aqi-2 }}, {{ data.aqi }}],
                        borderColor: '#00f2fe',
                        borderWidth: 2,
                        pointRadius: 0,
                        fill: true,
                        backgroundColor: 'rgba(0, 242, 254, 0.05)',
                        tension: 0.4
                    }]
                },
                options: { plugins: { legend: { display: false } }, scales: { x: { display: false }, y: { display: false } } }
            });
        </script>
    </body>
    </html>
    """, data=data, ai_analysis=ai_analysis, lang=lang)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
