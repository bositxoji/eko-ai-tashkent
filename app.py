import os
import requests
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# UNIVERSAL AI LOGIC (Har qanday savolga javob beradi)
def get_ai_response(prompt, lang):
    # API Kalit va URL
    api_key = "AIzaSyCl-dBQmgQTJWgA5LR0Fy5Wiq7HLxaHK2Y"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    # AIga beriladigan ko'rsatma: Endi u faqat eko emas, universal yordamchi
    instruction = f"Sen universal va aqlli yordamchisan. Foydalanuvchi savoliga {lang} tilida juda batafsil, aniq va foydali javob ber. Savol: "
    
    payload = {
        "contents": [{
            "parts": [{"text": f"{instruction} {prompt}"}]
        }]
    }
    
    try:
        # Server orqali so'rov yuborish (Xavfsiz va bloklanmaydi)
        response = requests.post(url, json=payload, timeout=20)
        data = response.json()
        
        # Javobni olish
        if 'candidates' in data:
            return data['candidates'][0]['content']['parts'][0]['text']
        else:
            return "AI hozirda band. Iltimos, birozdan so'ng qayta urinib ko'ring."
    except Exception as e:
        return f"Tizimda ulanish xatosi yuz berdi. Iltimos, internet aloqasini tekshiring."

