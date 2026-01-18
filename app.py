from flask import Flask, render_template_string, request
import requests
import os
from datetime import datetime

app = Flask(__name__)

# --- KONFIGURATSIYA VA TILLAR ---
LANGUAGES = {
    'uz': {
        'title': 'Global Eco-AI Tahlilchisi',
        'subtitle': 'Sun\'iy intellekt asosidagi ekologik monitoring',
        'aqi': 'Havo Sifati',
        'temp': 'Harorat',
        'humidity': 'Namlik',
        'wind': 'Shamol',
        'pm25': 'Chang (PM2.5)',
        'ai_analysis': 'AI Ekspert Xulosasi',
        'forecast': 'Ekologik Prognoz',
        'author': 'Muallif',
        'supervisor': 'Ilmiy rahbar'
    },
    'en': {
        'title': 'Global Eco-AI Analyzer',
        'subtitle': 'AI-powered environmental monitoring',
        'aqi': 'Air Quality',
        'temp': 'Temperature',
        'humidity': 'Humidity',
        'wind': 'Wind Speed',
        'pm25': 'Particulates (PM2.5)',
        'ai_analysis': 'AI Expert Analysis',
        'forecast': 'Eco Forecast',
        'author': 'Author',
        'supervisor': 'Supervisor'
    }
}

# --- AI EKSPERT TIZIMI (Logic Engine) ---
def get_advanced_ai_analysis(data, lang):
    aqi = data.get('aqi', 0)
    temp = data.get('temp', 0)
    pm25 = data.get('pm25', 0)
    
    # Bu qism Gemini/Grok tahlil uslubini simulyatsiya qiladi
    if lang == 'uz':
        if aqi <= 50:
            status = "A'lo (Safe)"
            desc = f"AI Tahlili: Hozirgi AQI {aqi} darajasi o'pka tozaligi uchun ideal. PM2.5 miqdori {pm25} normada. Ekologik prognoz: Barqaror."
        elif aqi <= 100:
            status = "O'rtacha (Caution)"
            desc = "AI Tahlili: Havo tarkibida aerozollar miqdori biroz oshgan. Umumiy salomatlik uchun xavf past, lekin sezgir guruhlarga ehtiyotkorlik tavsiya etiladi."
        else:
            status = "Xavfli (Danger)"
            desc = "AI OGOHLANTIRISHI: Atmosfera ifloslanishi kritik nuqtada. Yuqori nafas yo'llarini himoya qilish shart. Uy ichida qolish tavsiya etiladi."
    else:
        if aqi <= 50:
            status = "Excellent"
            desc = f"AI Insight: Current AQI of {aqi} is ideal. PM2.5 at {pm25} shows pristine conditions. Eco-forecast: Stable and healthy."
        else:
            status = "Alert"
            desc = "AI Insight: Pollutant levels are rising. Mitigation strategies recommended for vulnerable populations."
            
    return {"status": status, "desc": desc}

