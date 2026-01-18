import os
import requests
import time
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# --- AI MODELLAR INTEGRATSIYASI ---

def get_gemini_response(prompt, lang):
    api_key = "AIzaSyCl-dBQmgQTJWgA5LR0Fy5Wiq7HLxaHK2Y"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    payload = {"contents": [{"parts": [{"text": f"Sen universal yordamchisan. {lang} tilida javob ber: {prompt}"}]}]}
    try:
        res = requests.post(url, json=payload, timeout=15)
        return res.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        return None

def get_llama_response(prompt, lang):
    # Llama 3 (Groq API orqali bepul va tezkor alternativ)
    # Eslatma: Bu yerda ochiq API xizmatidan foydalaniladi
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": "Bearer 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"} # Test kalit
    payload = {
        "model": "llama3-8b-8192",
        "messages": [{"role": "user", "content": f"Answer in {lang}: {prompt}"}]
    }
    try:
        res = requests.post(url, json=payload, headers=headers, timeout=15)
        return res.json()['choices'][0]['message']['content']
    except:
        return "Xatolik: Ikkala AI modeli ham hozirda band."

def hybrid_ai_logic(prompt, lang):
    # Avval Gemini bilan urinib ko'radi
    response = get_gemini_response(prompt, lang)
    if response:
        return response
    # Agar Gemini xato bersa, Llama 3 ishga tushadi
    return get_llama_response(prompt, lang)

# --- WEB SERVER QISMI ---

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
            :root { --neon: #00f2fe; --bg: #010101; }
            body { background: var(--bg); color: #fff; font-family: sans-serif; margin: 0; }
            nav { display: flex; justify-content: space-between; padding: 15px 40px; border-bottom: 2px solid var(--neon); background: #000; }
            .container { max-width: 1200px; margin: auto; padding: 20px; }
            .glass { background: rgba(255,255,255,0.05); border: 1px solid #333; border-radius: 15px; padding: 20px; margin-bottom: 20px; }
            #ai-display { min-height: 250px; background: #000; border: 1px solid #222; padding: 20px; border-radius: 10px; white-space: pre-wrap; }
            textarea { width: 100%; background: #111; color: #fff; border: 1px solid #444; padding: 15px; border-radius: 10px; margin-top: 10px; }
            .btn { background: var(--neon); color: #000; border: none; padding: 12px 25px; border-radius: 8px; font-weight: bold; cursor: pointer; }
            .city-card { min-width: 130px; background: #0a0a0a; border: 1px solid #333; padding: 10px; border-radius: 8px; text-align: center; }
        </style>
    </head>
    <body>
        <nav>
            <div style="font-size: 24px; font-weight: bold; color: var(--neon);">ECO-AI-WORLD</div>
            <div style="font-size: 12px; color: #aaa;">Muallif: A.A Ataxojayev | Rahbar: E.A Egamberdiev</div>
        </nav>
        <div class="container">
            <div style="display: flex; gap: 15px; overflow-x: auto; margin-bottom: 20px;" id="cities"></div>
            
            <div class="glass">
                <h2>🤖 Hybrid AI Expert (Gemini + Llama)</h2>
                <div id="ai-display">Savol kutilyapti...</div>
                <textarea id="ai-input" placeholder="Xohlagan savolingizni bering..."></textarea>
                <div style="margin-top: 15px; display: flex; gap: 10px;">
                    <button class="btn" onclick="ask()">YUBORISH</button>
                    <button class="btn" style="background: #ff4b2b; color: #fff;" onclick="toPDF()">PDF HISOBOT</button>
                </div>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                <div class="glass"><canvas id="carbChart"></canvas></div>
                <div class="glass">
                    <h3>📚 Kutubxona</h3>
                    <a href="https://climate.nasa.gov" target="_blank" style="color: var(--neon);">🚀 NASA Monitoring</a><br><br>
                    <a href="https://earth911.com" target="_blank" style="color: var(--neon);">♻️ Eco Resource</a>
                </div>
            </div>
        </div>

        <script>
            async function ask() {
                const i = document.getElementById('ai-input').value;
                const o = document.getElementById('ai-display');
                if(!i) return;
                o.innerText = "AIlar kelishib javob tayyorlamoqda...";
                const res = await fetch('/get_ai', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({prompt: i, lang: 'uz'})
                });
                const data = await res.json();
                o.innerText = data.response;
            }

            function toPDF() {
                const doc = new jspdf.jsPDF();
                doc.text(document.getElementById('ai-display').innerText, 10, 10);
                doc.save("EcoAI_Report.pdf");
            }

            async function getTemps() {
                const list = document.getElementById('cities');
                const pts = ["Toshkent", "London", "Tokio"];
                for(let p of pts) {
                    list.innerHTML += `<div class="city-card"><b>${p}</b><br>Live Data...</div>`;
                }
            }
            
            new Chart(document.getElementById('carbChart'), {
                type: 'doughnut',
                data: { labels: ['Sanoat', 'Transport', 'Uy-joy'], datasets: [{ data: [45, 30, 25], backgroundColor: ['#ff4b2b', '#00f2fe', '#ffcc00'] }] }
            });
            getTemps();
        </script>
    </body>
    </html>
    """)

@app.route('/get_ai', methods=['POST'])
def ai_api():
    data = request.json
    response = hybrid_ai_logic(data['prompt'], data['lang'])
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
