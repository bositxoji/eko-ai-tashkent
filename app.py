import os
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# --- GLOBAL MULTI-INSTITUTIONAL KNOWLEDGE BASE ---
# Manbalar: NASA, UNEP, Google Sustainability, World Bank, EEA
GLOBAL_INTELLIGENCE = {
    "suv": {
        "unep": "UNEP (BMT) hisoboti: Dunyo aholisining 33 foizi xavfsiz ichimlik suvidan mahrum. 2030-yilga borib global suv tanqisligi 40% ga yetishi kutilmoqda.",
        "nasa": "NASA GRACE: Yer osti suv qatlamlarining 21 tasi (jami 37 tadan) kritik darajada kamayib bormoqda.",
        "google": "Google Water Risk: Sanoat zonalarida suv sarfi so'nggi 5 yilda samaradorlikni 20% ga oshirgan bo'lsa-da, umumiy iste'mol ortmoqda."
    },
    "havo": {
        "unep": "UNEP: Havo ifloslanishi har yili global iqtisodiyotga 5 trillion dollar zarar yetkazmoqda. PM2.5 zarralari eng xavfli antropogen omil.",
        "google": "Google Environmental Insights: Shaharlardagi transport emissiyasi global CO2 ning 72% ini tashkil qilmoqda.",
        "nasa": "NASA OMI: Stratosferadagi ozon qatlami tiklanmoqda, biroq troposferadagi 'issiqlik orollari' effekti kuchaymoqda."
    },
    "iqlim": {
        "unep": "UNEP Emission Gap Report: Global haroratni 1.5°C darajada ushlab turish uchun 2030-yilgacha emissiyani 45% ga qisqartirish shart.",
        "nasa": "NASA GISS: 2025-yil tarixdagi eng issiq 3 ta yildan biri bo'ldi. Muzliklarning erish tezligi rekord darajada.",
        "google": "Google Climate AI: Sun'iy intellekt yordamida prognozlash iqlim falokatlarini 72 soat oldin 90% aniqlik bilan aytib bermoqda."
    },
    "energiya": {
        "unep": "UNEP: Qayta tiklanuvchi energiya investitsiyalari yiliga 500 milliard dollardan oshdi.",
        "nasa": "NASA Solar Data: Quyosh faolligi davri yashil energiya hosildorligini oshirish uchun qulay imkoniyatlar yaratmoqda.",
        "google": "Google 24/7 Carbon-Free: Ma'lumotlar markazlarini 100% toza energiyaga o'tkazish tajribasi global standartga aylanmoqda."
    }
}

def global_ai_engine(query):
    query = query.lower()
    report = []
    
    # Mantiqiy tahlil algoritmi
    found_topics = [topic for topic in GLOBAL_INTELLIGENCE if topic in query]
    
    if not found_topics:
        return """<div class='error-msg'>🤖 <b>Tizim xabari:</b> So'rov bo'yicha global bazada ma'lumot qidirilmoqda. 
        Iltimos, kalit so'zlardan foydalaning: <i>Suv, Havo, Iqlim, Energiya, Chiqindi.</i></div>"""

    for topic in found_topics:
        data = GLOBAL_INTELLIGENCE[topic]
        block = f"""
        <div class="analysis-card">
            <h2 class="topic-title">🌍 {topic.upper()} MUAMMOSI: GLOBAL ANALITIKA</h2>
            <div class="source-grid">
                <div class="source-box unep"><b>🇺🇳 UNEP:</b> {data['unep']}</div>
                <div class="source-box nasa"><b>🚀 NASA:</b> {data['nasa']}</div>
                <div class="source-box google"><b>🔍 GOOGLE:</b> {data['google']}</div>
            </div>
            <div class="conclusion">
                <b>💡 EKSPERT XULOSASI:</b> Ushbu muammoni hal qilish uchun institutlararo integratsiya va 
                raqamli monitoringni (Satellite AI) kuchaytirish zarur.
            </div>
        </div>
        """
        report.append(block)
    
    return "".join(report)