# --- ASOSIY YO'NALISHLAR ---
@app.route('/')
def home():
    # Tilni aniqlash
    lang_code = request.args.get('lang', 'uz')
    city = request.args.get('city', 'tashkent')
    L = LANGUAGES.get(lang_code, LANGUAGES['uz'])
    
    # API ulanishi (Ma'lumotlar uzilmasligi uchun ishonchli token)
    token = "68f561578e030386d0800b656708306059b02a46"
    url = f"https://api.waqi.info/feed/{city}/?token={token}"
    
    try:
        r = requests.get(url).json()
        if r['status'] == 'ok':
            raw = r['data']
            iaqi = raw.get('iaqi', {})
            
            data = {
                'aqi': raw.get('aqi', 0),
                'temp': iaqi.get('t', {}).get('v', 0),
                'humidity': iaqi.get('h', {}).get('v', 0),
                'wind': iaqi.get('w', {}).get('v', 0),
                'pm25': iaqi.get('pm25', {}).get('v', 0),
                'city_display': raw.get('city', {}).get('name', city).split(',')[0]
            }
            ai_result = get_advanced_ai_analysis(data, lang_code)
        else:
            return "API Error: Please check city name or token."
    except:
        return "Connection Error: AI is unable to fetch real-time data."

    # --- HTML INTERFEYS (Modern & Professional) ---
    html_template = """
    <!DOCTYPE html>
    <html lang="{{ lang_code }}">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Eco-AI Pro</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            :root { --accent: #2ecc71; --bg: #f8f9fa; --card: #ffffff; }
            body { font-family: 'Inter', -apple-system, sans-serif; background: var(--bg); color: #2d3436; margin: 0; padding: 20px; }
            .main-container { max-width: 1000px; margin: 0 auto; }
            
            /* Navbar */
            .nav { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }
            .lang-btn { text-decoration: none; padding: 8px 15px; background: #ddd; border-radius: 8px; color: #333; font-size: 14px; margin-left: 5px; }
            
            /* Dashboard Grid */
            .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 20px; margin-bottom: 30px; }
            .card { background: var(--card); padding: 25px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.03); border: 1px solid #eee; position: relative; overflow: hidden; }
            .card i { font-size: 20px; color: var(--accent); margin-bottom: 10px; }
            .card .label { font-size: 13px; color: #7f8c8d; text-transform: uppercase; letter-spacing: 0.5px; }
            .card .value { font-size: 32px; font-weight: 800; display: block; margin-top: 5px; }

            /* AI Section */
            .ai-expert-box { background: linear-gradient(135deg, #2d3436, #000); color: white; padding: 35px; border-radius: 24px; margin-bottom: 30px; position: relative; }
            .ai-expert-box::after { content: 'AI'; position: absolute; top: 20px; right: 20px; background: var(--accent); color: black; padding: 4px 10px; border-radius: 6px; font-weight: bold; font-size: 12px; }
            .ai-status { color: var(--accent); font-weight: bold; font-size: 18px; margin-bottom: 10px; display: block; }
            
            /* Chart */
            .chart-box { background: white; padding: 25px; border-radius: 20px; height: 300px; margin-bottom: 40px; border: 1px solid #eee; }

            /* Footer */
            .footer { display: flex; justify-content: space-between; align-items: flex-end; font-size: 13px; color: #95a5a6; border-top: 1px solid #eee; padding-top: 20px; }
            .footer b { color: #2d3436; }
            
            .badge { background: #e8f8f1; color: #2ecc71; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="main-container">
            <div class="nav">
                <div>
                    <h1 style="margin:0; font-size: 24px;">{{ L.title }}</h1>
                    <span class="badge"><i class="fas fa-check-circle"></i> Live AI Monitoring</span>
                </div>
                <div>
                    <a href="/?lang=uz&city={{ city }}" class="lang-btn">UZ</a>
                    <a href="/?lang=en&city={{ city }}" class="lang-btn">EN</a>
                </div>
            </div>

            <div class="ai-expert-box">
                <span class="ai-status">{{ ai.status }}</span>
                <h2 style="margin: 0 0 15px 0; font-size: 22px;">{{ L.ai_analysis }}</h2>
                <p style="margin:0; line-height: 1.6; opacity: 0.9; font-size: 16px;">{{ ai.desc }}</p>
            </div>

            <div class="grid">
                <div class="card">
                    <i class="fas fa-leaf"></i>
                    <span class="label">{{ L.aqi }} ({{ data.city_display }})</span>
                    <span class="value">{{ data.aqi }}</span>
                </div>
                <div class="card">
                    <i class="fas fa-temperature-high"></i>
                    <span class="label">{{ L.temp }}</span>
                    <span class="value">{{ data.temp }}°C</span>
                </div>
                <div class="card">
                    <i class="fas fa-smog"></i>
                    <span class="label">{{ L.pm25 }}</span>
                    <span class="value">{{ data.pm25 }}</span>
                </div>
                <div class="card">
                    <i class="fas fa-wind"></i>
                    <span class="label">{{ L.wind }}</span>
                    <span class="value">{{ data.wind }} m/s</span>
                </div>
            </div>

            <div class="chart-box">
                <canvas id="ecoChart"></canvas>
            </div>

            <div class="footer">
                <div>
                    {{ L.author }}: <b>Ataxojayev Abdubositxoja</b><br>
                    {{ L.supervisor }}: <b>Elmurod Egamberdiev</b>
                </div>
                <div style="text-align: right;">
                    System: <b>V3.0 Global</b><br>
                    Engine: <b>EcoAI-Gemini-1.5</b>
                </div>
            </div>
        </div>

        <script>
            const ctx = document.getElementById('ecoChart').getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: ['AQI', 'Temp', 'PM2.5', 'Wind'],
                    datasets: [{
                        label: 'Environmental Data Metrics',
                        data: [{{ data.aqi }}, {{ data.temp }}, {{ data.pm25 }}, {{ data.wind }}],
                        borderColor: '#2ecc71',
                        backgroundColor: 'rgba(46, 204, 113, 0.1)',
                        fill: true,
                        tension: 0.4,
                        borderWidth: 3,
                        pointRadius: 5
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: { y: { beginAtZero: true, grid: { display: false } }, x: { grid: { display: false } } }
                }
            });
        </script>
    </body>
    </html>
    """
    return render_template_string(html_template, data=data, ai=ai_result, L=L, lang_code=lang_code, city=city)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
