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
        <title>Neural Eco v3.7 | Global Portal</title>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            :root { --neon: #00f2fe; --bg: #010101; --glass: rgba(255,255,255,0.03); }
            body { background: var(--bg); color: #fff; font-family: 'Inter', sans-serif; margin: 0; overflow-x: hidden; }
            .glass { background: var(--glass); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.1); border-radius: 15px; padding: 20px; margin-bottom: 20px; }
            
            nav { display: flex; justify-content: space-between; align-items: center; padding: 15px 30px; background: #000; border-bottom: 1px solid var(--neon); position: sticky; top: 0; z-index: 100; }
            .lang-btn { background: none; border: 1px solid var(--neon); color: var(--neon); padding: 5px 10px; border-radius: 5px; cursor: pointer; margin-left: 5px; }
            .lang-btn.active { background: var(--neon); color: #000; }

            .container { max-width: 1200px; margin: auto; padding: 20px; }
            h2 { color: var(--neon); text-transform: uppercase; letter-spacing: 2px; text-align: center; }

            /* City Scroll */
            .city-container { display: flex; overflow-x: auto; gap: 10px; padding: 10px 0; border-bottom: 1px solid #222; }
            .city-card { min-width: 140px; padding: 10px; background: #111; border-radius: 10px; text-align: center; border: 1px solid #333; }

            /* Grid Layout */
            .main-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }

            /* AI Display */
            #ai-box { min-height: 200px; max-height: 350px; overflow-y: auto; background: #050505; padding: 15px; border-radius: 10px; border: 1px solid #222; font-size: 14px; line-height: 1.6; }
            
            /* Buttons */
            .btn { background: var(--neon); color: #000; border: none; padding: 10px 20px; border-radius: 8px; font-weight: bold; cursor: pointer; transition: 0.3s; }
            .btn:hover { opacity: 0.8; box-shadow: 0 0 15px var(--neon); }

            /* Map */
            .map-box { height: 400px; border-radius: 15px; overflow: hidden; border: 1px solid var(--neon); margin: 20px 0; }
            
            /* Game */
            .bin-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 15px; }
            .bin { border: 1px solid #444; padding: 10px; border-radius: 10px; cursor: pointer; text-align: center; }
            .bin:hover { border-color: var(--neon); background: rgba(0,242,254,0.1); }
        </style>
    </head>
    <body>

    <nav>
        <div style="font-weight: bold;">NEURAL ECO <span style="color:var(--neon)">AI</span></div>
        <div>
            <button class="lang-btn active" onclick="setL('uz', this)">UZ</button>
            <button class="lang-btn" onclick="setL('ru', this)">RU</button>
            <button class="lang-btn" onclick="setL('en', this)">EN</button>
        </div>
    </nav>

    <div class="container">
        <h2 id="l-mon">Global Monitoring</h2>
        <div class="city-container" id="city-list"></div>

        <div class="map-box">
            <iframe src="https://earth.nullschool.net/#current/wind/surface/level/orthographic=69.21,41.26,1000" style="width:100%; height:100%; border:none;"></iframe>
        </div>

        <div class="main-grid">
            <div class="glass">
                <h2 id="l-fore">Prognoz 2080</h2>
                <canvas id="fChart"></canvas>
            </div>
            <div class="glass">
                <h2 id="l-site">Eko Resurslar</h2>
                <div style="display:flex; flex-direction:column; gap:10px;">
                    <a href="https://earth911.com" target="_blank" style="color:#aaa; text-decoration:none; padding:10px; border:1px solid #222; border-radius:8px;">🌍 Earth911 Portal</a>
                    <a href="https://news.mongabay.com" target="_blank" style="color:#aaa; text-decoration:none; padding:10px; border:1px solid #222; border-radius:8px;">🍃 Mongabay News</a>
                    <a href="https://oceana.org" target="_blank" style="color:#aaa; text-decoration:none; padding:10px; border:1px solid #222; border-radius:8px;">🌊 Oceana Oceans</a>
                </div>
            </div>
        </div>

        <div class="glass" style="margin-top:20px;">
            <h2 id="l-ai">Eco AI Expert</h2>
            <div id="ai-box">Tayyor. Savolingizni bering...</div>
            <textarea id="ai-in" style="width:100%; background:#111; color:#fff; border:1px solid #333; padding:10px; border-radius:10px; margin: 10px 0;" rows="2"></textarea>
            <div style="display:flex; gap:10px;">
                <button class="btn" id="l-send" onclick="askAI()">Yuborish</button>
                <button class="btn" style="background:#ff4b2b; color:#fff;" onclick="exp('pdf')">PDF</button>
                <button class="btn" style="background:#2b55ff; color:#fff;" onclick="exp('word')">Word</button>
            </div>
        </div>

        <div class="main-grid">
            <div class="glass">
                <h2>🚀 NASA News</h2>
                <p style="font-size:13px; color:#888;">Global iqlim monitoringi va kosmos ma'lumotlari.</p>
                <a href="https://climate.nasa.gov" target="_blank" class="btn" style="display:block; text-align:center; text-decoration:none;">NASA Climate</a>
            </div>
            <div class="glass">
                <h2 id="l-game">Eco Game</h2>
                <div style="text-align:center">
                    <div id="g-emoji" style="font-size:40px;">🧴</div>
                    <div class="bin-grid">
                        <div class="bin" onclick="game('plastic')">PLASTIK</div>
                        <div class="bin" onclick="game('organic')">ORGANIK</div>
                        <div class="bin" onclick="game('paper')">QOG'OZ</div>
                        <div class="bin" onclick="game('hazard')">XAVFLI</div>
                    </div>
                    <p>Ball: <span id="score" style="color:var(--neon); font-weight:bold;">0</span></p>
                </div>
            </div>
        </div>
    </div>

    <script>
        const API = "AIzaSyCl-dBQmgQTJWgA5LR0Fy5Wiq7HLxaHK2Y";
        let lang = 'uz';
        let score = 0;
        let item = {e:"🧴", t:"plastic"};

        const txt = {
            uz: {mon:"Global Monitoring", fore:"Prognoz 2080", site:"Eko Resurslar", ai:"Eco AI Expert", game:"Eco O'yin", send:"Yuborish"},
            ru: {mon:"Мониторинг", fore:"Прогноз 2080", site:"Эко Ресурсы", ai:"Эко ИИ Эксперт", game:"Эко Игра", send:"Отправить"},
            en: {mon:"Monitoring", fore:"Forecast 2080", site:"Eco Resources", ai:"Eco AI Expert", game:"Eco Game", send:"Send"}
        };

        function setL(l, b) {
            lang = l;
            document.querySelectorAll('.lang-btn').forEach(x => x.classList.remove('active'));
            b.classList.add('active');
            document.getElementById('l-mon').innerText = txt[l].mon;
            document.getElementById('l-fore').innerText = txt[l].fore;
            document.getElementById('l-site').innerText = txt[l].site;
            document.getElementById('l-ai').innerText = txt[l].ai;
            document.getElementById('l-game').innerText = txt[l].game;
            document.getElementById('l-send').innerText = txt[l].send;
        }

        async function askAI() {
            const inp = document.getElementById('ai-in').value;
            const box = document.getElementById('ai-box');
            box.innerText = "...";
            try {
                const r = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${API}`, {
                    method:'POST',
                    body: JSON.stringify({contents:[{parts:[{text:`Javobni ${lang} tilida yoz: ${inp}`}]}]})
                });
                const d = await r.json();
                const s = d.candidates[0].content.parts[0].text;
                box.innerText = "";
                let i = 0;
                const t = setInterval(() => {
                    box.innerText += s.charAt(i); i++;
                    if(i>=s.length) clearInterval(t);
                    box.scrollTop = box.scrollHeight;
                }, 10);
            } catch(e) { box.innerText = "Xato: API ulanmadi."; }
        }

        const items = [{e:"🧴",t:"plastic"},{e:"🍎",t:"organic"},{e:"📰",t:"paper"},{e:"🔋",t:"hazard"}];
        function game(c) {
            if(c === item.t) { score+=10; } else { score-=5; }
            document.getElementById('score').innerText = score;
            item = items[Math.floor(Math.random()*items.length)];
            document.getElementById('g-emoji').innerText = item.e;
        }

        const cities = [
            {n:"Toshkent",lt:41.2,ln:69.2},{n:"Berlin",lt:52.5,ln:13.4},{n:"Pekin",lt:39.9,ln:116.4},{n:"Seul",lt:37.5,ln:126.9},
            {n:"Tokio",lt:35.6,ln:139.6},{n:"Moskva",lt:55.7,ln:37.6},{n:"Istanbul",lt:41.0,ln:28.9},{n:"Qohira",lt:30.0,ln:31.2},
            {n:"Rio",lt:-22.9,ln:-43.1},{n:"Bogota",lt:4.7,ln:-74.0},{n:"Washington",lt:38.8,ln:-77.0},{n:"Ottawa",lt:45.4,ln:-75.6}
        ];

        async function init() {
            const list = document.getElementById('city-list');
            for(let c of cities) {
                try {
                    const r = await fetch(`https://api.open-meteo.com/v1/forecast?latitude=${c.lt}&longitude=${c.ln}&current=temperature_2m`);
                    const d = await r.json();
                    list.innerHTML += `<div class="city-card"><b>${c.n}</b><br><span style="color:var(--neon)">${Math.round(d.current.temperature_2m)}°C</span></div>`;
                } catch(e) {}
            }
            new Chart(document.getElementById('fChart'), { type:'line', data:{labels:['2025','2050','2080'], datasets:[{label:'Temp Change', data:[1.2, 2.2, 3.4], borderColor:'#00f2fe'}]}, options:{plugins:{legend:{display:false}}} });
        }

        function exp(t) {
            const c = document.getElementById('ai-box').innerText;
            if(t==='pdf') { const d = new jspdf.jsPDF(); d.text(c, 10, 10); d.save("eco.pdf"); }
            else { const b = new Blob([c], {type:'application/msword'}); const a = document.createElement('a'); a.href=URL.createObjectURL(b); a.download="eco.doc"; a.click(); }
        }

        init();
    </script>
    </body>
    </html>
    """)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.getenv("PORT", 5000))
