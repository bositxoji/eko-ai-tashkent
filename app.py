import os
import requests
import google.generativeai as genai
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# --- ELITA KONFIGURATSIYA ---
GEMINI_API_KEY = "AIzaSyCl-dBQmgQTJWgA5LR0Fy5Wiq7HLxaHK2Y"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

WAQI_TOKEN = "68f561578e030386d0800b656708306059b02a46"

# --- MULTI-LANGUAGE SYSTEM ---
LANG_DATA = {
    'uz': {
        'title': 'Global Eko-Intellekt', 'search': 'Shahar qidirish...', 'aqi': 'Havo Sifati',
        'temp': 'Harorat', 'hum': 'Namlik', 'pm25': 'Chang (PM2.5)', 'ai_label': 'AI EKSPERT TAHLILI',
        'offline_msg': 'Internet uzildi! Zerikmaslik uchun o'yin o'yna:', 'score': 'Ball', 'btn': 'Yangilash'
    },
    'ru': {
        'title': 'Глобальный Эко-Интеллект', 'search': 'Поиск города...', 'aqi': 'Качество воздуха',
        'temp': 'Температура', 'hum': 'Влажность', 'pm25': 'Пыль (PM2.5)', 'ai_label': 'АНАЛИЗ ЭКСПЕРТА AI',
        'offline_msg': 'Интернет пропал! Играй, пока ждешь:', 'score': 'Счет', 'btn': 'Обновить'
    },
    'en': {
        'title': 'Global Eco-Intelligence', 'search': 'Search city...', 'aqi': 'Air Quality',
        'temp': 'Temperature', 'hum': 'Humidity', 'pm25': 'Particles (PM2.5)', 'ai_label': 'AI EXPERT ANALYSIS',
        'offline_msg': 'Internet disconnected! Play this game:', 'score': 'Score', 'btn': 'Reload'
    }
}

def get_ai_insight(city, data, lang):
    """ Gemini AI orqali har bir til uchun individual tahlil """
    prompt = f"""
    Sen Global Eco-AI tizimisan. 
    Shahar: {city}, AQI: {data['aqi']}, Temp: {data['temp']}°C, Namlik: {data['hum']}%.
    Topshiriq: Ushbu ma'lumotlarni {lang} tilida professional va qisqa (2 jumla) tahlil qil.
    Maslahat va kelajakdagi ehtimoliy o'zgarishni ayt.
    """
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except:
        return "AI is processing environmental data..."

