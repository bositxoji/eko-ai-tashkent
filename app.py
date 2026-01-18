import os
import requests
import google.generativeai as genai
from flask import Flask, render_template_string, request

app = Flask(__name__)

# --- KONFIGURATSIYA (API KEYLAR) ---
# Gemini API
GEMINI_API_KEY = "AIzaSyCl-dBQmgQTJWgA5LR0Fy5Wiq7HLxaHK2Y"
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel('gemini-1.5-flash')

# WAQI Token
WAQI_TOKEN = "68f561578e030386d0800b656708306059b02a46"

# --- MULTI-LANGUAGE DICTIONARY ---
TRANSLATIONS = {
    'uz': {
        'title': 'Neural Eco-Intelligence', 'search': 'Shahar qidiruvi...',
        'aqi': 'Havo Sifati', 'temp': 'Harorat', 'hum': 'Namlik', 'pm25': 'PM2.5 Chang',
        'ai_header': 'MULTI-AI CORE TAHLILI', 'vitality': 'Shaharning hayotiyligi',
        'offline': 'Internet uzildi! "Eco-Hero" o'yinini boshla.', 'score': 'Ball', 'reload': 'Yangilash'
    },
    'ru': {
        'title': 'Neural Eco-Intelligence', 'search': 'Поиск города...',
        'aqi': 'Качество воздуха', 'temp': 'Температура', 'hum': 'Влажность', 'pm25': 'Пыль PM2.5',
        'ai_header': 'МУЛЬТИ-АЙ АНАЛИЗ', 'vitality': 'Vitality города',
        'offline': 'Интернет отключен! Играй в "Eco-Hero".', 'score': 'Счет', 'reload': 'Обновить'
    },
    'en': {
        'title': 'Neural Eco-Intelligence', 'search': 'Search city...',
        'aqi': 'Air Quality', 'temp': 'Temperature', 'hum': 'Humidity', 'pm25': 'PM2.5 Particles',
        'ai_header': 'MULTI-AI CORE ANALYSIS', 'vitality': 'City Vitality',
        'offline': 'No internet! Play "Eco-Hero" game.', 'score': 'Score', 'reload': 'Reload'
    }
}

def get_multi_ai_analysis(city, data, lang):
    """ Gemini va Maxsus algoritm yordamida Multi-AI tahlil """
    prompt = f"Expert ecological analysis for {city}: AQI {data['aqi']}, Temp {data['temp']}C. Language: {lang}. Sharp 2-sentence summary and global context."
    try:
        response = gemini_model.generate_content(prompt)
        return response.text.strip()
    except:
        # Fallback AI Logic (Agar API ishlamasa, mahalliy mantiqiy AI javob beradi)
        if data['aqi'] < 50: return "Atmosphere is pristine. Excellent for outdoor activity."
        return "Atmospheric pressure is normal, but air filtration is advised."

