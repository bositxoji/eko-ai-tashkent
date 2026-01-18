import os
import requests
import google.generativeai as genai
from flask import Flask, render_template_string, request

app = Flask(__name__)

# --- KONFIGURATSIYA ---
GEMINI_API_KEY = "AIzaSyCl-dBQmgQTJWgA5LR0Fy5Wiq7HLxaHK2Y"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

WAQI_TOKEN = "68f561578e030386d0800b656708306059b02a46"

# --- MULTI-LANGUAGE (Tutuq belgilari tuzatilgan versiya) ---
TRANSLATIONS = {
    'uz': {
        'title': 'Neural Eco-Intelligence', 'search': 'Shahar qidiruvi...',
        'aqi': 'Havo Sifati', 'temp': 'Harorat', 'hum': 'Namlik', 'pm25': 'PM2.5 Chang',
        'ai_header': 'AI EKSPERT TAHLILI',
        'offline': "Internet uzildi! 'Eco-Hero' o'yinini boshla.", # Qo'shtirnoq to'g'irlandi
        'score': 'Ball', 'reload': 'Yangilash'
    },
    'ru': {
        'title': 'Neural Eco-Intelligence', 'search': 'Поиск города...',
        'aqi': 'Качество воздуха', 'temp': 'Температура', 'hum': 'Влажность', 'pm25': 'Пыль PM2.5',
        'ai_header': 'АНАЛИЗ НЕЙРОСЕТИ',
        'offline': 'Нет интернета! Играй в "Eco-Hero".',
        'score': 'Счет', 'reload': 'Обновить'
    },
    'en': {
        'title': 'Neural Eco-Intelligence', 'search': 'Search city...',
        'aqi': 'Air Quality', 'temp': 'Temperature', 'hum': 'Humidity', 'pm25': 'PM2.5 Particles',
        'ai_header': 'AI EXPERT ANALYSIS',
        'offline': 'No internet! Play "Eco-Hero" game.',
        'score': 'Score', 'reload': 'Reload'
    }
}

def get_ai_analysis(city, data, lang):
    """ Gemini AI tahlili """
    prompt = (f"Analyze {city} environment: AQI {data['aqi']}, Temp {data['temp']}C. "
              f"Give a professional 2-sentence summary in {lang} language.")
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except:
        return "AI analysis is temporarily offline. System monitoring active."

