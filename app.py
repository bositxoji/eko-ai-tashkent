import os
from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="uz">
    <head>
        <meta charset="UTF-8">
        <title>ECO-AI-WORLD | Global Portal</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            :root { --neon: #00f2fe; --bg: #000; }
            body { background: var(--bg); color: #fff; font-family: 'Segoe UI', sans-serif; margin: 0; }
            nav { display: flex; justify-content: space-between; padding: 10px 40px; border-bottom: 2px solid var(--neon); background: #080808; position: sticky; top: 0; z-index: 1000; }
            .container { max-width: 1400px; margin: auto; padding: 20px; }
            
            /* 12 SHAHAR */
            .city-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(110px, 1fr)); gap: 10px; margin-bottom: 20px; }
            .city-card { background: #111; border: 1px solid #333; padding: 10px; border-radius: 8px; text-align: center; border-bottom: 2px solid var(--neon); }
            .temp { color: var(--neon); font-size: 20px; font-weight: bold; }

            .main-layout { display: grid; grid-template-columns: 2fr 1fr; gap: 20px; }
            .box { background: rgba(255,255,255,0.03); border: 1px solid #222; border-radius: 15px; padding: 20px; }
            
            /* NASA & LIBRARY */
            .lib-item { display: block; background: #0a0a0a; padding: 15px; margin-bottom: 10px; border-radius: 10px; text-decoration: none; color: #fff; border-left: 4px solid var(--neon); transition: 0.3s; }
            .lib-item:hover { background: #151515; transform: scale(1.02); }

            iframe { width: 100%; height: 400px; border-radius: 10px; border: 1px solid var(--neon); }
            #ai-screen { height: 250px; background: #050505; border: 1px solid #333; padding: 15px; border-radius: 10px; overflow-y: auto; color: var(--neon); margin-bottom: 10px; }
            textarea { width: 100%; background: #111; border: 1px solid #444; color: #fff; padding: 10px; border-radius: 8px; box-sizing: border-box; }
            .btn { background: var(--neon); color: #000; border: none; padding: 10px 20px; border-radius: 5px; font-weight: bold; cursor: pointer; margin-top: 10px; width: 100%; }
        </style>
    </head>
    <body>
        <nav>
            <div style="font-size: 22px; font-weight: bold; color: var(--neon);">ECO-AI-WORLD</div>
            <div style="font-size: 11px; text-align: right;">Muallif: <b>A.A Ataxojayev</b><br>Rahbar: <b>E.A Egamberdiev</b></div>
        </nav>

        <div class="container">
            <div class="city-grid" id="city-box"></div>

            <div class="main-layout">
                <div class="left">
                    <div class="box" style="margin-bottom: 20px;">
                        <h3>🌍 NASA GLOBAL MONITORING (LIVE)</h3>
                        <iframe src="https://earth.nullschool.net/#current/wind/surface/level/orthographic=69.21,41.26,1200"></iframe>
                    </div>
                    <div class="box">
                        <h3>🤖 SMART ECO-EXPERT (OFFLINE AI)</h3>
                        <div id="ai-screen">Tizim tayyor. Ekologiya haqida savol bering...</div>
                        <textarea id="ai-input" placeholder="Savol: Havoning kirlanishi, daryolar..."></textarea>
                        <button class="btn" onclick="ask()">SAVOLNI YUBORISH</button>
                    </div>
                </div>

                <div class="right">
                    <div class="box" style="margin-bottom: 20px;">
                        <h3>📚 NASA ILMIY KUTUBXONA</h3>
                        <a href="https://climate.nasa.gov" target="_blank" class="lib-item">🚀 NASA Climate News</a>
                        <a href="https://www.worldwildlife.org" target="_blank" class="lib-item">🐼 WWF Resources</a>
                        <a href="https://earth911.com" target="_blank" class="lib-item">♻️ Recycling Guide</a>
                        <a href="https://news.mongabay.com" target="_blank" class="lib-item">🌳 Forest Watch</a>
                    </div>
                    <div class="box">
                        <h3>📊 EMISSIYA TAHLILI</h3>
                        <canvas id="ecoChart"></canvas>
                        <div style="margin-top: 15px; padding: 10px; border: 1px dashed var(--neon); text-align: center;">
                            <b>ECO GAME SCORE: <span id="score">0</span></b><br>
                            <button class="btn" onclick="document.getElementById('score').innerText = parseInt(document.getElementById('score').innerText)+10">SARALASH (+10)</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <script>
            // 12 SHAHAR GENERATSIYASI
            const cList = ["Toshkent", "London", "Nyu-York", "Tokio", "Pekin", "Berlin", "Moskva", "Parij", "Dubay", "Seul", "Rim", "Istanbul"];
            const b = document.getElementById('city-box');
            cList.forEach(c => {
                let t = Math.floor(Math.random() * 20) + 10;
                b.innerHTML += `<div class="city-card"><b>${c}</b><div class="temp">${t}°C</div></div>`;
            });

            // SMART OFFLINE AI LOGIC
            function ask() {
                const i = document.getElementById('ai-input').value.toLowerCase();
                const s = document.getElementById('ai-screen');
                let r = "NASA ma'lumotlar bazasidan qidirilmoqda... Bu masala bo'yicha NASA Climate portalida batafsil tadqiqotlar mavjud.";
                
                if(i.includes("daryo") || i.includes("suv")) r = "Suv resurslarining kirlanishi NASA'ning GRACE sun'iy yo'ldoshlari orqali nazorat qilinadi. Asosiy muammo - sanoat chiqindilari.";
                if(i.includes("havo") || i.includes("iflos")) r = "Global havo sifati (AQI) hozirda rekord darajadagi karbonat angidrid (420ppm) miqdorini ko'rsatmoqda.";
                if(i.includes("salom")) r = "Assalomu alaykum! ECO-AI-WORLD universal yordamchisi xizmatga tayyor.";
                
                s.innerText = r;
                document.getElementById('ai-input').value = "";
            }

            // CHART
            new Chart(document.getElementById('ecoChart'), {
                type: 'doughnut',
                data: {
                    labels: ['Sanoat', 'Transport', 'Turar-joy'],
                    datasets: [{ data: [45, 30, 25], backgroundColor: ['#ff4b2b', '#00f2fe', '#ffcc00'] }]
                },
                options: { plugins: { legend: { labels: { color: '#fff' } } } }
            });
        </script>
    </body>
    </html>
    """)

if __name__ == "__main__":
    # Render portini to'g'ri aniqlash
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
