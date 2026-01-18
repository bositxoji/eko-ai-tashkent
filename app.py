from flask import Flask, render_template_string, request
import requests
import os
from datetime import datetime

app = Flask(__name__)

# O'zbekiston shaharlari uchun aniq stansiya nomlari
CITIES = {
    "uzbekistan/tashkent/us-embassy": "Toshkent",
    "uzbekistan/samarkand": "Samarqand",
    "uzbekistan/bukhara": "Buxoro",
    "uzbekistan/namangan": "Namangan",
    "uzbekistan/andijan": "Andijon",
    "uzbekistan/nukus": "Nukus"
}

def get_ai_logic(aqi):
    """ AQI darajasiga qarab AI tahlili va dizayn parametrlarini qaytaradi """
    if aqi <= 50:
        return {"status": "A'lo", "color": "#00b894", "advice": "AI: Havo juda toza! Ochiq havoda mashg'ulotlar uchun ajoyib vaqt."}
    elif aqi <= 100:
        return {"status": "O'rtacha", "color": "#fdcb6e", "advice": "AI: Havo sifati qoniqarli. Sezgir insonlar ehtiyot bo'lishi kerak."}
    elif aqi <= 150:
        return {"status": "Nosog'lom", "color": "#e17055", "advice": "AI: Havo tarkibi buzilgan. Ko'chada uzoq vaqt qolish tavsiya etilmaydi."}
    else:
        return {"status": "Xavfli", "color": "#d63031", "advice": "AI OGOHLANTIRISHI: Havo o'ta zaharli! Darhol himoya niqobini taqing."}

@app.route('/')
def home():
    city_path = request.args.get('city', 'uzbekistan/tashkent/us-embassy')
    # Yangilangan API kalit (shaxsiy va barqaror)
    token = "68f561578e030386d0800b656708306059b02a46" 
    url = f"https://api.waqi.info/feed/{city_path}/?token={token}"
    
    try:
        response = requests.get(url).json()
        if response['status'] == 'ok':
            res_data = response['data']
            aqi = res_data.get('aqi', 0)
            iaqi = res_data.get('iaqi', {})
            
            # Parametrlarni olish (Xatolardan himoyalangan holda)
            temp = iaqi.get('t', {}).get('v', "Noma'lum")
            pm25 = iaqi.get('pm25', {}).get('v', 0)
            wind = iaqi.get('w', {}).get('v', 0)
            
            ai_data = get_ai_logic(aqi)
            
            display_data = {
                "aqi": aqi, "temp": temp, "pm25": pm25, "wind": wind,
                "status": ai_data['status'], "color": ai_data['color'], "advice": ai_data['advice'],
                "city_name": CITIES.get(city_path),
                "time": datetime.now().strftime("%H:%M:%S")
            }
        else:
            return "API ulanishida xatolik yuz berdi. Iltimos, sahifani yangilang."
    except Exception as e:
        return f"Tizim xatosi: {e}"

    html_template = """
    <!DOCTYPE html>
    <html lang="uz">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Professional AI Eco System</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            body { font-family: 'Inter', sans-serif; background: #f0f2f5; margin: 0; padding: 20px; color: #333; }
            .container { max-width: 800px; margin: 0 auto; background: white; border-radius: 25px; padding: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); position: relative; }
            .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }
            .grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 30px; }
            .card { background: #fff; border: 1px solid #eee; padding: 20px; border-radius: 20px; text-align: center; }
            .val { font-size: 32px; font-weight: 800; color: {{ data.color }}; }
            .ai-box { background: #f8f9fa; border-left: 8px solid {{ data.color }}; padding: 20px; border-radius: 15px; margin-bottom: 30px; font-size: 17px; }
            .chart-box { height: 300px; margin-bottom: 50px; }
            .authors { border-top: 1px solid #eee; padding-top: 20px; text-align: right; font-size: 13px; color: #777; line-height: 1.6; }
            select { padding: 10px 20px; border-radius: 12px; border: 1px solid #ddd; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div>
                    <h1 style="margin:0">Eko-AI Monitoring</h1>
                    <small>Real-vaqt tahlili | {{ data.time }}</small>
                </div>
                <form action="/" method="get">
                    <select name="city" onchange="this.form.submit()">
                        {% for path, name in cities.items() %}
                        <option value="{{ path }}" {% if path == current_city %}selected{% endif %}>{{ name }}</option>
                        {% endfor %}
                    </select>
                </form>
            </div>

            <div class="grid">
                <div class="card">
                    <div style="font-size:12px; color:#999">AQI INDEX ({{ data.city_name }})</div>
                    <div class="val">{{ data.aqi }}</div>
                    <div style="font-weight:700; color:{{ data.color }}">{{ data.status }}</div>
                </div>
                <div class="card">
                    <div style="font-size:12px; color:#999">HARORAT</div>
                    <div class="val" style="color:#2d3436">{{ data.temp }}°C</div>
                </div>
                <div class="card">
                    <div style="font-size:12px; color:#999">CHANG (PM2.5)</div>
                    <div class="val" style="color:#2d3436">{{ data.pm25 }}</div>
                </div>
            </div>

            <div class="ai-box">
                <i class="fas fa-robot"></i> <b>AI Tahlili:</b> {{ data.advice }}
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
                    labels: ['Havo Sifati', 'Harorat', 'PM2.5 Chang'],
                    datasets: [{
                        label: 'Ko\'rsatkichlar',
                        data: [{{ data.aqi }}, {{ data.temp if data.temp != "Noma'lum" else 0 }}, {{ data.pm25 }}],
                        backgroundColor: ['{{ data.color }}', '#3498db', '#9b59b6'],
                        borderRadius: 10
                    }]
                },
                options: { responsive: true, maintainAspectRatio: false }
            });
        </script>
    </body>
    </html>
    """
    return render_template_string(html_template, data=display_data, cities=CITIES, current_city=city_path)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
