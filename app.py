from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="uz">
    <head>
        <meta charset="UTF-8">
        <title>Eco-Intelligence 3.0 | Future Portal</title>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            :root { --neon: #00f2fe; --danger: #ff4b2b; --bg: #030303; --glass: rgba(255,255,255,0.05); }
            body { background: var(--bg); color: #fff; font-family: 'Inter', sans-serif; margin: 0; overflow-x: hidden; }
            
            /* Glassmorphism Design */
            .glass { background: var(--glass); backdrop-filter: blur(15px); border: 1px solid rgba(255,255,255,0.1); border-radius: 20px; padding: 25px; }
            
            nav { display: flex; justify-content: space-between; align-items: center; padding: 15px 40px; background: rgba(0,0,0,0.8); position: sticky; top: 0; z-index: 1000; border-bottom: 1px solid var(--neon); }
            .lang-btn { background: none; border: 1px solid var(--neon); color: var(--neon); padding: 5px 10px; cursor: pointer; border-radius: 5px; }

            .container { max-width: 1300px; margin: auto; padding: 20px; }
            h2 { color: var(--neon); text-transform: uppercase; letter-spacing: 5px; text-shadow: 0 0 10px var(--neon); text-align: center; }

            /* AI Chat Simulation */
            .ai-container { min-height: 400px; display: flex; flex-direction: column; gap: 15px; }
            #ai-display { flex-grow: 1; font-size: 16px; line-height: 1.6; color: #e0e0e0; overflow-y: auto; max-height: 400px; padding-right: 10px; border-bottom: 1px solid #333; }
            .typing { border-right: 2px solid var(--neon); animation: blink 0.7s infinite; }
            @keyframes blink { 50% { border-color: transparent; } }

            /* Grid Layouts */
            .city-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 15px; }
            .game-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 30px; }

            /* Game Logic */
            .trash-item { font-size: 80px; transition: 0.3s; }
            .bin { padding: 20px; border: 2px solid #333; border-radius: 15px; cursor: pointer; transition: 0.3s; text-align: center; font-weight: bold; }
            .bin:hover { border-color: var(--neon); background: rgba(0,242,254,0.1); }
            .bin.correct { border-color: #0f0; background: rgba(0,255,0,0.1); }
            .bin.wrong { border-color: #f00; background: rgba(255,0,0,0.1); }

            button { background: var(--neon); color: #000; border: none; padding: 12px 20px; border-radius: 10px; font-weight: bold; cursor: pointer; }
        </style>
    </head>
    <body>

    <nav>
        <div style="font-weight: bold; color: var(--neon);">NEURAL ECO v3.0</div>
        <div style="display:flex; gap:10px;">
            <button class="lang-btn" onclick="setLang('uz')">UZ</button>
            <button class="lang-btn" onclick="setLang('en')">EN</button>
            <button class="lang-btn" onclick="setLang('ru')">RU</button>
        </div>
    </nav>

    <div class="container">
        
        <section>
            <h2 id="t-monitor">SHAHARLAR MONITORINGI</h2>
            <div class="city-grid" id="city-list"></div>
        </section>

        <section class="game-grid">
            <div class="glass">
                <h2 id="t-forecast">2080 PROGNOZ</h2>
                <canvas id="forecastChart"></canvas>
            </div>
            <div class="glass">
                <h2 id="t-game">ECO MADANIYAT O'YINI</h2>
                <div style="text-align:center">
                    <div id="item-emoji" class="trash-item">🧴</div>
                    <p id="t-sort">Qaysi idishga tashlaysiz?</p>
                    <div style="display:grid; grid-template-columns: 1fr 1fr; gap:10px">
                        <div class="bin" onclick="checkAnswer('plastic')">PLASTIK</div>
                        <div class="bin" onclick="checkAnswer('organic')">ORGANIK</div>
                        <div class="bin" onclick="checkAnswer('paper')">QOG'OZ</div>
                        <div class="bin" onclick="checkAnswer('hazard')">XAVFLI</div>
                    </div>
                    <h3>Ball: <span id="score">0</span></h3>
                </div>
            </div>
        </section>

        <section class="glass" style="margin-top:40px">
            <h2 id="t-ai">ECO AI CHATBOT (STREAMING)</h2>
            <div class="ai-container">
                <div id="ai-display"></div>
                <div style="display:flex; gap:10px">
                    <textarea id="ai-input" style="flex-grow:1; background:#111; border:1px solid #333; color:#fff; border-radius:10px; padding:10px;" placeholder="Savolingizni bering..."></textarea>
                    <button onclick="askAI()">YUBORISH</button>
                </div>
                <div style="display:flex; gap:10px; margin-top:10px">
                    <button onclick="download('pdf')" style="background:#ff4b2b; color:#fff;">PDF</button>
                    <button onclick="download('doc')" style="background:#2b55ff; color:#fff;">WORD</button>
                </div>
            </div>
        </section>

    </div>

    <script>
        const GEMINI_KEY = "AIzaSyCl-dBQmgQTJWgA5LR0Fy5Wiq7HLxaHK2Y";
        let currentLang = 'uz';
        let score = 0;
        let currentItem = { emoji: "🧴", type: "plastic" };

        const translations = {
            uz: { monitor: "SHAHARLAR MONITORINGI", forecast: "2080 PROGNOZ", game: "ECO O'YIN", ai: "ECO AI TAHLIL", sort: "Qaysi idishga tashlaysiz?" },
            en: { monitor: "CITY MONITORING", forecast: "2080 FORECAST", game: "ECO GAME", ai: "ECO AI ANALYSIS", sort: "Where to dispose?" },
            ru: { monitor: "МОНИТОРИНГ ГОРОДОВ", forecast: "ПРОГНОЗ 2080", game: "ЭКО ИГРА", ai: "ЭКО ИИ АНАЛИЗ", sort: "Куда выбросить?" }
        };

        function setLang(l) {
            currentLang = l;
            document.getElementById('t-monitor').innerText = translations[l].monitor;
            document.getElementById('t-forecast').innerText = translations[l].forecast;
            document.getElementById('t-game').innerText = translations[l].game;
            document.getElementById('t-ai').innerText = translations[l].ai;
            document.getElementById('t-sort').innerText = translations[l].sort;
        }

        // 1. AI Streaming (ChatGPT kabi yozish)
        async function askAI() {
            const input = document.getElementById('ai-input').value;
            const display = document.getElementById('ai-display');
            display.innerHTML = ""; 
            
            try {
                const res = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${GEMINI_KEY}`, {
                    method: 'POST',
                    body: JSON.stringify({contents: [{parts: [{text: `Til: ${currentLang}. Savol: ${input}. Batafsil va ilmiy javob ber.`}]}]})
                });
                const data = await res.json();
                const text = data.candidates[0].content.parts[0].text;
                
                // Typing effekti
                let i = 0;
                const timer = setInterval(() => {
                    display.innerHTML += text.charAt(i);
                    i++;
                    if (i >= text.length) clearInterval(timer);
                    display.scrollTop = display.scrollHeight;
                }, 15);
            } catch(e) { display.innerText = "Xatolik yuz berdi."; }
        }

        // 2. To'g'rilangan O'yin mantiqi
        const trashItems = [
            {e:"🧴", t:"plastic"}, {e:"🍎", t:"organic"}, {e:"📰", t:"paper"}, 
            {e:"🔋", t:"hazard"}, {e:"🥤", t:"plastic"}, {e:"🍌", t:"organic"}
        ];

        function checkAnswer(type) {
            if(type === currentItem.type) {
                score += 10;
                alert("To'g'ri! +10 ball");
            } else {
                score -= 5;
                alert("Xato! Bu " + currentItem.type + " edi.");
            }
            document.getElementById('score').innerText = score;
            currentItem = trashItems[Math.floor(Math.random()*trashItems.length)];
            document.getElementById('item-emoji').innerText = currentItem.emoji;
        }

        // 3. Shaharlar (12 ta)
        const cities = [
            {n:"Toshkent", lt:41.2, ln:69.2}, {n:"Berlin", lt:52.5, ln:13.4}, {n:"Pekin", lt:39.9, ln:116.4},
            {n:"Seul", lt:37.5, ln:126.9}, {n:"Tokio", lt:35.6, ln:139.6}, {n:"Moskva", lt:55.7, ln:37.6},
            {n:"Istanbul", lt:41.0, ln:28.9}, {n:"Qohira", lt:30.0, ln:31.2}, {n:"Rio", lt:-22.9, ln:-43.1},
            {n:"Bogota", lt:4.7, ln:-74.0}, {n:"Washington", lt:38.8, ln:-77.0}, {n:"Ottawa", lt:45.4, ln:-75.6}
        ];

        async function loadCities() {
            const list = document.getElementById('city-list');
            for(let c of cities) {
                const res = await fetch(`https://api.open-meteo.com/v1/forecast?latitude=${c.lt}&longitude=${c.ln}&current=temperature_2m`);
                const data = await res.json();
                list.innerHTML += `<div class="glass" style="text-align:center"><h4>${c.n}</h4><b style="font-size:24px; color:var(--neon)">${Math.round(data.current.temperature_2m)}°C</b></div>`;
            }
        }

        // Chart Init
        new Chart(document.getElementById('forecastChart'), {
            type: 'line',
            data: { labels: ['2025','2040','2060','2080'], datasets: [{label:'Temp Change', data:[1.1, 1.8, 2.6, 3.4], borderColor:'#00f2fe'}] },
            options: { plugins: { legend: { labels: { color: 'white' } } } }
        });

        function download(type) {
            const content = document.getElementById('ai-display').innerText;
            if(type === 'pdf') {
                const doc = new jspdf.jsPDF();
                doc.text(content, 10, 10);
                doc.save("report.pdf");
            } else {
                const blob = new Blob([content], {type: 'application/msword'});
                const link = document.createElement('a');
                link.href = URL.createObjectURL(blob);
                link.download = "report.doc";
                link.click();
            }
        }

        loadCities();
    </script>
    </body>
    </html>
    """)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
