import os
import requests
import time
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# UNIVERSAL AI LOGIC - MUKAMMAL VERSYIA
def get_ai_response(prompt, lang):
    # API Kalit (Agar yana band desa, bu Google limiti bilan bog'liq)
    api_key = "AIzaSyCl-dBQmgQTJWgA5LR0Fy5Wiq7HLxaHK2Y"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [{"text": f"Sen ECO-AI-WORLD tizimining universal yordamchisan. Foydalanuvchi savoliga {lang} tilida juda batafsil javob ber. Savol: {prompt}"}]
        }]
    }
    
    # 3 marta qayta urinish (Retry) mantiqi
    for attempt in range(3):
        try:
            response = requests.post(url, json=payload, timeout=25)
            data = response.json()
            if 'candidates' in data:
                return data['candidates'][0]['content']['parts'][0]['text']
            time.sleep(1) # Band bo'lsa 1 soniya kutish
        except:
            continue
    return "Hozirda AI xizmati band yoki limit tugagan. Iltimos, 1 daqiqadan so'ng urinib ko'ring."

@app.route('/')
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="uz">
    <head>
        <meta charset="UTF-8">
        <title>ECO-AI-WORLD | A.A Ataxojayev</title>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            :root { --neon: #00f2fe; --bg: #010101; --glass: rgba(255,255,255,0.05); }
            body { background: var(--bg); color: #fff; font-family: 'Segoe UI', sans-serif; margin: 0; }
            nav { display: flex; justify-content: space-between; align-items: center; padding: 10px 40px; background: #000; border-bottom: 2px solid var(--neon); position: sticky; top: 0; z-index: 1000; }
            .authors { border-left: 2px solid var(--neon); padding-left: 15px; font-size: 12px; color: #aaa; }
            .authors b { color: var(--neon); text-transform: uppercase; }
            .container { max-width: 1200px; margin: auto; padding: 20px; }
            .glass { background: var(--glass); backdrop-filter: blur(10px); border: 1px solid rgba(0,242,254,0.2); border-radius: 15px; padding: 20px; margin-bottom: 25px; }
            h2 { color: var(--neon); text-transform: uppercase; font-size: 18px; border-bottom: 1px solid #333; padding-bottom: 10px; }
            .city-scroll { display: flex; overflow-x: auto; gap: 15px; padding-bottom: 10px; }
            .city-card { min-width: 140px; background: #0a0a0a; border: 1px solid #333; padding: 15px; border-radius: 10px; text-align: center; }
            #ai-display { min-height: 250px; background: rgba(0,0,0,0.6); border-radius: 10px; padding: 20px; line-height: 1.6; overflow-y: auto; white-space: pre-wrap; border: 1px solid #222; }
            textarea { width: 100%; background: #111; border: 1px solid #444; color: #fff; padding: 15px; border-radius: 10px; margin-top: 15px; box-sizing: border-box; font-size: 16px; }
            .btn { background: var(--neon); color: #000; border: none; padding: 12px 25px; border-radius: 8px; font-weight: bold; cursor: pointer; transition: 0.3s; }
            .btn:hover { opacity: 0.8; box-shadow: 0 0 15px var(--neon); }
            .map-box { height: 400px; border-radius: 15px; overflow: hidden; border: 1px solid var(--neon); margin-bottom: 25px; }
            .lang-btn { background: none; border: 1px solid var(--neon); color: var(--neon); padding: 5px 10px; border-radius: 5px; cursor: pointer; margin-left: 5px; }
            .lang-btn.active { background: var(--neon); color: #000; }
        </style>
    </head>
    <body>
        <nav>
            <div style="font-weight: bold; font-size: 22px; color: var(--neon);">ECO-AI-WORLD</div>
            <div style="display: flex; align-items: center; gap: 20px;">
                <div class="authors">Muallif: <b>A.A Ataxojayev</b><br>Rahbar: <b>E.A Egamberdiev</b></div>
                <div>
                    <button class="lang-btn active" onclick="setL('uz', this)">UZ</button>
                    <button class="lang-btn" onclick="setL('ru', this)">RU</button>
                    <button class="lang-btn" onclick="setL('en', this)">EN</button>
                </div>
            </div>
        </nav>

        <div class="container">
            <h2>🏙️ Live Monitoring</h2>
            <div class="city-scroll" id="cities"></div>

            <div class="map-box">
                <iframe src="https://earth.nullschool.net/#current/wind/surface/level/orthographic=69.21,41.26,1200" style="width:100%; height:100%; border:none;"></iframe>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                <div class="glass">
                    <h2>📊 Carbon Analytics</h2>
                    <canvas id="carbChart"></canvas>
                </div>
                <div class="glass">
                    <h2>📚 Ilmiy Kutubxona</h2>
                    <a href="https://climate.nasa.gov" target="_blank" style="display:block; color:#ddd; margin-bottom:10px;">🚀 NASA Climate</a>
                    <a href="https://earth911.com" target="_blank" style="display:block; color:#ddd; margin-bottom:10px;">♻️ Recycling Center</a>
                    <a href="https://news.mongabay.com" target="_blank" style="display:block; color:#ddd;">🌳 Nature News</a>
                </div>
            </div>

            <div class="glass">
                <h2>🤖 ECO AI EXPERT</h2>
                <div id="ai-display">Savolingizni pastga yozing...</div>
                <textarea id="ai-input" placeholder="Masalan: Global isishning oqibatlari qanday?"></textarea>
                <div style="margin-top:15px; display:flex; gap:10px;">
                    <button class="btn" onclick="ask()">YUBORISH</button>
                    <button class="btn" style="background:#ff4b2b; color:#fff;" onclick="toPDF()">PDF EKSPORT</button>
                </div>
            </div>
        </div>

        <script>
            let L = 'uz';
            function setL(l, b) { L=l; document.querySelectorAll('.lang-btn').forEach(x=>x.classList.remove('active')); b.classList.add('active'); }

            async function getC() {
                const list = document.getElementById('cities');
                const pts = [{n:"Toshkent",lat:41.2,lon:69.2},{n:"London",lat:51.5,lon:-0.1},{n:"Tokio",lat:35.6,lon:139.6}];
                for(let p of pts) {
                    const r = await fetch(`https://api.open-meteo.com/v1/forecast?latitude=${p.lat}&longitude=${p.lon}&current=temperature_2m`);
                    const d = await r.json();
                    list.innerHTML += `<div class="city-card"><b>${p.n}</b><br><span style="color:var(--neon); font-size:20px;">${Math.round(d.current.temperature_2m)}°C</span></div>`;
                }
            }

            async function ask() {
                const i = document.getElementById('ai-input').value;
                const o = document.getElementById('ai-display');
                if(!i) return;
                o.innerText = "Tahlil qilinmoqda...";
                const res = await fetch('/get_ai', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({prompt: i, lang: L})
                });
                const data = await res.json();
                o.innerText = data.response;
            }

            function toPDF() {
                const doc = new jspdf.jsPDF();
                doc.text(document.getElementById('ai-display').innerText, 10, 10);
                doc.save("Report.pdf");
            }

            new Chart(document.getElementById('carbChart'), {
                type: 'doughnut',
                data: { labels: ['Sanoat', 'Transport', 'Uy-joy'], datasets: [{ data: [45, 30, 25], backgroundColor: ['#ff4b2b', '#00f2fe', '#ffcc00'] }] },
                options: { plugins: { legend: { labels: { color: '#fff' } } } }
            });
            getC();
        </script>
    </body>
    </html>
    """)

@app.route('/get_ai', methods=['POST'])
def ai_api():
    data = request.json
    return jsonify({"response": get_ai_response(data['prompt'], data['lang'])})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
