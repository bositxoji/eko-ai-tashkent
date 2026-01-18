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
        <title>Neural Eco v4.0 | Advanced Intelligence</title>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            :root { --neon: #00f2fe; --bg: #010101; --glass: rgba(255,255,255,0.03); --border: rgba(0, 242, 254, 0.3); }
            body { background: var(--bg); color: #fff; font-family: 'Inter', sans-serif; margin: 0; scroll-behavior: smooth; }
            .glass { background: var(--glass); backdrop-filter: blur(15px); border: 1px solid var(--border); border-radius: 20px; padding: 25px; margin-bottom: 25px; transition: 0.3s; }
            .glass:hover { border-color: var(--neon); box-shadow: 0 0 15px var(--border); }
            
            nav { display: flex; justify-content: space-between; align-items: center; padding: 15px 40px; background: rgba(0,0,0,0.9); position: sticky; top: 0; z-index: 1000; border-bottom: 1px solid var(--neon); }
            .lang-btn { background: none; border: 1px solid var(--neon); color: var(--neon); padding: 5px 12px; cursor: pointer; border-radius: 8px; font-weight: bold; margin-left: 10px; }
            .lang-btn.active { background: var(--neon); color: #000; }

            .container { max-width: 1300px; margin: auto; padding: 20px; }
            h2 { color: var(--neon); text-transform: uppercase; letter-spacing: 3px; text-align: center; margin-bottom: 30px; }

            /* Grid Layouts */
            .grid-3 { display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 25px; }
            .city-scroll { display: flex; overflow-x: auto; gap: 15px; padding: 15px 0; border-bottom: 1px solid #222; }
            .city-card { min-width: 150px; text-align: center; padding: 15px; border-radius: 12px; background: #0a0a0a; border: 1px solid #222; }

            /* Carbon Footprint & Library */
            .info-card { background: rgba(0,0,0,0.5); border-left: 4px solid var(--neon); padding: 15px; margin-bottom: 10px; border-radius: 0 10px 10px 0; }
            .article-link { display: block; color: #ddd; text-decoration: none; padding: 12px; border-bottom: 1px solid #333; transition: 0.3s; }
            .article-link:hover { color: var(--neon); background: rgba(255,255,255,0.05); }

            /* AI Section */
            #ai-out { min-height: 250px; background: #050505; border: 1px solid #333; border-radius: 15px; padding: 20px; margin-bottom: 15px; line-height: 1.8; overflow-y: auto; }
            textarea { width: 100%; background: #111; border: 1px solid #444; color: #fff; padding: 15px; border-radius: 12px; outline: none; box-sizing: border-box; }

            .btn { background: var(--neon); color: #000; border: none; padding: 12px 25px; border-radius: 10px; font-weight: bold; cursor: pointer; }
            .btn-danger { background: #ff4b2b; color: white; }
            .btn-blue { background: #2b55ff; color: white; }

            /* Map Box */
            .map-box { height: 450px; border-radius: 20px; overflow: hidden; border: 1px solid var(--neon); margin: 30px 0; }
        </style>
    </head>
    <body>

    <nav>
        <div style="font-weight: bold; font-size: 20px;">NEURAL ECO <span style="color:var(--neon)">PRO</span></div>
        <div>
            <button class="lang-btn active" onclick="chLang('uz', this)">UZ</button>
            <button class="lang-btn" onclick="chLang('ru', this)">RU</button>
            <button class="lang-btn" onclick="chLang('en', this)">EN</button>
        </div>
    </nav>

    <div class="container">
        
        <section>
            <h2 id="l-mon">Global City Monitor</h2>
            <div class="city-scroll" id="city-list"></div>
        </section>

        <div class="map-box">
            <iframe src="https://earth.nullschool.net/#current/wind/surface/level/orthographic=69.21,41.26,1000" style="width:100%; height:100%; border:none;"></iframe>
        </div>

        <div class="grid-3">
            <div class="glass">
                <h2 id="l-carb">Carbon Footprint</h2>
                <canvas id="carbChart" style="max-height: 200px;"></canvas>
                <div class="info-card" style="margin-top:20px">
                    <p style="font-size:14px;" id="l-cinfo">Sizning hududingizda o'rtacha karbon chiqindisi: <b>4.5 tonna/yil</b></p>
                </div>
            </div>

            <div class="glass">
                <h2 id="l-lib">Maqolalar Kutubxonasi</h2>
                <div style="max-height: 300px; overflow-y: auto;">
                    <a href="https://earth911.com" target="_blank" class="article-link">🌍 Global Eko-Risk Monitoring 2026</a>
                    <a href="https://news.mongabay.com" target="_blank" class="article-link">🍃 O'rmonlar qisqarishi tahlili</a>
                    <a href="https://oceana.org" target="_blank" class="article-link">🌊 Okeanlardagi plastik xavfi</a>
                    <a href="#" class="article-link">📑 Iqlim o'zgarishi va iqtisodiy risklar</a>
                </div>
            </div>

            <div class="glass">
                <h2 id="l-fore">2080 Iqlim Prognozi</h2>
                <canvas id="fChart"></canvas>
            </div>
        </div>

        <div class="glass" style="margin-top:30px">
            <h2 id="l-ai">Eco AI Expert (ChatGPT Mode)</h2>
            <div id="ai-out">Savolingizni bering...</div>
            <textarea id="ai-in" rows="3" placeholder="Masalan: Ekologik risklarni qanday kamaytirish mumkin?"></textarea>
            <div style="display:flex; gap:10px; margin-top:15px">
                <button class="btn" id="l-send" onclick="askAI()">Yuborish</button>
                <button class="btn btn-danger" onclick="exp('pdf')">PDF</button>
                <button class="btn btn-blue" onclick="exp('doc')">Word</button>
            </div>
        </div>

        <div class="grid-3">
            <div class="glass" style="border-color:#0033a0">
                <h2>🚀 NASA Intelligence</h2>
                <a href="https://climate.nasa.gov" target="_blank" class="article-link">NASA Global Climate News</a>
                <a href="https://www.nasa.gov" target="_blank" class="btn" style="display:block; text-align:center; margin-top:10px; background:#0033a0; color:white;">NASA Portali</a>
            </div>
            <div class="glass">
                <h2 id="l-game">Eco Game</h2>
                <div style="text-align:center">
                    <div id="g-emoji" style="font-size:50px; margin-bottom:10px;">🧴</div>
                    <div style="display:grid; grid-template-columns: 1fr 1fr; gap:10px">
                        <div style="border:1px solid #444; padding:10px; cursor:pointer" onclick="game('plastic')">PLASTIK</div>
                        <div style="border:1px solid #444; padding:10px; cursor:pointer" onclick="game('organic')">ORGANIK</div>
                    </div>
                    <p style="margin-top:15px">Ball: <span id="score" style="color:var(--neon); font-weight:bold">0</span></p>
                </div>
            </div>
        </div>
    </div>

    <script>
        const API = "AIzaSyCl-dBQmgQTJWgA5LR0Fy5Wiq7HLxaHK2Y";
        let lang = 'uz';
        let score = 0;
        let item = {e:"🧴", t:"plastic"};

        const dic = {
            uz: {mon:"Global Monitoring", carb:"Karbon Footprint", lib:"Maqolalar Kutubxonasi", fore:"2080 Prognoz", ai:"Eco AI Expert", game:"Eko O'yin", send:"Yuborish"},
            ru: {mon:"Глобальный Мониторинг", carb:"Углеродный след", lib:"Библиотека статей", fore:"Прогноз 2080", ai:"Эко ИИ Эксперт", game:"Эко Игра", send:"Отправить"},
            en: {mon:"Global Monitoring", carb:"Carbon Footprint", lib:"Article Library", fore:"2080 Forecast", ai:"Eco AI Expert", game:"Eco Game", send:"Send"}
        };

        function chLang(l, b) {
            lang = l;
            document.querySelectorAll('.lang-btn').forEach(x => x.classList.remove('active'));
            b.classList.add('active');
            Object.keys(dic[l]).forEach(k => {
                const el = document.getElementById('l-'+k);
                if(el) el.innerText = dic[l][k];
            });
        }

        async function askAI() {
            const inp = document.getElementById('ai-in').value;
            const out = document.getElementById('ai-out');
            out.innerText = "AI tahlil qilmoqda...";
            try {
                const r = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${API}`, {
                    method:'POST',
                    body: JSON.stringify({contents:[{parts:[{text:`Javobni ${lang} tilida, ilmiy va batafsil yoz: ${inp}`}]}]})
                });
                const d = await r.json();
                const s = d.candidates[0].content.parts[0].text;
                out.innerText = "";
                let i = 0;
                const t = setInterval(() => {
                    out.innerText += s.charAt(i); i++;
                    if(i>=s.length) clearInterval(t);
                    out.scrollTop = out.scrollHeight;
                }, 10);
            } catch(e) { out.innerText = "Xato: API ulanishda muammo. Iltimos, Render-da 'requests' kutubxonasi borligini tekshiring."; }
        }

        function game(c) {
            if(c === item.t) score+=10; else score-=5;
            document.getElementById('score').innerText = score;
            const trash = [{e:"🧴",t:"plastic"},{e:"🍎",t:"organic"},{e:"📰",t:"paper"}];
            item = trash[Math.floor(Math.random()*trash.length)];
            document.getElementById('g-emoji').innerText = item.e;
        }

        const cities = [
            {n:"Toshkent",lt:41.2,ln:69.2},{n:"Berlin",lt:52.5,ln:13.4},{n:"Pekin",lt:39.9,ln:116.4},{n:"Seul",lt:37.5,ln:126.9},
            {n:"Tokio",lt:35.6,ln:139.6},{n:"Moskva",lt:55.7,ln:37.6},{n:"Istanbul",lt:41.0,ln:28.9},{n:"Rio",lt:-22.9,ln:-43.1}
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
            new Chart(document.getElementById('fChart'), { type:'line', data:{labels:['2025','2050','2080'], datasets:[{label:'Temp Change', data:[1.1, 2.3, 3.5], borderColor:'#00f2fe'}]}, options:{plugins:{legend:{display:false}}, scales:{y:{ticks:{color:'#fff'}}}} });
            new Chart(document.getElementById('carbChart'), { type:'doughnut', data:{labels:['Transport','Oziq-ovqat','Energiya'], datasets:[{data:[30,25,45], backgroundColor:['#ff4b2b','#00f2fe','#ffcc00']}]}, options:{plugins:{legend:{position:'bottom', labels:{color:'#fff'}}}} });
        }

        function exp(t) {
            const c = document.getElementById('ai-out').innerText;
            if(t==='pdf') { const d = new jspdf.jsPDF(); d.text(c, 10, 10); d.save("eco_report.pdf"); }
            else { const b = new Blob([c], {type:'application/msword'}); const a = document.createElement('a'); a.href=URL.createObjectURL(b); a.download="report.doc"; a.click(); }
        }

        init();
    </script>
    </body>
    </html>
    """)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.getenv("PORT", 5000))
