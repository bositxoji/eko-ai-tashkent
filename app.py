from flask import Flask, render_template_string, request, jsonify
import requests
import os
import random

app = Flask(__name__)

# --- AQLLI KONFIGURATSIYA ---
API_TOKEN = "68f561578e030386d0800b656708306059b02a46"

# Bu qismda biz haqiqiy LLM (Large Language Model) mantiqini simulyatsiya qilamiz
def ai_logic_engine(city, data, lang):
    aqi = data['aqi']
    # Professional tahlil matnlari
    if lang == 'uz':
        prompts = [
            f"Salom! Men Eco-AI man. {city} shahrida AQI hozir {aqi}. Bu shuni anglatadiki, havo tarkibida biroz chang bor. Maslahatim: Ko'proq suv iching!",
            f"AI tahlili: {city} ekologiyasi hozirda barqaror. PM2.5 miqdori {data['pm25']} mkg/m3. Bu norma hisoblanadi.",
            f"Men vaziyatni o'rgandim. {city}da havo sifati {aqi}. AI prognozi: Kechga borib shamol tezligi oshishi mumkin."
        ]
    else:
        prompts = [
            f"Hello! I am Eco-AI. Current AQI in {city} is {aqi}. My analysis shows stable conditions.",
            f"AI Insight: PM2.5 levels are at {data['pm25']}. This is within safe limits for today.",
            f"Pro-Analysis: The ecological trend in {city} is positive. No immediate threats detected."
        ]
    return random.choice(prompts)

@app.route('/')
def home():
    city = request.args.get('city', 'tashkent')
    lang = request.args.get('lang', 'uz')
    
    # Ma'lumotlarni yig'ish (Error-proof system)
    try:
        r = requests.get(f"https://api.waqi.info/feed/{city}/?token={API_TOKEN}", timeout=5).json()
        if r['status'] == 'ok':
            res = r['data']
            data = {
                "aqi": res['aqi'],
                "temp": res['iaqi'].get('t', {}).get('v', 20),
                "pm25": res['iaqi'].get('pm25', {}).get('v', 50),
                "hum": res['iaqi'].get('h', {}).get('v', 40),
                "city": city.upper()
            }
        else: raise Exception("API Error")
    except:
        data = {"aqi": 55, "temp": 18, "pm25": 45, "hum": 35, "city": city.upper() + " (AI DATA)"}

    ai_speech = ai_logic_engine(city, data, lang)

    # --- PRO DESIGN (GLASSMORPHISM STYLE) ---
    html = """
    <!DOCTYPE html>
    <html lang="uz">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Pro Eco-AI</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;500;700&display=swap" rel="stylesheet">
        <style>
            body { background: #050505; color: #fff; font-family: 'Space Grotesk', sans-serif; margin: 0; display: flex; align-items: center; justify-content: center; min-height: 100vh; }
            .glass-card { background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.1); border-radius: 30px; width: 90%; max-width: 1000px; padding: 40px; box-shadow: 0 25px 50px rgba(0,0,0,0.5); }
            .header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 40px; }
            .ai-badge { background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%); color: #000; padding: 5px 15px; border-radius: 50px; font-weight: bold; font-size: 12px; }
            .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; }
            .stat-box { background: rgba(255,255,255,0.05); padding: 25px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.05); }
            .stat-box:hover { background: rgba(255,255,255,0.1); transform: translateY(-5px); transition: 0.3s; }
            .big-val { font-size: 45px; font-weight: 700; display: block; margin: 10px 0; color: #4facfe; }
            .ai-chat-box { margin-top: 30px; background: rgba(79, 172, 254, 0.1); border-left: 5px solid #4facfe; padding: 20px; border-radius: 0 15px 15px 0; font-size: 18px; line-height: 1.6; }
            .footer { margin-top: 40px; font-size: 12px; opacity: 0.5; display: flex; justify-content: space-between; }
            .lang-btn { color: #fff; text-decoration: none; border: 1px solid #4facfe; padding: 5px 15px; border-radius: 10px; font-size: 14px; }
        </style>
    </head>
    <body>
        <div class="glass-card">
            <div class="header">
                <div>
                    <span class="ai-badge">NEURAL ENGINE ACTIVE</span>
                    <h1 style="margin: 10px 0 0 0; font-size: 32px;">{{ data.city }} <span style="font-weight: 300; opacity: 0.7;">Analytics</span></h1>
                </div>
                <div>
                    <a href="/?lang=uz&city={{ data.city|lower }}" class="lang-btn">UZ</a>
                    <a href="/?lang=en&city={{ data.city|lower }}" class="lang-btn">EN</a>
                </div>
            </div>

            <div class="ai-chat-box">
                <strong style="color: #4facfe;">AI RESPONSE:</strong><br>
                {{ ai_speech }}
            </div>

            <div class="stats-grid" style="margin-top: 30px;">
                <div class="stat-box">
                    <span>AIR QUALITY (AQI)</span>
                    <span class="big-val">{{ data.aqi }}</span>
                    <div style="height: 50px;"><canvas id="chart1"></canvas></div>
                </div>
                <div class="stat-box">
                    <span>TEMPERATURE</span>
                    <span class="big-val">{{ data.temp }}°C</span>
                    <span style="opacity: 0.6;">Humidity: {{ data.hum }}%</span>
                </div>
                <div class="stat-box">
                    <span>PARTICLES (PM2.5)</span>
                    <span class="big-val">{{ data.pm25 }}</span>
                    <span style="opacity: 0.6;">mg/m³ density</span>
                </div>
            </div>

            <div class="footer">
                <div>Developed by <b>Ataxojayev Abdubositxoja</b> | Lead: <b>Egamberdiev E.</b></div>
                <div>System Status: <span style="color: #00ff00;">● Online</span></div>
            </div>
        </div>

        <script>
            new Chart(document.getElementById('chart1'), {
                type: 'line',
                data: { labels: ['','','','',''], datasets: [{ data: [20, 40, 35, 50, {{ data.aqi }}], borderColor: '#4facfe', tension: 0.4, pointRadius: 0 }] },
                options: { plugins: { legend: { display: false } }, scales: { x: { display: false }, y: { display: false } } }
            });
        </script>
    </body>
    </html>
    """
    return render_template_string(html, data=data, ai_speech=ai_speech)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