@app.route('/')
def home():
    # 1. Joylashuvni aniqlash
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    lang = request.args.get('lang', 'uz')
    city = request.args.get('city')
    
    if not city or city == "None":
        try:
            geo = requests.get(f"http://ip-api.com/json/{user_ip}", timeout=3).json()
            city = geo.get('city', 'Tashkent')
        except: city = "Tashkent"

    L = TRANSLATIONS.get(lang, TRANSLATIONS['uz'])

    # 2. Havo ma'lumotlarini olish (Xatolikdan himoyalangan)
    try:
        r = requests.get(f"https://api.waqi.info/feed/{city}/?token={WAQI_TOKEN}", timeout=5).json()
        if r['status'] == 'ok':
            res = r['data']
            data = {
                "aqi": res['aqi'],
                "temp": res['iaqi'].get('t', {}).get('v', 0),
                "hum": res['iaqi'].get('h', {}).get('v', 0),
                "pm25": res['iaqi'].get('pm25', {}).get('v', 0),
                "city": city.upper()
            }
        else: raise Exception()
    except:
        # Fallback (Ma'lumot topilmasa)
        data = {"aqi": 45, "temp": 20, "hum": 35, "pm25": 10, "city": city.upper() + " (STATION OFFLINE)"}

    ai_msg = get_ai_analysis(city, data, lang)

    return render_template_string("""
    <!DOCTYPE html>
    <html lang="{{ lang }}">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{{ L.title }}</title>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
        <style>
            :root { --neon: #00f2fe; --bg: #050505; --card: #111; }
            body { background: var(--bg); color: #fff; font-family: 'Segoe UI', sans-serif; margin: 0; }
            .container { max-width: 800px; margin: 50px auto; padding: 20px; }
            .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }
            .lang-switch a { color: #666; text-decoration: none; margin-left: 10px; font-weight: bold; }
            .lang-switch a.active { color: var(--neon); text-shadow: 0 0 10px var(--neon); }
            
            .main-card { background: var(--card); border: 1px solid #222; border-radius: 30px; padding: 40px; position: relative; }
            .aqi-val { font-size: 90px; font-weight: 900; color: var(--neon); margin: 10px 0; }
            .ai-terminal { background: rgba(0,242,254,0.05); padding: 20px; border-left: 4px solid var(--neon); border-radius: 10px; margin: 25px 0; }
            
            .stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; }
            .s-item { background: #1a1a1a; padding: 15px; border-radius: 15px; text-align: center; border: 1px solid #222; }

            #offline-ui { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: #000; z-index: 9999; flex-direction: column; align-items: center; justify-content: center; }
            canvas { border: 2px solid var(--neon); border-radius: 10px; background: #080808; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div style="font-weight: 900; letter-spacing: 2px;">ECO <span style="color:var(--neon)">AI</span></div>
                <div class="lang-switch">
                    <a href="/?lang=uz&city={{ data.city }}" class="{% if lang=='uz' %}active{% endif %}">UZ</a>
                    <a href="/?lang=ru&city={{ data.city }}" class="{% if lang=='ru' %}active{% endif %}">RU</a>
                    <a href="/?lang=en&city={{ data.city }}" class="{% if lang=='en' %}active{% endif %}">EN</a>
                </div>
            </div>

            <div class="main-card">
                <div style="color: var(--neon); font-size: 12px; letter-spacing: 3px;">{{ data.city }}</div>
                <div class="aqi-val">{{ data.aqi }}</div>
                <div style="opacity: 0.5;">{{ L.aqi }} (US AQI)</div>

                <div class="ai-terminal">
                    <i class="fas fa-robot"></i> <strong>{{ L.ai_header }}</strong><br>
                    <p style="font-style: italic; margin-top: 10px;">"{{ ai_msg }}"</p>
                </div>

                <div class="stats">
                    <div class="s-item"><small>{{ L.temp }}</small><br><b>{{ data.temp }}°C</b></div>
                    <div class="s-item"><small>{{ L.hum }}</small><br><b>{{ data.hum }}%</b></div>
                    <div class="s-item"><small>{{ L.pm25 }}</small><br><b>{{ data.pm25 }}</b></div>
                </div>
            </div>
        </div>

        <div id="offline-ui">
            <h2 style="color:var(--neon)">{{ L.offline }}</h2>
            <canvas id="gameCanvas" width="350" height="400"></canvas>
            <h3 id="scoreText">{{ L.score }}: 0</h3>
            <button onclick="location.reload()" style="background:var(--neon); border:none; padding:10px 30px; border-radius:10px; font-weight:bold;">{{ L.reload }}</button>
        </div>

        <script>
            window.addEventListener('offline', () => {
                document.getElementById('offline-ui').style.display = 'flex';
                const canvas = document.getElementById('gameCanvas');
                const ctx = canvas.getContext('2d');
                let score = 0; let pX = 150; let items = [];
                window.addEventListener('mousemove', e => { pX = e.clientX - canvas.offsetLeft - 25; });
                function play() {
                    ctx.clearRect(0,0,350,400); ctx.fillStyle = '#00f2fe'; ctx.fillRect(pX, 380, 50, 10);
                    if(Math.random() < 0.05) items.push({x: Math.random()*330, y:0, t: Math.random()>0.3 ? '🌱':'🗑️'});
                    items.forEach((it, i) => {
                        it.y += 4; ctx.font = "20px Arial"; ctx.fillText(it.t, it.x, it.y);
                        if(it.y > 380 && it.x > pX && it.x < pX + 50) {
                            score += it.t == '🌱' ? 10 : -10; items.splice(i, 1);
                            document.getElementById('scoreText').innerText = "{{ L.score }}: " + score;
                        }
                    });
                    requestAnimationFrame(play);
                }
                play();
            });
            window.addEventListener('online', () => location.reload());
        </script>
    </body>
    </html>
    """, data=data, ai_msg=ai_msg, lang=lang, L=L)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
