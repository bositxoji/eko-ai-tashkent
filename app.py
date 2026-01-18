from flask import Flask, render_template_string
import requests
import os
from datetime import datetime

app = Flask(__name__)

# --- PROFESSIONAL AI TAHLIL QISMI ---
def analyze_data(data):
    try:
        aqi = data.get('aqi', 0)
        iaqi = data.get('iaqi', {})
        
        # Qo'shimcha parametrlar (agar API bersa)
        pm25 = iaqi.get('pm25', {}).get('v', 0)
        temp = iaqi.get('t', {}).get('v', 0)
        wind = iaqi.get('w', {}).get('v', 0)
        
        # 1. Asosiy Status va Rang
        if aqi <= 50:
            status = "A'lo Darajada"
            color = "#00e676" # Yorqin yashil
            bg_gradient = "linear-gradient(135deg, #11998e, #38ef7d)"
        elif aqi <= 100:
            status = "O'rtacha"
            color = "#ffd600" # Sariq
            bg_gradient = "linear-gradient(135deg, #fce38a, #f38181)"
        elif aqi <= 150:
            status = "Nosog'lom (Sezgir guruhlar uchun)"
            color = "#ff9100" # Zarg'aldoq
            bg_gradient = "linear-gradient(135deg, #f46b45, #eea849)"
        else:
            status = "Xavfli"
            color = "#ff1744" # Qizil
            bg_gradient = "linear-gradient(135deg, #cb2d3e, #ef473a)"

        # 2. Smart AI Maslahatchi (Mantiqiy zanjir)
        advice = []
        
        # Havo bo'yicha
        if aqi > 100:
            advice.append("⚠️ Havo tarkibida zararli moddalar ortgan. Niqob taqish tavsiya etiladi.")
        else:
            advice.append("✅ Havo toza, xonalarni shamollatish uchun ajoyib vaqt.")
            
        # Harorat va Shamol bo'yicha (Qo'shimcha intellekt)
        if temp < 5:
            advice.append("❄️ Tashqarida sovuq. Issiq kiyining.")
        elif temp > 30:
            advice.append("☀️ Kun issiq. Ko'proq suv iching va quyoshda ko'p yurmang.")
            
        if wind > 10:
            advice.append("💨 Kuchli shamol kuzatilmoqda. Chang ko'tarilishi mumkin, ehtiyot bo'ling.")

        return {
            "aqi": aqi,
            "status": status,
            "color": color,
            "bg": bg_gradient,
            "pm25": pm25,
            "temp": temp,
            "wind": wind,
            "advice": " ".join(advice),
            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
    except Exception as e:
        return None

def get_full_data(city="Tashkent"):
    token = "demo" # Agar shaxsiy tokeningiz bo'lsa, shu yerga qo'ying
    url = f"https://api.waqi.info/feed/{city}/?token={token}"
    try:
        r = requests.get(url).json()
        if r['status'] == 'ok':
            return analyze_data(r['data'])
        return None
    except:
        return None

@app.route('/')
def home():
    data = get_full_data("Tashkent")
    
    if not data:
        return "Ma'lumot olishda xatolik. Keyinroq urinib ko'ring.", 500

    # HTML TEMPLATE - PROFESSIONAL DASHBOARD
    html_template = """
    <!DOCTYPE html>
    <html lang="uz">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Eko-AI Pro Dashboard</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        
        <style>
            :root {
                --glass-bg: rgba(255, 255, 255, 0.25);
                --glass-border: 1px solid rgba(255, 255, 255, 0.18);
                --text-color: #2d3436;
            }
            body {
                font-family: 'Segoe UI', sans-serif;
                background: {{ data.bg }};
                background-size: 400% 400%;
                animation: gradient 15s ease infinite;
                margin: 0;
                min-height: 100vh;
                color: var(--text-color);
                display: flex;
                justify-content: center;
                padding: 20px;
            }
            @keyframes gradient {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }
            
            .dashboard {
                background: rgba(255, 255, 255, 0.85);
                backdrop-filter: blur(20px);
                border-radius: 30px;
                padding: 30px;
                width: 100%;
                max-width: 800px;
                box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            }
            
            .header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 30px;
                border-bottom: 2px solid rgba(0,0,0,0.05);
                padding-bottom: 20px;
            }
            .header h1 { margin: 0; font-size: 24px; color: #2d3436; }
            .badge { background: #2d3436; color: white; padding: 5px 12px; border-radius: 20px; font-size: 12px; }
            
            /* Asosiy ko'rsatkichlar */
            .main-stats {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }
            .stat-card {
                background: white;
                padding: 20px;
                border-radius: 20px;
                text-align: center;
                box-shadow: 0 10px 20px rgba(0,0,0,0.05);
                transition: transform 0.3s;
            }
            .stat-card:hover { transform: translateY(-5px); }
            
            .big-number { font-size: 48px; font-weight: bold; color: {{ data.color }}; }
            .label { color: #636e72; font-size: 14px; text-transform: uppercase; letter-spacing: 1px; }
            
            /* AI Section */
            .ai-box {
                background: #f1f2f6;
                padding: 25px;
                border-radius: 20px;
                border-left: 6px solid {{ data.color }};
                margin-bottom: 30px;
            }
            .ai-title { font-weight: bold; margin-bottom: 10px; display: flex; align-items: center; gap: 10px; }
            
            /* Chart Container */
            .chart-container {
                background: white;
                padding: 20px;
                border-radius: 20px;
                height: 250px;
                margin-bottom: 20px;
            }

            .btn-refresh {
                width: 100%;
                padding: 15px;
                background: #2d3436;
                color: white;
                border: none;
                border-radius: 15px;
                font-size: 16px;
                cursor: pointer;
                transition: 0.3s;
            }
            .btn-refresh:hover { background: #000; }
        </style>
    </head>
    <body>
        <div class="dashboard">
            <div class="header">
                <div>
                    <h1>Toshkent AI Monitoring</h1>
                    <small>{{ data.date }}</small>
                </div>
                <span class="badge">PRO VERSION v2.1</span>
            </div>

            <div class="main-stats">
                <div class="stat-card">
                    <div class="label">Havo Sifati (AQI)</div>
                    <div class="big-number">{{ data.aqi }}</div>
                    <div style="color: {{ data.color }}; font-weight: bold;">{{ data.status }}</div>
                </div>
                
                <div class="stat-card">
                    <div class="label">Harorat</div>
                    <div class="big-number">{{ data.temp }}°C</div>
                    <div class="label">Havo harorati</div>
                </div>
                
                <div class="stat-card">
                    <div class="label">Mayda Chang (PM2.5)</div>
                    <div class="big-number">{{ data.pm25 }}</div>
                    <div class="label">µg/m³</div>
                </div>
            </div>

            <div class="ai-box">
                <div class="ai-title">
                    <i class="fas fa-robot"></i> Sun'iy Intellekt Tahlili:
                </div>
                {{ data.advice }}
            </div>

            <div class="chart-container">
                <canvas id="airChart"></canvas>
            </div>

            <button class="btn-refresh" onclick="location.reload()">
                <i class="fas fa-sync-alt"></i> Tizimni Yangilash
            </button>
        </div>

        <script>
            // Grafik chizish qismi
            const ctx = document.getElementById('airChart').getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: ['AQI (Havo)', 'PM2.5 (Chang)', 'Shamol (m/s)', 'Harorat (C)'],
                    datasets: [{
                        label: 'Eko Ko\'rsatkichlar',
                        data: [{{ data.aqi }}, {{ data.pm25 }}, {{ data.wind }}, {{ data.temp }}],
                        backgroundColor: [
                            '{{ data.color }}',
                            'rgba(54, 162, 235, 0.6)',
                            'rgba(75, 192, 192, 0.6)',
                            'rgba(255, 159, 64, 0.6)'
                        ],
                        borderColor: [
                            '{{ data.color }}',
                            'rgba(54, 162, 235, 1)',
                            'rgba(75, 192, 192, 1)',
                            'rgba(255, 159, 64, 1)'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: { beginAtZero: true }
                    }
                }
            });
        </script>
    </body>
    </html>
    """
    return render_template_string(html_template, data=data)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
