import os
import requests
import google.generativeai as genai
from flask import Flask, render_template_string, request

app = Flask(__name__)

# --- ELITA KONFIGURATSIYA ---
# Sizning Gemini API kalitingiz
genai.configure(api_key="AIzaSyCl-dBQmgQTJWgA5LR0Fy5Wiq7HLxaHK2Y")
model = genai.GenerativeModel('gemini-1.5-flash')

WAQI_TOKEN = "68f561578e030386d0800b656708306059b02a46"

# --- MULTI-LANGUAGE DICTIONARY ---
TRANSLATIONS = {
    'uz': {
        'title': 'Global Eko-Intellekt',
        'aqi': 'Havo Sifati', 'temp': 'Harorat', 'hum': 'Namlik', 'pm25': 'Chang (PM2.5)',
        'ai_analysis': 'GEMINI AI TAHLILI', 'loading': 'Aniqlanmoqda...',
        'author': 'Muallif', 'supervisor': 'Ilmiy rahbar'
    },
    'ru': {
        'title': 'Глобальный Эко-Интеллект',
        'aqi': 'Качество воздуха', 'temp': 'Температура', 'hum': 'Влажность', 'pm25': 'Пыль (PM2.5)',
        'ai_analysis': 'АНАЛИЗ GEMINI AI', 'loading': 'Определение...',
        'author': 'Автор', 'supervisor': 'Научный руководитель'
    },
    'en': {
        'title': 'Global Eco-Intelligence',
        'aqi': 'Air Quality', 'temp': 'Temperature', 'hum': 'Humidity', 'pm25': 'Particles (PM2.5)',
        'ai_analysis': 'GEMINI AI ANALYSIS', 'loading': 'Detecting...',
        'author': 'Author', 'supervisor': 'Supervisor'
    }
}

def get_pro_ai_analysis(city, data, lang):
    """ Gemini AI orqali har bir til uchun alohida chuqur tahlil """
    prompt = f"As an environmental expert, analyze this for {city}: AQI is {data['aqi']}, Temp {data['temp']}°C, Humidity {data['hum']}%. Give a sharp, professional 2-sentence summary and health advice in {lang} language."
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except:
        return "AI system is calibrating. Please wait."

@app.route('/')
def home():
    # 1. GPS/IP orqali foydalanuvchi shahrini avtomatik aniqlash
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    auto_city = "tashkent"
    try:
        # IP orqali shaharni topish (Free GeoAPI)
        geo_r = requests.get(f"http://ip-api.com/json/{user_ip}", timeout=3).json()
        if geo_r['status'] == 'success':
            auto_city = geo_r['city']
    except: pass

    city = request.args.get('city', auto_city)
    lang = request.args.get('lang', 'uz')
    L = TRANSLATIONS.get(lang, TRANSLATIONS['uz'])

    # 2. Havo ma'lumotlarini olish
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
            ai_comment = get_pro_ai_analysis(city, data, lang)
        else: raise Exception("API Error")
    except:
        data = {"aqi": "--", "temp": "--", "hum": "--", "pm25": "--", "city": city.upper() + " (NOT FOUND)"}
        ai_comment = "Error connecting to global stations."

    return render_template_string("""
    <!DOCTYPE html>
    <html lang="{{ lang }}">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{{ L.title }}</title>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
        <style>
            :root { --neon: #00f2fe; --bg: #050505; --card: #111111; }
            body { background: var(--bg); color: #fff; font-family: 'Inter', sans-serif; margin: 0; padding: 20px; }
            .container { max-width: 1000px; margin: 0 auto; }
            
            /* Navbar */
            .nav { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }
            .lang-switch a { color: #888; text-decoration: none; margin-left: 15px; font-weight: bold; transition: 0.3s; }
            .lang-switch a.active { color: var(--neon); text-shadow: 0 0 10px var(--neon); }

            /* Main Card */
            .main-card { background: var(--card); border: 1px solid #222; border-radius: 30px; padding: 40px; position: relative; overflow: hidden; }
            .main-card::before { content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 5px; background: linear-gradient(90deg, transparent, var(--neon), transparent); }
            
            .city-label { text-transform: uppercase; letter-spacing: 3px; font-size: 14px; color: var(--neon); opacity: 0.8; }
            .aqi-box { display: flex; align-items: baseline; gap: 20px; margin: 20px 0; }
            .aqi-num { font-size: 90px; font-weight: 900; line-height: 1; }
            
            /* AI Terminal */
            .ai-box { background: rgba(0, 242, 254, 0.05); border-radius: 20px; padding: 25px; border-left: 5px solid var(--neon); margin: 30px 0; }
            .ai-box i { color: var(--neon); margin-bottom: 10px; display: block; }
            
            /* Grid */
            .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; }
            .stat { background: #1a1a1a; padding: 20px; border-radius: 20px; border: 1px solid #222; }
            .stat i { color: #555; margin-bottom: 10px; }
            .stat-val { display: block; font-size: 24px; font-weight: bold; }

            .footer { margin-top: 50px; display: flex; justify-content: space-between; font-size: 12px; color: #444; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="nav">
                <div style="font-weight: 800; font-size: 20px; letter-spacing: -1px;">GLOBAL <span style="color:var(--neon)">ECO-AI</span></div>
                <div class="lang-switch">
                    <a href="/?lang=uz&city={{ data.city|lower }}" class="{% if lang=='uz' %}active{% endif %}">UZ</a>
                    <a href="/?lang=ru&city={{ data.city|lower }}" class="{% if lang=='ru' %}active{% endif %}">RU</a>
                    <a href="/?lang=en&city={{ data.city|lower }}" class="{% if lang=='en' %}active{% endif %}">EN</a>
                </div>
            </div>

            <div class="main-card">
                <span class="city-label"><i class="fas fa-location-dot"></i> {{ data.city }}</span>
                <div class="aqi-box">
                    <span class="aqi-num">{{ data.aqi }}</span>
                    <span style="font-size: 20px; opacity: 0.5;">{{ L.aqi }}</span>
                </div>

                <div class="ai-box">
                    <i class="fas fa-robot"></i>
                    <strong>{{ L.ai_analysis }}:</strong><br>
                    <p style="font-style: italic; font-size: 18px; margin-top: 10px;">"{{ ai_comment }}"</p>
                </div>

                <div class="grid">
                    <div class="stat">
                        <i class="fas fa-temperature-high"></i>
                        <span style="display:block; font-size:12px; opacity:0.6;">{{ L.temp }}</span>
                        <span class="stat-val">{{ data.temp }}°C</span>
                    </div>
                    <div class="stat">
                        <i class="fas fa-droplet"></i>
                        <span style="display:block; font-size:12px; opacity:0.6;">{{ L.hum }}</span>
                        <span class="stat-val">{{ data.hum }}%</span>
                    </div>
                    <div class="stat">
                        <i class="fas fa-wind"></i>
                        <span style="display:block; font-size:12px; opacity:0.6;">{{ L.pm25 }}</span>
                        <span class="stat-val">{{ data.pm25 }}</span>
                    </div>
                </div>
            </div>

            <div class="footer">
                <div>{{ L.author }}: <b>Ataxojayev Abdubositxoja</b></div>
                <div>{{ L.supervisor }}: <b>Egamberdiev E.</b></div>
            </div>
        </div>
    </body>
    </html>
    """, data=data, ai_comment=ai_comment, lang=lang, L=L)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
