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
        <title>Eco AI | Future Horizons 2080</title>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            :root { --neon: #00f2fe; --danger: #ff4b2b; --bg: #050505; }
            body { background: var(--bg); color: #fff; font-family: 'Segoe UI', sans-serif; margin: 0; }
            nav { background: #111; padding: 20px; display: flex; justify-content: space-around; position: sticky; top: 0; z-index: 100; border-bottom: 1px solid var(--neon); }
            nav a { color: #fff; text-decoration: none; font-weight: bold; font-size: 14px; }
            .section { padding: 60px 20px; max-width: 1200px; margin: auto; border-bottom: 1px solid #222; }
            h2 { color: var(--neon); text-align: center; letter-spacing: 3px; }
            
            /* Carbon Footprint & Future Section */
            .grid-future { display: grid; grid-template-columns: 1fr 1fr; gap: 30px; }
            canvas { background: #111; border-radius: 20px; padding: 20px; }
            
            /* Eco AI Chat Section */
            .ai-chat { background: #111; padding: 30px; border-radius: 30px; border: 1px solid #333; }
            #chat-output { min-height: 200px; color: #ddd; margin-bottom: 20px; white-space: pre-wrap; }
            input { width: 80%; padding: 15px; border-radius: 10px; border: none; background: #222; color: #fff; }
            .btn { padding: 15px 25px; border-radius: 10px; border: none; cursor: pointer; font-weight: bold; background: var(--neon); }
            
            /* Game Section */
            .game-box { height: 300px; background: linear-gradient(45deg, #001f3f, #000); border-radius: 30px; display: flex; flex-direction: column; align-items: center; justify-content: center; }
            .score { font-size: 24px; color: var(--neon); }
        </style>
    </head>
    <body>

    <nav>
        <a href="#monitor">MONITOR</a>
        <a href="#future">FUTURE 2080</a>
        <a href="#ai-expert">ECO AI EXPERT</a>
        <a href="#game">ECO GAMES</a>
        <a href="#carbon">FOOTPRINT</a>
    </nav>

    <div class="section" id="monitor">
        <h2>🌐 GLOBAL MONITORING</h2>
        <iframe src="https://earth.nullschool.net/#current/wind/surface/level/orthographic=69.21,41.26,1000" style="width:100%; height:500px; border-radius:30px; border:none;"></iframe>
    </div>

    <div class="section" id="future">
        <h2>📈 BASHORATLAR (2025 - 2080)</h2>
        <div class="grid-future">
            <div>
                <canvas id="forecastChart"></canvas>
            </div>
            <div style="padding: 20px; background: #111; border-radius: 20px;">
                <h3>Siyosiy va Tarixiy Tahlil</h3>
                <p id="historical-text" style="color: #aaa; font-size: 14px;">
                    2080-yilgacha bo'lgan iqlim o'zgarishlari dunyo siyosatini "Yashil diplomatiya"ga majbur qiladi. 2045-yilda global uglerod solig'i joriy etilishi kutilmoqda...
                </p>
            </div>
        </div>
    </div>

    <div class="section" id="ai-expert">
        <h2>🤖 ECO AI EXPERT</h2>
        <div class="ai-chat">
            <div id="chat-output">Ekologik savolingizni bering (masalan: "Orol dengizini qanday qutqaramiz?")...</div>
            <input type="text" id="ai-input" placeholder="Savol yozing...">
            <button class="btn" onclick="askAI()">SAVOL BERISH</button>
            <div style="margin-top: 20px;">
                <button onclick="downloadPDF()" style="background:#ff4b2b" class="btn">PDF YUKLASH</button>
                <button onclick="downloadDoc()" style="background:#2b55ff" class="btn">WORD YUKLASH</button>
            </div>
        </div>
    </div>

    <div class="section" id="game">
        <h2>🎮 ECO-GAME: TRASH SORT</h2>
        <div class="game-box">
            <p id="trash-item" style="font-size: 50px;">🗑️</p>
            <p>Ushbu chiqindini qayerga tashlaysiz?</p>
            <div>
                <button class="btn" onclick="playGame('recycle')">QAYTA ISHLASH</button>
                <button class="btn" style="background:gray" onclick="playGame('landfill')">AXLATXONA</button>
            </div>
            <p class="score">Ball: <span id="score-val">0</span></p>
        </div>
    </div>

    <script>
        const GEMINI_KEY = "AIzaSyCl-dBQmgQTJWgA5LR0Fy5Wiq7HLxaHK2Y";

        // 1. Forecast Chart (2080-yilgacha)
        const ctx = document.getElementById('forecastChart').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['2025', '2035', '2045', '2055', '2065', '2075', '2080'],
                datasets: [{
                    label: 'Global Harorat O'shishi (°C)',
                    data: [1.2, 1.5, 1.8, 2.2, 2.7, 3.2, 3.5],
                    borderColor: '#00f2fe',
                    fill: false
                }]
            }
        });

        // 2. AI Expert & Data Export
        async function askAI() {
            const query = document.getElementById('ai-input').value;
            const output = document.getElementById('chat-output');
            output.innerText = "Tahlil qilinmoqda...";
            
            const res = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${GEMINI_KEY}`, {
                method: 'POST',
                body: JSON.stringify({contents: [{parts: [{text: query + ". Batafsil tahlil qiling va hisobot tayyorlang."}]}]})
            });
            const data = await res.json();
            const responseText = data.candidates[0].content.parts[0].text;
            output.innerText = responseText;
        }

        function downloadPDF() {
            const { jsPDF } = window.jspdf;
            const doc = new jsPDF();
            doc.text(document.getElementById('chat-output').innerText, 10, 10);
            doc.save("eco-report.pdf");
        }

        function downloadDoc() {
            const content = document.getElementById('chat-output').innerText;
            const blob = new Blob(['\\ufeff', content], { type: 'application/msword' });
            const url = URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.download = 'eco-report.doc';
            link.click();
        }

        // 3. Eco Game Logic
        let score = 0;
        const trash = ["📦", "🔋", "🍎", "📰", "🥤"];
        function playGame(choice) {
            score += 10;
            document.getElementById('score-val').innerText = score;
            document.getElementById('trash-item').innerText = trash[Math.floor(Math.random()*trash.length)];
        }
    </script>
    </body>
    </html>
    """)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
