import os
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# --- ULTRA EXPERT LOGIC (OFFLINE AI) ---
def get_expert_analysis(prompt):
    p = prompt.lower()
    
    # 1. Kengaytirilgan bilimlar bazasi
    knowledge = {
        "daryo": "Tahlil: Daryolar ifloslanishi global muammo. NASA ma'lumotlariga ko'ra, Orol dengizi havzasi va Amudaryo sathi 2026-yilda rekord darajada pasayishi kutilmoqda. Yechim: Suvni tejovchi sug'orish va sanoat filtrlari.",
        "havo": "Havo monitoringi: PM2.5 zarralari miqdori me'yordan 12 barobar yuqori. Asosiy manba - ko'mir yoqish va transport. 2080-yilga borib global harorat yana 2-3 darajaga oshishi mumkin.",
        "chiqindi": "Statistika: Dunyodagi plastikning atigi 9% qayta ishlanadi. NASA va WWF ma'lumotlariga ko'ra, 2050-yilga borib okeanlarda baliqdan ko'ra plastik ko'proq bo'ladi.",
        "nasa": "NASA Resurslari: NASA'ning Landsat sun'iy yo'ldoshlari global o'rmonlar qisqarishini real vaqtda kuzatmoqda. NASA Climate portalida 'Global Warming' eng xavfli nuqtaga yetganini ko'rsatadi.",
        "salom": "Assalomu alaykum! ECO-AI-WORLD expert tizimi onlayn. Sizga global iqlim, daryolar va NASA monitoringi bo'yicha ma'lumot bera olaman.",
        "energiya": "Energetika tahlili: Qayta tiklanuvchi energiya (quyosh, shamol) ulushi 2026-yilda global miqyosda 30% dan oshishi bashorat qilinmoqda."
    }

    # 2. Kalit so'z bo'yicha aqlli qidiruv
    for key, value in knowledge.items():
        if key in p:
            return value
    
    # 3. Agar kalit so'z topilmasa, mantiqiy xulosa chiqarish
    return "Tahliliy xulosa: Ushbu masala ekologik barqarorlik va 'Yashil iqtisodiyot' uchun juda muhim. NASA va xalqaro tashkilotlar ushbu yo'nalishda monitoring ishlarini kuchaytirmoqda."