@app.route('/')
def home():
    # 1. GPS/IP Orqali shaharni aniqlash
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    lang = request.args.get('lang', 'uz')
    city = request.args.get('city')
    
    if not city or "(AI DATA)" in city:
        try:
            geo_r = requests.get(f"http://ip-api.com/json/{user_ip}", timeout=3).json()
            city = geo_r.get('city', 'Tashkent')
        except: city = "Tashkent"

    L = TRANSLATIONS.get(lang, TRANSLATIONS['uz'])

    # 2. Havo ma'lumotlarini olish (Xatolardan himoyalangan)
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
        else: raise Exception("City not found")
    except:
        # Ma'lumot topilmasa xato emas, default ko'rsatkichlar (Safe Mode)
        data = {"aqi": 50, "temp": 22, "hum": 40, "pm25": 15, "city": f"{city.upper()} (SENSORS OFFLINE)"}

    ai_analysis = get_multi_ai_analysis(city, data, lang)

    # --- FRONTEND KOD (DESIGN + OFFLINE GAME) ---
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="{{ lang }}">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{{ L.title }}</title>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
        <style>
            :root { --neon: #00f2fe; --accent: #7d2ae8; --bg: #030508; --card: #0d1117; }
            body { background: var(--bg); color: #fff; font-family: 'Inter', sans-serif; margin: 0; overflow-x: hidden; }
            
            /* Neural Background Effect */
            .bg-glow { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: radial-gradient(circle at 50% 50%, #10213e 0%, transparent 60%); z-index: -1; }

            .app-container { max-width: 1000px; margin: 40px auto; padding: 20px; }
            
            /* Navbar */
            .nav { display: flex; justify-content: space-between; align-items: center; margin-bottom: 40px; }
            .search-box { background: var(--card); border: 1px solid #333; border-radius: 50px; padding: 5px 20px; display: flex; align-items: center; }
            .search-box input { background: none; border: none; color: #fff; padding: 10px; outline: none; width: 200px; }
            .lang-switch a { color: #555; text-decoration: none; margin-left: 15px; font-weight: bold; transition: 0.3s; }
            .lang-switch a.active { color: var(--neon); text-shadow: 0 0 10px var(--neon); }

            /* Main Interface */
            .hero-card { background: var(--card); border: 1px solid #222; border-radius: 40px; padding: 50px; position: relative; overflow: hidden; }
            .hero-card::after { content: ''; position: absolute; top: -50%; left: -50%; width: 200%; height: 200%; background: conic-gradient(from 0deg, transparent, var(--neon), transparent); animation: rotate 10s linear infinite; opacity: 0.05; z-index: 0; }
            @keyframes rotate { 100% { transform: rotate(360deg); } }
            
            .content-rel { position: relative; z-index: 1; }
            .city-tag { font-size: 14px; letter-spacing: 5px; color: var(--neon); font-weight: bold; }
            .aqi-display { font-size: 120px; font-weight: 900; margin: 20px 0; letter-spacing: -5px; }
            
            .ai-box { background: rgba(0, 242, 254, 0.03); border: 1px solid rgba(0, 242, 254, 0.1); border-radius: 25px; padding: 30px; margin: 30px 0; border-left: 5px solid var(--neon); }
            .ai-box i { color: var(--neon); margin-bottom: 10px; font-size: 24px; }
            
            .stats-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
            .stat-item { background: rgba(255,255,255,0.02); padding: 25px; border-radius: 25px; border: 1px solid #222; text-align: center; }
            .stat-item b { font-size: 28px; display: block; margin-top: 5px; color: var(--neon); }

            /* Offline Game Screen */
            #offline-layer { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: #000; z-index: 10000; flex-direction: column; align-items: center; justify-content: center; }
            canvas { border: 3px solid var(--neon); border-radius: 20px; background: #050505; box-shadow: 0 0 50px rgba(0,242,254,0.2); }
        </style>
    </head>
    <body>
        <div class="bg-glow"></div>
        
        <div class="app-container">
            <div class="nav">
                <form class="search-box" action="/">
                    <i class="fas fa-search"></i>
                    <input type="text" name="city" placeholder="{{ L.search }}">
                    <input type="hidden" name="lang" value="{{ lang }}">
                </form>
                <div class="lang-switch">
                    <a href="/?lang=uz&city={{ data.city }}" class="{% if lang=='uz' %}active{% endif %}">UZ</a>
                    <a href="/?lang=ru&city={{ data.city }}" class="{% if lang=='ru' %}active{% endif %}">RU</a>
                    <a href="/?lang=en&city={{ data.city }}" class="{% if lang=='en' %}active{% endif %}">EN</a>
                </div>
            </div>

            <div class="hero-card">
                <div class="content-rel">
                    <div class="city-tag"><i class="fas fa-microchip"></i> {{ data.city }}</div>
                    <div class="aqi-display">{{ data.aqi }}</div>
                    <div style="opacity: 0.5; font-size: 18px;">{{ L.aqi }} Index</div>

                    <div class="ai-box">
                        <i class="fas fa-brain"></i><br>
                        <strong>{{ L.ai_header }}:</strong>
                        <p style="font-size: 20px; font-style: italic; color: #ccc; margin-top: 15px;">"{{ ai_analysis }}"</p>
                    </div>

                    <div class="stats-grid">
                        <div class="stat-item"><i class="fas fa-thermometer-half"></i><br><small>{{ L.temp }}</small><b>{{ data.temp }}°C</b></div>
                        <div class="stat-item"><i class="fas fa-droplet"></i><br><small>{{ L.hum }}</small><b>{{ data.hum }}%</b></div>
                        <div class="stat-item"><i class="fas fa-wind"></i><br><small>{{ L.pm25 }}</small><b>{{ data.pm25 }}</b></div>
                    </div>
                </div>
            </div>
            
            <div style="margin-top: 30px; font-size: 12px; color: #444; text-align: center;">
                Developed by Ataxojayev Abdubositxoja | Supervisor: E. Egamberdiev
            </div>
        </div>

        <div id="offline-layer">
            <h1 style="color:var(--neon)">{{ L.offline }}</h1>
            <canvas id="ecoGame" width="400" height="500"></canvas>
            <h2 id="scoreDisplay" style="margin-top:20px;">{{ L.score }}: 0</h2>
            <button onclick="location.reload()" style="background:var(--neon); border:none; padding:15px 40px; border-radius:50px; font-weight:bold; cursor:pointer;">{{ L.reload }}</button>
        </div>

        <script>
            // Offline Detection
            window.addEventListener('offline', () => {
                document.getElementById('offline-layer').style.display = 'flex';
                startEcoGame();
            });
            window.addEventListener('online', () => location.reload());

            // ECO-HERO GAME logic
            function startEcoGame() {
                const canvas = document.getElementById('ecoGame');
                const ctx = canvas.getContext('2d');
                let score = 0;
                let player = { x: 175, w: 50 };
                let items = [];

                window.addEventListener('mousemove', e => {
                    let rect = canvas.getBoundingClientRect();
                    player.x = e.clientX - rect.left - 25;
                });

                function loop() {
                    ctx.clearRect(0,0,400,500);
                    // Draw Player
                    ctx.fillStyle = '#00f2fe';
                    ctx.fillRect(player.x, 470, 50, 10);

                    // Spawn items
                    if(Math.random() < 0.05) {
                        items.push({x: Math.random()*380, y:0, type: Math.random()>0.3 ? '🌱' : '🗑️'});
                    }

                    items.forEach((it, i) => {
                        it.y += 5;
                        ctx.font = "24px Arial";
                        ctx.fillText(it.type, it.x, it.y);

                        // Collision
                        if(it.y > 470 && it.x > player.x && it.x < player.x + 50) {
                            score += (it.type == '🌱' ? 10 : -10);
                            items.splice(i, 1);
                            document.getElementById('scoreDisplay').innerText = "{{ L.score }}: " + score;
                        }
                    });
                    requestAnimationFrame(loop);
                }
                loop();
            }
        </script>
    </body>
    </html>
    """, data=data, ai_analysis=ai_analysis, lang=lang, L=L)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