@app.route('/')
def index():
    # 1. IP orqali joylashuvni aniqlash
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    lang = request.args.get('lang', 'uz')
    city = request.args.get('city')

    if not city:
        try:
            geo = requests.get(f"http://ip-api.com/json/{user_ip}", timeout=3).json()
            city = geo.get('city', 'Tashkent')
        except: city = 'Tashkent'

    L = LANG_DATA.get(lang, LANG_DATA['uz'])

    # 2. Havo sifatini olish
    try:
        r = requests.get(f"https://api.waqi.info/feed/{city}/?token={WAQI_TOKEN}", timeout=7).json()
        if r['status'] == 'ok':
            res = r['data']
            data = {
                "aqi": res['aqi'],
                "temp": res['iaqi'].get('t', {}).get('v', 0),
                "hum": res['iaqi'].get('h', {}).get('v', 0),
                "pm25": res['iaqi'].get('pm25', {}).get('v', 0),
                "city": city.upper()
            }
            ai_comment = get_ai_insight(city, data, lang)
        else: raise Exception()
    except:
        data = {"aqi": "--", "temp": "--", "hum": "--", "pm25": "--", "city": city.upper() + " (OFFLINE)"}
        ai_comment = "Tizim stansiya bilan bog'lana olmadi."

    # --- FRONTEND (CSS, HTML, JS) ---
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="{{ lang }}">
    <head>
        <meta charset="UTF-8">
        <title>{{ L.title }}</title>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
        <style>
            :root { --neon: #00f2fe; --glass: rgba(255, 255, 255, 0.03); --bg: #05070a; }
            body { background: var(--bg); color: #fff; font-family: 'Inter', sans-serif; margin: 0; transition: 0.5s; }
            .main-ui { max-width: 900px; margin: 40px auto; padding: 20px; }
            
            .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }
            .search-bar { background: var(--glass); border: 1px solid #333; padding: 10px 20px; border-radius: 50px; display: flex; align-items: center; }
            .search-bar input { background: none; border: none; color: #fff; padding-left: 10px; outline: none; }
            
            .lang-switch a { color: #888; text-decoration: none; margin-left: 10px; font-weight: bold; }
            .lang-switch a.active { color: var(--neon); text-shadow: 0 0 10px var(--neon); }

            .hero-card { background: linear-gradient(135deg, #111, #080808); border: 1px solid #222; border-radius: 30px; padding: 40px; box-shadow: 0 30px 60px rgba(0,0,0,0.5); position: relative; }
            .city-name { font-size: 14px; text-transform: uppercase; letter-spacing: 4px; color: var(--neon); }
            .aqi-num { font-size: 100px; font-weight: 900; margin: 10px 0; background: linear-gradient(to right, #fff, var(--neon)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }

            .ai-terminal { background: rgba(0,242,254,0.05); border-left: 4px solid var(--neon); padding: 25px; border-radius: 0 20px 20px 0; margin: 30px 0; font-size: 18px; line-height: 1.6; }

            .stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
            .s-card { background: var(--glass); padding: 20px; border-radius: 20px; border: 1px solid #222; text-align: center; }
            .s-card i { color: #555; margin-bottom: 10px; }

            /* Offline Game UI */
            #offline-screen { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: #000; z-index: 10000; flex-direction: column; align-items: center; justify-content: center; }
            canvas { border: 2px solid var(--neon); border-radius: 15px; background: #050505; }
        </style>
    </head>
    <body>
        <div class="main-ui">
            <div class="header">
                <form class="search-bar" action="/">
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
                <div class="city-name"><i class="fas fa-tower-broadcast"></i> {{ data.city }}</div>
                <div class="aqi-num">{{ data.aqi }}</div>
                <div style="opacity: 0.5;">{{ L.aqi }}</div>

                <div class="ai-terminal">
                    <i class="fas fa-brain" style="color: var(--neon);"></i> <strong style="color:var(--neon)">{{ L.ai_label }}</strong><br>
                    "{{ ai_comment }}"
                </div>

                <div class="stats">
                    <div class="s-card"><i class="fas fa-temperature-three-quarters"></i><br><small>{{ L.temp }}</small><br><strong>{{ data.temp }}°C</strong></div>
                    <div class="s-card"><i class="fas fa-droplet"></i><br><small>{{ L.hum }}</small><br><strong>{{ data.hum }}%</strong></div>
                    <div class="s-card"><i class="fas fa-wind"></i><br><small>{{ L.pm25 }}</small><br><strong>{{ data.pm25 }}</strong></div>
                </div>
            </div>
        </div>

        <div id="offline-screen">
            <h2 style="color:var(--neon)">{{ L.offline_msg }}</h2>
            <canvas id="ecoGame" width="400" height="400"></canvas>
            <div id="scoreBox" style="font-size: 24px; margin-top: 10px;">{{ L.score }}: 0</div>
            <button onclick="location.reload()" style="margin-top:20px; padding:10px 40px; border-radius:50px; background:var(--neon); border:none; font-weight:bold;">{{ L.btn }}</button>
        </div>

        <script>
            // Offline Detection
            window.addEventListener('offline', () => {
                document.getElementById('offline-screen').style.display = 'flex';
                initGame();
            });
            window.addEventListener('online', () => location.reload());

            function initGame() {
                const canvas = document.getElementById('ecoGame');
                const ctx = canvas.getContext('2d');
                let score = 0;
                let basket = { x: 175, w: 50 };
                let items = [];

                document.addEventListener('mousemove', e => {
                    let rect = canvas.getBoundingClientRect();
                    basket.x = e.clientX - rect.left - 25;
                });

                function update() {
                    ctx.clearRect(0,0,400,400);
                    ctx.fillStyle = '#00f2fe';
                    ctx.fillRect(basket.x, 380, basket.w, 10);

                    if(Math.random() < 0.05) items.push({x: Math.random()*380, y: 0, t: Math.random()>0.5 ? '🌱' : '🗑️'});

                    items.forEach((it, i) => {
                        it.y += 4;
                        ctx.font = "24px Arial";
                        ctx.fillText(it.t, it.x, it.y);

                        if(it.y > 380 && it.x > basket.x && it.x < basket.x + basket.w) {
                            score += it.t == '🌱' ? 10 : -10;
                            items.splice(i, 1);
                            document.getElementById('scoreBox').innerText = "{{ L.score }}: " + score;
                        }
                    });
                    requestAnimationFrame(update);
                }
                update();
            }
        </script>
    </body>
    </html>
    """, data=data, ai_comment=ai_comment, lang=lang, L=L)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