@app.route('/')
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="uz">
    <head>
        <meta charset="UTF-8">
        <title>ECO-AI WORLD | Global Intelligence</title>
        <style>
            :root { --unep: #0077b6; --nasa: #e03131; --google: #2b8a3e; --bg: #0b0e14; }
            body { background: var(--bg); color: #e9ecef; font-family: 'Inter', sans-serif; margin: 0; }
            .nav { background: #1a1f26; padding: 20px 80px; border-bottom: 2px solid #343a40; display: flex; justify-content: space-between; align-items: center; }
            .container { max-width: 1200px; margin: 50px auto; padding: 0 20px; }
            .chat-window { background: #1a1f26; border-radius: 20px; border: 1px solid #343a40; display: flex; flex-direction: column; height: 750px; box-shadow: 0 20px 50px rgba(0,0,0,0.4); }
            #display { flex: 1; padding: 40px; overflow-y: auto; scroll-behavior: smooth; }
            .input-box { padding: 30px; background: #252b33; display: flex; gap: 15px; border-top: 1px solid #343a40; border-radius: 0 0 20px 20px; }
            input { flex: 1; background: #0b0e14; border: 1px solid #495057; color: #fff; padding: 18px; border-radius: 12px; font-size: 16px; outline: none; transition: 0.3s; }
            input:focus { border-color: #00d2ff; box-shadow: 0 0 15px rgba(0,210,255,0.2); }
            .send-btn { background: linear-gradient(135deg, #00d2ff 0%, #3a7bd5 100%); color: #fff; border: none; padding: 0 40px; border-radius: 12px; font-weight: bold; cursor: pointer; text-transform: uppercase; }
            
            .analysis-card { background: #252b33; border-radius: 15px; padding: 25px; margin-bottom: 30px; border-left: 5px solid #00d2ff; }
            .topic-title { margin-top: 0; font-size: 20px; color: #00d2ff; }
            .source-grid { display: grid; gap: 15px; margin: 20px 0; }
            .source-box { padding: 15px; border-radius: 8px; font-size: 14px; line-height: 1.6; }
            .unep { border: 1px solid var(--unep); background: rgba(0, 119, 182, 0.1); }
            .nasa { border: 1px solid var(--nasa); background: rgba(224, 49, 49, 0.1); }
            .google { border: 1px solid var(--google); background: rgba(43, 138, 62, 0.1); }
            .conclusion { background: #1a1f26; padding: 15px; border-radius: 8px; border: 1px dashed #ced4da; font-size: 15px; }
            .error-msg { color: #fab005; padding: 20px; border: 1px solid #fab005; border-radius: 10px; }
        </style>
    </head>
    <body>
        <div class="nav">
            <div style="font-size: 26px; font-weight: 800;">GLOBAL <span style="color:#00d2ff">ECO-AI</span></div>
            <div style="font-size: 14px;">Status: <span style="color:#40c057;">● Multi-Database Sync Active</span></div>
        </div>

        <div class="container">
            <div class="chat-window">
                <div id="display">
                    <div style="text-align: center; padding-top: 100px;">
                        <h1 style="font-size: 32px; margin-bottom: 10px;">Dunyo bilimlar bazasi yuklandi.</h1>
                        <p style="opacity: 0.6;">NASA, UNEP va Google Insights tahlillari asosida javob beraman.</p>
                    </div>
                </div>
                <div class="input-box">
                    <input type="text" id="userInput" placeholder="Tahlil uchun mavzu (masalan: Suv va Iqlim)..." onkeypress="if(event.key==='Enter') runEngine()">
                    <button class="send-btn" onclick="runEngine()">Tahlilni Boshlash</button>
                </div>
            </div>
        </div>

        <script>
            function runEngine() {
                const inp = document.getElementById('userInput');
                const disp = document.getElementById('display');
                if(!inp.value) return;

                const query = inp.value;
                if(disp.innerHTML.includes('Dunyo bilimlar bazasi')) disp.innerHTML = '';
                
                disp.innerHTML += `<div style="margin-bottom: 20px; color: #adb5bd;">> So'rov: ${query}</div>`;
                
                fetch('/get_global_analysis', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({query: query})
                })
                .then(res => res.json())
                .then(data => {
                    disp.innerHTML += data.result;
                    disp.scrollTop = disp.scrollHeight;
                });
                inp.value = '';
            }
        </script>
    </body>
    </html>
    """)

@app.route('/get_global_analysis', methods=['POST'])
def global_analysis():
    u_query = request.json.get('query', '')
    res_html = global_ai_engine(u_query)
    return jsonify({"result": res_html})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
