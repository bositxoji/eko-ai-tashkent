import os
import requests
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# AI Backend Logic
def get_ai_response(prompt, lang):
    api_key = "AIzaSyCl-dBQmgQTJWgA5LR0Fy5Wiq7HLxaHK2Y"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    payload = {"contents": [{"parts": [{"text": f"Javobni {lang} tilida, ilmiy va juda batafsil yoz: {prompt}"}]}]}
    try:
        response = requests.post(url, json=payload, timeout=15)
        data = response.json()
        return data['candidates'][0]['content']['parts'][0]['text']
    except Exception:
        return "Xatolik: Server AI bilan bog'lana olmadi. Iltimos, Render paneli orqali internet va API holatini tekshiring."

@app.route('/')
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="uz">
    <head>
        <meta charset="UTF-8">
        <title>Neural Eco v5.2 | A.A Ataxojayev</title>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            :root { --neon: #00f2fe; --bg: #010101; --glass: rgba(255,255,255,0.03); }
            body { background: var(--bg); color: #fff; font-family: 'Inter', sans-serif; margin: 0; }
            
            /* Navigatsiya va Mualliflik */
            nav { display: flex; justify-content: space-between; align-items: center; padding: 10px 40px; background: #000; border-bottom: 2px solid var(--neon); position: sticky; top: 0; z-index: 1000; }
            .header-info { display: flex; align-items: center; gap: 30px; }
            .authors { border-left: 2px solid var(--neon); padding-left: 20px; font-size: 12px; line-height: 1.4; color: #aaa; }
            .authors b { color: var(--neon); font-size: 14px; text-transform: uppercase; }

            .container { max-width: 1300px; margin: auto; padding: 25px; }
            .glass { background: var(--glass); backdrop-filter: blur(15px); border: 1px solid rgba(0,242,254,0.15); border-radius: 20px; padding: 25px; margin-bottom: 30px; }
            h2 { color: var(--neon); text-transform: uppercase; letter-spacing: 2px; border-bottom: 1px solid #222; padding-bottom: 10px; margin-bottom: 20px; }
            
            .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 25px; }
            .article-item { display: block; color: #ddd; text-decoration: none; padding: 15px; border-radius: 10px; border: 1px solid #222; margin-bottom: 10px; transition: 0.3s; }
            .article-item:hover { border-color: var(--neon); background: rgba(0, 242, 254, 0.05); transform: translateX(5px); }

            #ai-display { min-height: 300px; background: rgba(0,0,0,0.5); border: 1px solid #333; border-radius: 15px; padding: 25px; line-height: 1.8; overflow-y: auto; color: #e0e0e0; }
            textarea { width: 100%; background: #111; border: 1px solid #444; color: #fff; padding: 15px; border-radius: 12px; margin-top: 15px; box-sizing: border-box; }

            .btn { background: var(--neon); color: #000; border: none; padding: 12px 25px; border-radius: 8px; font-weight: bold; cursor: pointer; transition: 0.3s; }
            .btn:hover { box-shadow: 0 0 20px rgba(0, 242, 254, 0.4); }
            
            .map-container { height: 500px; border-radius: 20px; overflow: hidden; border: 1px solid var(--neon); box-shadow: 0 0 30px rgba(0,0,0,0.5); }
            .lang-btn { background: none; border: 1px solid var(--neon); color: var(--neon); padding: 6px 14px; border-radius: 6px; cursor: pointer; margin-left: 5px; }
            .lang-btn.active { background: var(--neon); color: #000; }
        </style>
    </head>
    <body>
        <nav>
            <div style="font-weight: bold; font-size: 22px; letter-spacing: 1px;">NEURAL ECO <span style="color:var(--neon)">PRO</span></div>
            <div class="header-info">
                <div class="authors">
                    Muallif: <b>A.A Ataxojayev</b><br>
                    Ilmiy rahbar: <b>E.A Egamberdiev</b>
                </div>
                <div style="display: flex;">
                    <button class="lang-btn active" onclick="updateLang('uz', this)">UZ</button>
                    <button class="lang-btn" onclick="updateLang('ru', this)">RU</button>
                    <button class="lang-btn" onclick="updateLang('en', this)">EN</button>
                </div>
            </div>
        </nav>

        <div class="container">
            <div class="map-container">
                <iframe src="https://earth.nullschool.net/#current/wind/surface/level/orthographic=69.21,41.26,1200" style="width:100%; height:100%; border:none;"></iframe>
            </div>

            <div class="grid">
                <div class="glass">
                    <h2 id="l-carb">Carbon Footprint</h2>
                    <canvas id="carbChart"></canvas>
                    <div style="background: rgba(0,0,0,0.4); padding: 15px; border-radius: 10px; margin-top: 20px; font-size: 13px;">
                        📌 <b>Tahlil:</b> Emissiya darajasi energiya iste'moli va transport tizimi bilan bevosita bog'liq.
                    </div>
                </div>

                <div class="glass">
                    <h2 id="l-lib">Ilmiy Kutubxona</h2>
                    <div style="max-height: 350px; overflow-y: auto;">
                        <a href="https://earth911.com" target="_blank" class="article-item">📑 Chiqindilarni utilizatsiya qilish texnologiyalari</a>
                        <a href="https://news.mongabay.com" target="_blank" class="article-item">🌳 Global o'rmon qoplami monitoringi</a>
                        <a href="https://oceana.org" target="_blank" class="article-item">🐋 Dengiz ekotizimi va bioxilma-xillik</a>
                        <a href="https://climate.nasa.gov" target="_blank" class="article-item">🚀 NASA: Iqlim o'zgarishi dinamikasi</a>
                    </div>
                </div>
            </div>

            <div class="glass">
                <h2 id="l-ai">Eco AI Intelligent Expert</h2>
                <div id="ai-display">Tizim tahlilga tayyor. Atrof-muhit risklari yoki barqaror rivojlanish haqida so'rang...</div>
                <textarea id="ai-input" placeholder="Savolingizni kiriting..."></textarea>
                <div style="margin-top:20px; display:flex; gap:15px;">
                    <button class="btn" onclick="callAI()" id="l-btn">TAHLIL QILISH</button>
                    <button class="btn" style="background:#ff4b2b; color:#fff;" onclick="generatePDF()">PDF EKSPORT</button>
                </div>
            </div>
        </div>

        <script>
            let currentLang = 'uz';

            function updateLang(l, btn) {
                currentLang = l;
                document.querySelectorAll('.lang-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                
                const ui = {
                    uz: {carb:"Karbon Footprint", lib:"Ilmiy Kutubxona", ai:"Eco AI Expert", btn:"TAHLIL QILISH"},
                    ru: {carb:"Углеродный след", lib:"Научная библиотека", ai:"Эко ИИ Эксперт", btn:"АНАЛИЗИРОВАТЬ"},
                    en: {carb:"Carbon Footprint", lib:"Scientific Library", ai:"Eco AI Expert", btn:"ANALYZE NOW"}
                };
                document.getElementById('l-carb').innerText = ui[l].carb;
                document.getElementById('l-lib').innerText = ui[l].lib;
                document.getElementById('l-ai').innerText = ui[l].ai;
                document.getElementById('l-btn').innerText = ui[l].btn;
            }

            async function callAI() {
                const inp = document.getElementById('ai-input').value;
                const out = document.getElementById('ai-display');
                if(!inp) return;
                
                out.innerText = "Ma'lumotlar qayta ishlanmoqda...";

                try {
                    const res = await fetch('/get_ai', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({prompt: inp, lang: currentLang})
                    });
                    const data = await res.json();
                    out.innerText = data.response;
                } catch(e) {
                    out.innerText = "Xato: Server bilan ulanishda muammo yuzaga keldi.";
                }
            }

            function generatePDF() {
                const doc = new jspdf.jsPDF();
                const content = document.getElementById('ai-display').innerText;
                const textLines = doc.splitTextToSize(content, 180);
                doc.setFontSize(16);
                doc.text("NEURAL ECO - ILMIY HISOBOT", 10, 15);
                doc.setFontSize(10);
                doc.text("Muallif: A.A Ataxojayev | Ilmiy rahbar: E.A Egamberdiev", 10, 22);
                doc.setFontSize(12);
                doc.text(textLines, 10, 35);
                doc.save("NeuralEco_Report.pdf");
            }

            // Charts
            const ctx = document.getElementById('carbChart').getContext('2d');
            new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: ['Sanoat', 'Transport', 'Turar-joy'],
                    datasets: [{
                        data: [40, 35, 25],
                        backgroundColor: ['#ff4b2b', '#00f2fe', '#ffcc00'],
                        borderWidth: 0
                    }]
                },
                options: {
                    plugins: { legend: { position: 'bottom', labels: { color: '#fff', padding: 20 } } }
                }
            });
        </script>
    </body>
    </html>
    """)

@app.route('/get_ai', methods=['POST'])
def ai_api():
    data = request.json
    response = get_ai_response(data['prompt'], data['lang'])
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.getenv("PORT", 5000))
