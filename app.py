from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="uz">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Eco AI | Global Intelligence Portal</title>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            :root { --neon: #00f2fe; --bg: #050505; --card: #111; }
            body { background: var(--bg); color: #fff; font-family: 'Segoe UI', sans-serif; margin: 0; scroll-behavior: smooth; }
            
            /* Navigatsiya */
            nav { background: rgba(17,17,17,0.95); padding: 15px; display: flex; justify-content: center; gap: 20px; position: sticky; top: 0; z-index: 1000; border-bottom: 1px solid var(--neon); }
            nav a { color: #fff; text-decoration: none; font-size: 12px; font-weight: bold; letter-spacing: 1px; transition: 0.3s; }
            nav a:hover { color: var(--neon); }

            .container { max-width: 1200px; margin: auto; padding: 20px; }
            section { padding: 60px 0; border-bottom: 1px solid #222; }
            h2 { color: var(--neon); text-align: center; text-transform: uppercase; letter-spacing: 4px; margin-bottom: 40px; }

            /* 1-Vazifa: Shaharlar Monitoringi */
            .city-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; }
            .city-card { background: var(--card); padding: 20px; border-radius: 15px; border: 1px solid #222; text-align: center; }
            .city-card h4 { margin: 0; color: var(--neon); }
            .city-temp { font-size: 28px; font-weight: bold; margin: 10px 0; }

            /* Futprint va Prognoz */
            .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 30px; }
            .info-box { background: var(--card); padding: 25px; border-radius: 20px; border-left: 5px solid var(--neon); }

            /* Eco AI bo'limi */
            .ai-window { background: var(--card); border-radius: 25px; padding: 30px; border: 1px solid #333; }
            #ai-display { min-height: 150px; background: #0a0a0a; padding: 15px; border-radius: 10px; margin-bottom: 15px; font-size: 14px; color: #ccc; }
            textarea { width: 100%; background: #222; border: 1px solid #444; color: #fff; padding: 10px; border-radius: 10px; margin-bottom: 10px; }

            /* Eco O'yin */
            .game-area { background: linear-gradient(135deg, #001f3f, #000); padding: 40px; border-radius: 30px; text-align: center; }
            .trash-bin { display: inline-block; padding: 20px; margin: 10px; border: 2px dashed var(--neon); cursor: pointer; border-radius: 10px; }

            /* Linklar bo'limi */
            .link-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
            .link-card { background: #1a1a1a; padding: 20px; border-radius: 15px; text-decoration: none; color: #fff; text-align: center; transition: 0.3s; }
            .link-card:hover { background: var(--neon); color: #000; }
        </style>
    </head>
    <body>

    <nav>
        <a href="#monitor">SHAHARLAR</a>
        <a href="#future">PROGNOZ 2080</a>
        <a href="#carbon">FOOTPRINT</a>
        <a href="#ai-expert">ECO AI</a>
        <a href="#nasa">NASA</a>
        <a href="#games">O'YINLAR</a>
    </nav>

    <div class="container">
        
        <section id="monitor">
            <h2>🌍 GLOBAL MONITORING (Real-Time)</h2>
            <div class="city-grid" id="city-list">
                </div>
        </section>

        <section id="future">
            <h2>📈 BASHORATLAR VA CARBON FOOTPRINT</h2>
            <div class="grid-2">
                <div class="info-box">
                    <h3>Karbon Footprint (Global)</h3>
                    <p>Yillik Emissiya: <b style="color:red">37.5 Billion Ton</b></p>
                    <p>Asosiy manba: Energiya (73.2%)</p>
                    <canvas id="carbonChart"></canvas>
                </div>
                <div class="info-box">
                    <h3>2025-2080 Prognoz</h3>
                    <p style="font-size:13px">Siyosiy-tarixiy tahlil: 2080-yilga borib, global harorat +3.2°C ga ko'tarilishi bashorat qilinmoqda. Bu iqtisodiy migratsiyani 40% ga oshiradi.</p>
                    <canvas id="forecastChart"></canvas>
                </div>
            </div>
        </section>

        <section id="ai-expert">
            <h2>🤖 ECO AI EXPERT (Hisobot Tayyorlash)</h2>
            <div class="ai-window">
                <div id="ai-display">Ekologik muammo haqida so'rang (masalan: "Karbon izini kamaytirish yo'llari")...</div>
                <textarea id="ai-input" rows="3" placeholder="Savolingizni kiriting..."></textarea>
                <div style="display:flex; gap:10px">
                    <button onclick="askEcoAI()" style="background:var(--neon); color:#000; border:none; padding:12px 25px; border-radius:10px; cursor:pointer; font-weight:bold">TAHLIL QILISH</button>
                    <button onclick="exportPDF()" style="background:#ff4b2b; color:white; border:none; padding:12px; border-radius:10px; cursor:pointer">PDF YUKLASH</button>
                    <button onclick="exportWord()" style="background:#2b55ff; color:white; border:none; padding:12px; border-radius:10px; cursor:pointer">WORD YUKLASH</button>
                </div>
            </div>
        </section>

        <section id="nasa">
            <h2>🚀 NASA & KOINOT BILIMLARI</h2>
            <div class="link-grid">
                <a href="https://www.nasa.gov" target="_blank" class="link-card">NASA Rasmiy</a>
                <a href="https://climate.nasa.gov" target="_blank" class="link-card">Iqlim Monitoringi</a>
                <a href="https://earthobservatory.nasa.gov" target="_blank" class="link-card">Yer Kuzatuvlari</a>
            </div>
            <iframe src="https://earth.nullschool.net/#current/wind/surface/level/orthographic=69.21,41.26,1000" style="width:100%; height:400px; border-radius:20px; margin-top:30px; border:none;"></iframe>
        </section>

        <section id="games">
            <h2>🎮 ECO-MADANIYAT O'YINLARI</h2>
            <div class="game-area">
                <p id="game-item" style="font-size:60px">🧴</p>
                <p>Ushbu chiqindini qayerga saralaysiz?</p>
                <div class="trash-bin" onclick="checkGame('p')">PET (Plastik)</div>
                <div class="trash-bin" onclick="checkGame('o')">ORGANIK</div>
                <div class="trash-bin" onclick="checkGame('q')">QOGO'Z</div>
                <p>Ball: <b id="score">0</b></p>
            </div>
        </section>

        <section>
            <h2>🌱 FOYDALI RESURSLAR</h2>
            <div class="link-grid">
                <a href="https://earth911.com" target="_blank" class="link-card">Earth911</a>
                <a href="https://news.mongabay.com" target="_blank" class="link-card">Mongabay</a>
                <a href="https://oceana.org" target="_blank" class="link-card">Oceana</a>
            </div>
        </section>
    </div>

    <script>
        const GEMINI_KEY = "AIzaSyCl-dBQmgQTJWgA5LR0Fy5Wiq7HLxaHK2Y";

        // 1. Shaharlar yuklanishi
        const cities = [
            {n:"Toshkent", lt:41.2, ln:69.2}, {n:"Berlin", lt:52.5, ln:13.4},
            {n:"Pekin", lt:39.9, ln:116.4}, {n:"Seul", lt:37.5, ln:126.9},
            {n:"Tokio", lt:35.6, ln:139.6}, {n:"Moskva", lt:55.7, ln:37.6},
            {n:"Istanbul", lt:41.0, ln:28.9}, {n:"Qohira", lt:30.0, ln:31.2},
            {n:"Rio", lt:-22.9, ln:-43.1}, {n:"Bogota", lt:4.7, ln:-74.0},
            {n:"Washington", lt:38.8, ln:-77.0}, {n:"Ottawa", lt:45.4, ln:-75.6}
        ];

        async function initCities() {
            const list = document.getElementById('city-list');
            for(let c of cities) {
                const r = await fetch(`https://api.open-meteo.com/v1/forecast?latitude=${c.lt}&longitude=${c.ln}&current=temperature_2m`);
                const d = await r.json();
                list.innerHTML += `<div class="city-card"><h4>${c.n}</h4><div class="city-temp">${Math.round(d.current.temperature_2m)}°C</div></div>`;
            }
        }

        // 2. Grafiklarni chizish
        const fCtx = document.getElementById('forecastChart').getContext('2d');
        new Chart(fCtx, {
            type: 'line',
            data: {
                labels: ['2025','2035','2045','2055','2065','2075','2080'],
                datasets: [{label: 'Harorat (°C)', data:[1.2, 1.6, 2.0, 2.5, 2.9, 3.1, 3.2], borderColor:'#00f2fe'}]
            }
        });

        // 3. AI Expert Funksiyasi
        async function askEcoAI() {
            const q = document.getElementById('ai-input').value;
            const disp = document.getElementById('ai-display');
            disp.innerText = "Sun'iy intellekt hisobot tayyorlamoqda...";
            
            const res = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${GEMINI_KEY}`, {
                method:'POST',
                body: JSON.stringify({contents:[{parts:[{text: q + ". O'zbek tilida ilmiy, batafsil hisobot yoz."}]}]})
            });
            const data = await res.json();
            disp.innerText = data.candidates[0].content.parts[0].text;
        }

        // PDF va Word Export
        function exportPDF() {
            const { jsPDF } = window.jspdf;
            const doc = new jsPDF();
            doc.setFontSize(10);
            const text = document.getElementById('ai-display').innerText;
            const splitText = doc.splitTextToSize(text, 180);
            doc.text(splitText, 10, 10);
            doc.save("eco-report.pdf");
        }

        function exportWord() {
            const content = document.getElementById('ai-display').innerText;
            const blob = new Blob(['\\ufeff', content], {type: 'application/msword'});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url; a.download = 'eco-report.doc'; a.click();
        }

        // 4. Eco Game Mantiqi
        let score = 0;
        function checkGame(type) {
            score += 10;
            document.getElementById('score').innerText = score;
            const items = ["📦", "🔋", "🍎", "📰", "🥤"];
            document.getElementById('game-item').innerText = items[Math.floor(Math.random()*items.length)];
        }

        initCities();
    </script>
    </body>
    </html>
    """)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
