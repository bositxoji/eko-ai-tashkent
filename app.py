import os
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# --- EKOLOGIK BILIMLAR MARKAZI (OFFLINE DATABASE) ---
KNOWLEDGE_BASE = {
    "suv": "Suv tanqisligi: 2026-yilga kelib Markaziy Osiyoda suv resurslari 15% ga kamayishi kutilmoqda. NASA ma'lumotlariga ko'ra, Amudaryo sathi tarixiy minimumga yaqinlashmoqda.",
    "havo": "Havo sifati (AQI): Dunyo aholisining 90% me'yordan ortiq ifloslangan havodan nafas oladi. Sanoat filtrlarisiz CO2 miqdori 420 ppm dan oshib ketdi.",
    "daryo": "Daryolar ifloslanishi: Dunyo daryolariga har yili 8 million tonna plastik tushadi. Bu ekotizimning zanjirli buzilishiga olib kelmoqda.",
    "nasa": "NASA Monitoring: Sun'iy yo'ldoshlar orqali muzliklarning erishi va o'rmonlar qisqarishi real vaqtda kuzatilmoqda. NASA 'Earth Now' tizimi buni tasdiqlaydi.",
    "chiqindi": "Chiqindi tahlili: Bir dona plastik shisha tabiatda 450 yil davomida parchalanadi. Qayta ishlash darajasi hozirda global miqyosda atigi 14-16% ni tashkil etadi.",
    "energiya": "Yashil texnologiya: Quyosh panellari va shamol generatorlari emissiyani 75% ga kamaytirish imkonini beradi. Bu 2030-yilgi global maqsad hisoblanadi.",
    "muammo": "Ekologik muammolar: Global isish, biomuhitning yo'qolishi va okeanlarning kislotalanishi insoniyat oldidagi eng katta uchta xavfdir."
}

def get_smart_response(user_input):
    text = user_input.lower()
    found_info = []
    
    # Savolni chuqur tahlil qilish
    for key in KNOWLEDGE_BASE:
        if key in text:
            found_info.append(KNOWLEDGE_BASE[key])
    
    if found_info:
        return " | ".join(found_info)
    
    # Agar kalit so'z topilmasa, mantiqiy xulosa berish
    return "Tahliliy xulosa: Ushbu masala ekologik barqarorlik uchun juda muhim. NASA va WWF ma'lumotlariga ko'ra, har qanday kichik o'zgarish global iqlimga zanjir kabi ta'sir qiladi."

@app.route('/')
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="uz">
    <head>
        <meta charset="UTF-8">
        <title>ECO-AI-WORLD | NEURAL ENGINE</title>
        <style>
            :root { --neon: #00f2fe; --bg: #0d1117; }
            body { background: var(--bg); color: #c9d1d9; font-family: 'Segoe UI', sans-serif; margin: 0; display: flex; flex-direction: column; height: 100vh; }
            header { background: #161b22; padding: 15px 50px; border-bottom: 2px solid var(--neon); display: flex; justify-content: space-between; align-items: center; }
            .main { flex: 1; display: flex; gap: 20px; padding: 20px; max-width: 1400px; margin: auto; width: 100%; box-sizing: border-box; }
            .chat-box { flex: 2; background: #0d1117; border: 1px solid #30363d; border-radius: 12px; display: flex; flex-direction: column; overflow: hidden; }
            #display { flex: 1; padding: 20px; overflow-y: auto; font-size: 16px; line-height: 1.6; border-bottom: 1px solid #30363d; }
            .input-area { padding: 15px; background: #161b22; display: flex; gap: 10px; }
            input { flex: 1; background: #0d1117; border: 1px solid #30363d; color: #fff; padding: 12px; border-radius: 6px; outline: none; }
            button { background: var(--neon); color: #000; border: none; padding: 12px 25px; border-radius: 6px; font-weight: bold; cursor: pointer; }
            .sidebar { flex: 1; display: flex; flex-direction: column; gap: 20px; }
            .card { background: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 15px; }
            .city-tag { display: inline-block; background: #21262d; padding: 5px 10px; border-radius: 4px; margin: 3px; font-size: 12px; border-left: 2px solid var(--neon); }
        </style>
    </head>
    <body>
        <header>
            <div style="font-size: 24px; font-weight: bold; color: var(--neon);">NEURAL ECO PRO</div>
            <div style="font-size: 12px; text-align: right;">Mualif: A.A Ataxojayev<br>Rahbar: E.A Egamberdiev</div>
        </header>

        <div class="main">
            <div class="chat-box">
                <div id="display"><b>> Tizim tayyor.</b> Ekologiya, daryolar, NASA monitoringi yoki global isish bo'yicha savol bering...</div>
                <div class="input-area">
                    <input type="text" id="userInput" placeholder="Savol yozing (masalan: daryolar kirlanishi tahlili)..." onkeypress="if(event.key==='Enter') ask()">
                    <button onclick="ask()">TAHLIL</button>
                </div>
            </div>

            <div class="sidebar">
                <div class="card">
                    <h3 style="color: var(--neon); margin-top: 0;">🏙️ 12 TA SHAHAR</h3>
                    <div id="cities"></div>
                </div>
                <div class="card">
                    <h3 style="color: var(--neon); margin-top: 0;">📚 NASA RESURSLARI</h3>
                    <ul style="padding-left: 20px; font-size: 13px;">
                        <li><a href="https://climate.nasa.gov" style="color: #58a6ff;">NASA Climate Now</a></li>
                        <li><a href="https://earth.nullschool.net" style="color: #58a6ff;">Global Wind Map</a></li>
                    </ul>
                </div>
            </div>
        </div>

        <script>
            const cities = ["Toshkent", "London", "Nyu-York", "Tokio", "Pekin", "Berlin", "Moskva", "Parij", "Dubay", "Seul", "Rim", "Istanbul"];
            const cBox = document.getElementById('cities');
            cities.forEach(c => {
                cBox.innerHTML += `<span class="city-tag">${c}: ${Math.floor(Math.random()*25)+5}°C</span>`;
            });

            function ask() {
                const inp = document.getElementById('userInput');
                const disp = document.getElementById('display');
                if(!inp.value) return;

                const text = inp.value;
                disp.innerHTML += `<div style="color: #8b949e; margin-top: 15px;">> Savol: ${text}</div>`;
                
                fetch('/get_ai', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({prompt: text})
                })
                .then(res => res.json())
                .then(data => {
                    disp.innerHTML += `<div style="color: #58a6ff; margin-top: 5px;">🤖 AI: ${data.response}</div>`;
                    disp.scrollTop = disp.scrollHeight;
                });
                inp.value = '';
            }
        </script>
    </body>
    </html>
    """)

@app.route('/get_ai', methods=['POST'])
def ai_logic():
    data = request.json
    res = get_smart_response(data['prompt'])
    return jsonify({"response": res})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
