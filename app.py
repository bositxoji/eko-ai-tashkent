from flask import Flask, render_template_string, request
import requests
import os
from datetime import datetime

app = Flask(__name__)

# Shaharlar va ularning xalqaro stansiya ID-lari (aniqlik uchun)
CITIES = {
    "tashkent": "Tashkent",
    "samarkand": "Samarkand",
    "bukhara": "Bukhara",
    "namangan": "Namangan",
    "andijan": "Andijon",
    "nukus": "Nukus"
}

def get_ai_analysis(aqi, temp, pm25):
    """ Haqiqiy AI mantiqiy tahlili """
    analysis = {
        "status": "",
        "color": "",
        "advice": "",
        "icon": ""
    }
    
    # AQI va PM2.5 asosida tahlil
    if aqi <= 50:
        analysis.update({"status": "A'lo", "color": "#00b894", "icon": "fa-smile-beam", 
                        "advice": "AI Xulosasi: Havo ideal darajada toza. Bugun o'pka uchun haqiqiy bayram!"})
    elif aqi <= 100:
        analysis.update({"status": "O'rtacha", "color": "#fdcb6e", "icon": "fa-meh", 
                        "advice": "AI Xulosasi: Chang miqdori biroz oshgan. Allergiyasi borlar ehtiyot bo'lishi lozim."})
    elif aqi <= 150:
        analysis.update({"status": "Zararli", "color": "#e17055", "icon": "fa-mask", 
                        "advice": "AI Xulosasi: Havo sifati pasaygan. Ko'chada uzoq qolish tavsiya etilmaydi."})
    else:
        analysis.update({"status": "Xavfli", "color": "#d63031", "icon": "fa-biohazard", 
                        "advice": "AI OGOHLANTIRISHI: Havo o'ta zaharli! Darhol niqob taqing va yopiq binoda qoling."})
        
    # Harorat bo'yicha qo'shimcha AI mantiq
    if temp < 5:
        analysis["advice"] += " Shuningdek, havo sovuq, issiq kiyinishni unutmang."
        
    return analysis