@app.route('/')
def index():
    # Avvalgi dizayn (Mualliflar va barcha bo'limlar saqlangan holda)
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="uz">
    <head>
        <meta charset="UTF-8">
        <title>Neural Eco v5.3 | A.A Ataxojayev</title>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            :root { --neon: #00f2fe; --bg: #010101; --glass: rgba(255,255,255,0.03); }
            body { background: var(--bg); color: #fff; font-family: 'Inter', sans-serif; margin: 0; }
            nav { display: flex; justify-content: space-between; align-items: center; padding: 10px 40px; background: #000; border-bottom: 2px solid var(--neon); position: sticky; top: 0; z-index: 1000; }
            .header-info { display: flex; align-items: center; gap: 30px; }
            .authors { border-left: 2px solid var(--neon); padding-left: 20px; font-size: 12px; line-height: 1.4; color: #aaa; }
            .authors b { color: var(--neon); font-size: 14px; text-transform: uppercase; }
            .container { max-width: 1300px; margin: auto; padding: 25px; }
            .glass { background: var(--glass); backdrop-filter: blur(15px); border: 1px solid rgba(0,242,254,0.15); border-radius: 20px; padding: 25px; margin-bottom: 30px; }
            h2 { color: var(--neon); text-transform: uppercase; letter-spacing: 2px; border-bottom: 1px solid #222; padding-bottom: 10px; margin-bottom: 20px; }
            .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 25px; }
            .article-item { display: block; color: #ddd; text-decoration: none; padding: 15px; border-radius: 10px; border: 1px solid #222; margin-bottom: 10px; transition: 0.3s; }
            .article-item:hover { border-color: var(--neon); background: rgba(0, 242, 254, 0.05); }
            #ai-display { min-height: 300px; background: rgba(0,0,0,0.5); border: 1px solid #333; border-radius: 15px; padding: 25px; line-height: 1.8; overflow-y: auto; color: #e0e0e0; white-space: pre-wrap; }
            textarea { width: 100%; background: #111; border: 1px solid #444; color: #fff; padding: 15px; border-radius: 12px; margin-top: 15px; box-sizing: border-box; font-size: 16px; outline: none; }
            textarea:focus { border-color: var(--neon); }
            .btn { background: var(--neon); color: #000; border: none; padding: 12px 25px; border-radius: 8px; font-weight: bold; cursor: pointer; transition: 0.3s; }
            .btn:hover { box-shadow: 0 0 20px rgba(0, 242, 254, 0.4); opacity: 0.9; }
            .map-container { height: 500px; border-radius: 20px; overflow: hidden; border: 1px solid var(--neon); margin-bottom: 30px; }
            .lang-btn { background: none; border: 1px solid var(--neon); color: var(--neon); padding: 6px 14px; border-radius: 6px; cursor: pointer; margin-left: 5px; }
            .lang-btn.active { background: var(--neon); color: #000; }
        </style>
    </head>
    <body>
        <nav>
            <div style="font-weight: bold; font-size: 22px;">NEURAL ECO <span style="color:var(--neon)">PRO</span></div>
            <div class="header-info">
                <div class="authors">
                    Muallif: <b>A.A Ataxojayev</b><br>
                    Ilmiy rahbar: <b>E.A Egamberdiev</b>
                </div>
                <div>
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
                </div>
                <div class="glass">
                    <h2 id="l-lib">Scientific Library</h2>
                    <div style="max-height: 300px; overflow-y: auto;">
                        <a href="https://climate.nasa.gov" target="_blank" class="article-item">🚀 NASA Climate Data</a>
                        <a href="https://earth911.com" target="_blank" class="article-item">♻️ Waste Management Risks</a>
                        <a href="https://news.mongabay.com" target="_blank" class="article-item">🌳 Forest Monitoring</a>
                    </div>
                </div>
            </div>

            <div class="glass">
                <h2 id="l-ai">Eco AI Intelligent Expert</h2>
                <div id="ai-display">Men universal aqlli yordamchiman. Har qanday savolingizga javob bera olaman...</div>
                <textarea id="ai-input" placeholder="Savolingizni bu yerga yozing (Masalan: Dunyo iqtisodiyoti haqida yoki Fizika qonunlari haqida)..."></textarea>
                <div style="margin-top:20px; display:flex; gap:15px;">
                    <button class="btn" onclick="callAI()" id="l-btn">SAVOLNI YUBORISH</button>
                    <button class="btn" style="background:#ff4b2b; color:#fff;" onclick="generatePDF()">HISOBOT (PDF)</button>
                </div>
            </div>
        </div>

        <script>
            let currentLang = 'uz';

            function updateLang(l, btn) {
                currentLang = l;
                document.querySelectorAll('.lang-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
            }

            async function callAI() {
                const inp = document.getElementById('ai-input').value;
                const out = document.getElementById('ai-display');
                if(!inp) return;
                
                out.innerText = "AI o'ylamoqda va javob tayyorlamoqda...";

                try {
                    // SERVER-SIDE REQUEST (Bloklanishni oldini oladi)
                    const res = await fetch('/get_ai', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({prompt: inp, lang: currentLang})
                    });
                    const data = await res.json();
                    
                    // Javobni chiqarish
                    out.innerText = "";
                    let i = 0;
                    const text = data.response;
                    const interval = setInterval(() => {
                        out.innerText += text.charAt(i);
                        i++;
                        if (i >= text.length) {
                            clearInterval(interval);
                            out.scrollTop = out.scrollHeight;
                        }
                    }, 15);
                } catch(e) {
                    out.innerText = "Xato: Tizim hozirda javob bera olmaydi. Iltimos, Render paneli orqali API holatini tekshiring.";
                }
            }

            function generatePDF() {
                const doc = new jspdf.jsPDF();
                const content = document.getElementById('ai-display').innerText;
                const textLines = doc.splitTextToSize(content, 180);
                doc.text(textLines, 10, 20);
                doc.save("AI_Report.pdf");
            }

            // Chart Initialization
            const ctx = document.getElementById('carbChart').getContext('2d');
            new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: ['Sanoat', 'Transport', 'Turar-joy'],
                    datasets: [{ data: [40, 35, 25], backgroundColor: ['#ff4b2b', '#00f2fe', '#ffcc00'], borderWidth: 0 }]
                },
                options: { plugins: { legend: { labels: { color: '#fff' } } } }
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
    # Render uchun portni avtomatik aniqlash
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
