from flask import Flask, render_template_string, request
import requests
import os
from datetime import datetime

app = Flask(__name__)

# Shaharlar ro'yxati
CITIES = {
    "Tashkent": "Toshkent",
    "Samarkand": "Samarqand",
    "Bukhara": "Buxoro",
    "Namangan": "Namangan",
    "Andijan": "Andijon",
    "Nukus": "Nukus"
}

def analyze_data(data, city_name):
    try:
        aqi = data.get('aqi', 0)
        iaqi = data.get('iaqi', {})
        pm25 = iaqi.get('pm25', {}).get('v', 0)
        temp = iaqi.get('t', {}).get('v', 0)
        wind = iaqi.get('w', {}).get('v', 0)
        
        if aqi <= 50:
            status, color = "A'lo Darajada", "#00e676"
            bg = "linear-gradient(135deg, #11998e, #38ef7d)"
        elif aqi <= 100:
            status, color = "O'rtacha", "#ffd600"
            bg = "linear-gradient(135deg, #fce38a, #f38181)"
        elif aqi <= 150:
            status, color = "Nosog'lom", "#ff9100"
            bg = "linear-gradient(135deg, #f46b45, #eea849)"
        else:
            status, color = "Xavfli", "#ff1744"
            bg = "linear-gradient(135deg, #cb2d3e, #ef473a)"

        advice = []
        if aqi > 100: advice.append("⚠️ Havo tarkibi zararli. Niqob taqing.")
        else: advice.append("✅ Havo toza, sayr uchun mos vaqt.")
        if temp < 10: advice.append("❄️ Havo sovuq, issiq kiyining.")
        
        return {
            "aqi": aqi, "status": status, "color": color, "bg": bg,
            "pm25": pm25, "temp": temp, "wind": wind,
            "advice": " ".join(advice), "city": city_name,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
    except: return None

@app.route('/')
def home():
    selected_city = request.args.get('city', 'Tashkent')
    token = "demo"
    url = f"https://api.waqi.info/feed/{selected_city}/?token={token}"
    
    r = requests.get(url).json()
    data = analyze_data(r['data'], CITIES.get(selected_city, "Noma'lum")) if r['status'] == 'ok' else None

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
            body { font-family: 'Segoe UI', sans-serif; background: {{ data.bg }}; margin: 0; min-height: 100vh; display: flex; justify-content: center; padding: 20px; transition: 0.5s; }
            .dashboard { background: rgba(255, 255, 255, 0.9); backdrop-filter: blur(15px); border-radius: 30px; padding: 30px; width: 100%; max-width: 850px; position: relative; box-shadow: 0 15px 35px rgba(0,0,0,0.2); }
            
            .header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 25px; }
            .city-selector { padding: 10px; border-radius: 12px; border: 1px solid #ddd; font-size: 16px; background: white; cursor: pointer; }
            
            .main-stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 15px; margin-bottom: 25px; }
            .stat-card { background: white; padding: 20px; border-radius: 20px; text-align: center; box-shadow: 0 5px 15px rgba(0,0,0,0.05); }
            .big-num { font-size: 42px; font-weight: bold; color: {{ data.color }}; }
            
            .ai-box { background: #fdfdfd; padding: 20px; border-radius: 15px; border-left: 6px solid {{ data.color }}; margin-bottom: 25px; font-style: italic; }
            
            .authors-box { position: absolute; bottom: 20px; right: 30px; text-align: right; font-size: 13px; color: #555; line-height: 1.4; background: rgba(255,255,255,0.5); padding: 10px; border-radius: 10px; }
            .authors-box b { color: #2d3436; }

            .chart-wrapper { height: 200px; margin-bottom: 60px; }
            @media (max-width: 600px) { .authors-box { position: static; text-align: center; margin-top: 20px; } }
        </style>
    </head>
    <body>
        <div class="dashboard">
            <div class="header">
                <div>
                    <h1 style="margin:0">Katta shaharlar AI Monitoringi</h1>
                    <small>Real-vaqt tahlili: {{ data.date }}</small>
                </div>
                <form action="/" method="get">
                    <select name="city" class="city-selector" onchange="this.form.submit()">
                        {% for code, name in cities_list.items() %}
                        <option value="{{ code }}" {% if code == current_city %}selected{% endif %}>{{ name }}</option>
                        {% endfor %}
                    </select>
                </form>
            </div>

            <div class="main-stats">
                <div class="stat-card">
                    <div style="font-size:12px; color:#666">HAVO SIFATI ({{ data.city }})</div>
                    <div class="big-num">{{ data.aqi }}</div>
                    <div style="color:{{ data.color }}; font-weight:bold">{{ data.status }}</div>
                </div>
                <div class="stat-card">
                    <div style="font-size:12px; color:#666">HARORAT</div>
                    <div class="big-num">{{ data.temp }}°C</div>
                </div>
                <div class="stat-card">
                    <div style="font-size:12px; color:#666">CHANG (PM2.5)</div>
                    <div class="big-num">{{ data.pm25 }}</div>
                </div>
            </div>

            <div class="ai-box">
                <i class="fas fa-robot"></i> <b>AI Tahlili:</b> {{ data.advice }}
            </div>

            <div class="chart-wrapper">
                <canvas id="ecoChart"></canvas>
            </div>

            <div class="authors-box">
                Mualliflar: <b>Ataxojayev Abdubositxoja</b><br>
                Ilmiy rahbar: <b>Elmurod Egamberdiev</b>
            </div>
        </div>

        <script>
            const ctx = document.getElementById('ecoChart').getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: ['AQI', 'Harorat', 'Chang', 'Shamol'],
                    datasets: [{
                        label: 'Hozirgi ko\'rsatkichlar',
                        data: [{{ data.aqi }}, {{ data.temp }}, {{ data.pm25 }}, {{ data.wind }}],
                        borderColor: '{{ data.color }}',
                        backgroundColor: 'rgba(0,0,0,0.05)',
                        fill: true,
                        tension: 0.4
                    }]
                },
                options: { responsive: true, maintainAspectRatio: false }
            });
        </script>
    </body>
    </html>
    """
    return render_template_string(html_template, data=data, cities_list=CITIES, current_city=selected_city)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