@app.route('/')
def home():
    city_code = request.args.get('city', 'tashkent')
    token = "demo" # Real loyihada waqi.info'dan shaxsiy token olish tavsiya etiladi
    url = f"https://api.waqi.info/feed/{city_code}/?token={token}"
    
    try:
        r = requests.get(url).json()
        if r['status'] == 'ok':
            raw_data = r['data']
            aqi = raw_data.get('aqi', 0)
            iaqi = raw_data.get('iaqi', {})
            
            # Parametrlarni olish
            temp = iaqi.get('t', {}).get('v', 0)
            pm25 = iaqi.get('pm25', {}).get('v', 0)
            wind = iaqi.get('w', {}).get('v', 0)
            humid = iaqi.get('h', {}).get('v', 0)
            
            ai = get_ai_analysis(aqi, temp, pm25)
            
            data = {
                "aqi": aqi, "temp": temp, "pm25": pm25, "wind": wind, "humid": humid,
                "ai": ai, "city": CITIES.get(city_code), "time": datetime.now().strftime("%H:%M")
            }
        else:
            return "API xatosi: Ma'lumot olib bo'lmadi. Tokenni tekshiring."
    except Exception as e:
        return f"Tizim xatosi: {str(e)}"

    html_template = """
    <!DOCTYPE html>
    <html lang="uz">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Global AI Eco Monitoring</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        <style>
            :root { --main-color: {{ data.ai.color }}; }
            body { background: #f4f7f6; font-family: 'Inter', sans-serif; margin: 0; padding: 20px; color: #2d3436; }
            .container { max-width: 900px; margin: 0 auto; background: white; border-radius: 30px; padding: 40px; box-shadow: 0 20px 60px rgba(0,0,0,0.05); position: relative; }
            
            .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 40px; }
            .city-picker { padding: 12px 20px; border-radius: 15px; border: 2px solid #eee; font-weight: 600; cursor: pointer; outline: none; }
            
            .main-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 40px; }
            .card { background: #fff; border: 1px solid #f0f0f0; padding: 25px; border-radius: 20px; text-align: center; transition: 0.3s; }
            .card:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.05); }
            .card i { font-size: 24px; color: var(--main-color); margin-bottom: 15px; }
            .val { font-size: 36px; font-weight: 800; display: block; }
            .unit { font-size: 14px; color: #b2bec3; font-weight: 600; }

            .ai-section { background: #f9fafb; padding: 30px; border-radius: 25px; border-left: 10px solid var(--main-color); margin-bottom: 40px; }
            .ai-header { display: flex; align-items: center; gap: 15px; font-size: 20px; font-weight: 700; margin-bottom: 15px; }
            
            .chart-box { background: #fff; padding: 20px; border-radius: 20px; border: 1px solid #f0f0f0; margin-bottom: 80px; height: 300px; }
            
            .source-tag { font-size: 12px; color: #bdc3c7; margin-top: 10px; }
            .authors { position: absolute; bottom: 20px; right: 40px; text-align: right; font-size: 13px; line-height: 1.6; color: #636e72; }
            .authors b { color: #2d3436; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div>
                    <h1 style="margin:0; font-size: 28px;">Global AI Eco System</h1>
                    <div class="source-tag">Manba: World Air Quality Index (WAQI) | {{ data.time }}</div>
                </div>
                <form action="/" method="get">
                    <select name="city" class="city-picker" onchange="this.form.submit()">
                        {% for code, name in cities.items() %}
                        <option value="{{ code }}" {% if code == current_city %}selected{% endif %}>{{ name }}</option>
                        {% endfor %}
                    </select>
                </form>
            </div>

            <div class="main-grid">
                <div class="card">
                    <i class="fas fa-wind"></i>
                    <span class="unit">AQI INDEX</span>
                    <span class="val" style="color: var(--main-color)">{{ data.aqi }}</span>
                    <small style="font-weight: 700; color: var(--main-color)">{{ data.ai.status }}</small>
                </div>
                <div class="card">
                    <i class="fas fa-thermometer-half"></i>
                    <span class="unit">HARORAT</span>
                    <span class="val">{{ data.temp }}°C</span>
                </div>
                <div class="card">
                    <i class="fas fa-smog"></i>
                    <span class="unit">PM2.5 CHANG</span>
                    <span class="val">{{ data.pm25 }}</span>
                </div>
            </div>

            <div class="ai-section">
                <div class="ai-header">
                    <i class="fas {{ data.ai.icon }}" style="color: var(--main-color)"></i>
                    AI Analitik Tahlili
                </div>
                <p style="margin:0; line-height: 1.6; font-size: 16px;">{{ data.ai.advice }}</p>
            </div>

            <div class="chart-box">
                <canvas id="ecoChart"></canvas>
            </div>

            <div class="authors">
                Muallif: <b>Ataxojayev Abdubositxoja</b><br>
                Ilmiy rahbar: <b>Elmurod Egamberdiev</b>
            </div>
        </div>

        <script>
            const ctx = document.getElementById('ecoChart').getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: ['AQI', 'Temp (°C)', 'Chang (PM2.5)', 'Namlik (%)', 'Shamol (m/s)'],
                    datasets: [{
                        label: 'Hozirgi ko\'rsatkichlar ({{ data.city }})',
                        data: [{{ data.aqi }}, {{ data.temp }}, {{ data.pm25 }}, {{ data.humid }}, {{ data.wind }}],
                        backgroundColor: ['{{ data.ai.color }}', '#0984e3', '#6c5ce7', '#00cec9', '#fab1a0'],
                        borderRadius: 10
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: { y: { beginAtZero: true, grid: { display: false } } }
                }
            });
        </script>
    </body>
    </html>
    """
    return render_template_string(html_template, data=data, cities=CITIES, current_city=city_code)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