@app.route('/')
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="uz">
    <head>
        <meta charset="UTF-8">
        <title>ECO-AI-WORLD v11.0 | Advanced Portal</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            :root { --neon: #00f2fe; --bg: #000; }
            body { background: var(--bg); color: #fff; font-family: 'Segoe UI', sans-serif; margin: 0; }
            nav { display: flex; justify-content: space-between; padding: 10px 40px; border-bottom: 2px solid var(--neon); background: #080808; }
            .container { max-width: 1300px; margin: auto; padding: 20px; }
            
            /* 12 TA SHAHAR */
            .city-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(100px, 1fr)); gap: 10px; margin-bottom: 20px; }
            .city-card { background: #111; border: 1px solid #333; padding: 10px; border-radius: 8px; text-align: center; font-size: 13px; border-bottom: 2px solid var(--neon); }
            
            .main-grid { display: grid; grid-template-columns: 2fr 1fr; gap: 20px; }
            .box { background: rgba(255,255,255,0.03); border: 1px solid #222; border-radius: 15px; padding: 20px; }
            
            iframe { width: 100%; height: 400px; border-radius: 12px; border: 1px solid var(--neon); }
            #display { height: 280px; background: #050505; border-radius: 10px; padding: 15px; overflow-y: auto; color: var(--neon); font-size: 15px; border: 1px solid #333; margin-bottom: 15px; }
            
            .lib-link { display: block; background: #111; padding: 12px; margin-bottom: 10px; border-radius: 8px; text-decoration: none; color: #fff; border-left: 4px solid var(--neon); }
            input { width: 100%; background: #111; border: 1px solid #444; color: #fff; padding: 15px; border-radius: 8px; box-sizing: border-box; }
            .btn { background: var(--neon); color: #000; border: none; padding: 12px 25px; border-radius: 8px; font-weight: bold; cursor: pointer; margin-top: 10px; width: 100%; }
        </style>
    </head>
    <body>
        <nav>
            <div style="font-size: 22px; font-weight: bold; color: var(--neon);">ECO-AI-WORLD v11.0</div>
            <div style="font-size: 11px; text-align: right;">A.A Ataxojayev | E.A Egamberdiev</div>
        </nav>

        <div class="container">
            <div class="city-grid" id="cities"></div>

            <div class="main-grid">
                <div class="left">
                    <div class="box" style="margin-bottom: 20px;">
                        <h3>🌍 NASA GLOBAL MONITORING</h3>
                        <iframe src="https://earth.nullschool.net/#current/wind/surface/level/orthographic=64.44,41.48,1500"></iframe>
                    </div>
                    <div class="box">
                        <h3>🤖 EXPERT AI ANALYSIS (NASA DATA)</h3>
                        <div id="display">Salom! Men NASA bazasi asosida ishlovchi ekologik tahlilchiman. Savol yozing...</div>
                        <input type="text" id="userInput" placeholder="Masalan: Daryolar kirlanishi tahlili...">
                        <button class="btn" onclick="ask()">TAHLILNI BOSHLASH</button>
                    </div>
                </div>

                <div class="right">
                    <div class="box" style="margin-bottom: 20px;">
                        <h3>📚 NASA ILMIY KUTUBXONA</h3>
                        <a href="https://climate.nasa.gov" target="_blank" class="lib-link">🚀 NASA Climate News</a>
                        <a href="https://www.worldwildlife.org" target="_blank" class="lib-link">🐼 WWF Global Reports</a>
                        <a href="https://earth911.com" target="_blank" class="lib-link">♻️ Eco Recycling Center</a>
                        <a href="https://news.mongabay.com" target="_blank" class="lib-link">🌳 Forest Watch 2026</a>
                    </div>
                    <div class="box">
                        <h3>📊 EMISSIYA PROGNOZI</h3>
                        <canvas id="myChart"></canvas>
                        <div style="margin-top: 15px; text-align: center; border: 1px dashed var(--neon); padding: 10px;">
                            <b>ECO GAME BALL: <span id="score">0</span></b><br>
                            <button class="btn" style="padding: 5px;" onclick="addScore()">SARALASH</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <script>
            // 12 TA SHAHAR
            const list = ["Toshkent", "London", "Nyu-York", "Tokio", "Pekin", "Berlin", "Moskva", "Parij", "Dubay", "Seul", "Rim", "Istanbul"];
            const cDiv = document.getElementById('cities');
            list.forEach(c => {
                let t = Math.floor(Math.random() * 20) + 10;
                cDiv.innerHTML += `<div class="city-card"><b>${c}</b><br><span style="color:var(--neon)">${t}°C</span></div>`;
            });

            // AI ANALYSIS
            function ask() {
                const input = document.getElementById('userInput').value;
                const disp = document.getElementById('display');
                if(!input) return;

                fetch('/expert_talk', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({prompt: input})
                })
                .then(res => res.json())
                .then(data => {
                    disp.innerHTML += `<div style="color:#fff; margin-top:10px;">> ${input}</div>`;
                    disp.innerHTML += `<div style="margin-top:5px;">🤖 ${data.response}</div>`;
                    disp.scrollTop = disp.scrollHeight;
                });
                document.getElementById('userInput').value = '';
            }

            // SCORE
            let s = 0; function addScore() { s+=10; document.getElementById('score').innerText = s; }

            // CHART
            new Chart(document.getElementById('myChart'), {
                type: 'line',
                data: {
                    labels: ['2025', '2050', '2080'],
                    datasets: [{ label: 'Harorat (°C)', data: [1.1, 2.2, 3.5], borderColor: '#00f2fe', tension: 0.3 }]
                },
                options: { plugins: { legend: { labels: { color: '#fff' } } }, scales: { y: { ticks: { color: '#fff' } }, x: { ticks: { color: '#fff' } } } }
            });
        </script>
    </body>
    </html>
    """)

@app.route('/expert_talk', methods=['POST'])
def expert_talk():
    data = request.json
    response = get_expert_analysis(data['prompt'])
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
