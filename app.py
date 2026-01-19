import os
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# --- KENGAYTIRILGAN O'ZBEK TILIDAGI BILIMLAR BAZASI ---
KNOWLEDGE_BASE = {
    "suv": "NASA va UNEP ma'lumotlariga ko'ra, global chuchuk suv tanqisligi 2026-yilda eng yuqori nuqtaga chiqishi kutilmoqda. Markaziy Osiyo mintaqasida muzliklarning erishi daryolar oqimini kamaytirib, qishloq xo'jaligiga jiddiy xavf solmoqda. Google Sustainability tahlillari suvni tejash texnologiyalarini joriy etishni 40% samaraliroq deb hisoblaydi.",
    "havo": "Havo ifloslanishi (PM2.5) hozirda megapolislarda me'yordan 15 baravar yuqori. NASA monitoringi shuni ko'rsatadiki, bu nafaqat sog'liqqa, balki mahalliy iqlimning isishiga ham sabab bo'ladi. UNEP tavsiyasiga ko'ra, yashil hududlarni 30% ga ko'paytirish havo sifatini sezilarli yaxshilaydi.",
    "iqlim": "Global isish natijasida 2025-2026 yillarda o'rtacha harorat 1.2°C ga oshdi. Bu issiqxona gazlarining (CO2) rekord darajadagi 425 ppm ko'rsatkichi bilan bog'liq. NASA Climate Now loyihasi muzliklarning erishini to'xtatish uchun karbon neytralligiga erishishni shart deb biladi.",
    "chiqindi": "Dunyo okeanlaridagi plastik miqdori har yili 10 million tonnaga ko'paymoqda. Google AI tahlillari chiqindilarni saralash va qayta ishlash darajasini 60% ga yetkazish orqali ekologik muvozanatni tiklash mumkinligini ko'rsatmoqda."
}

def generate_detailed_response(user_query):
    query = user_query.lower()
    detailed_text = ""
    
    # 1. Kalit so'zlarni tekshirish va tahlil qilish
    found = False
    for key, data in KNOWLEDGE_BASE.items():
        if key in query:
            detailed_text += f"### 🌍 {key.upper()} BO'YICHA GLOBAL TAHLIL\n{data}\n\n"
            found = True
            
    # 2. Agar aniq kalit so'z bo'lmasa, universal o'zbekcha javob yasash
    if not found:
        detailed_text = f"""
        ### 🤖 ECO-AI ANALITIK HISOBOTI
        Sizning "{user_query}" bo'yicha so'rovingiz qabul qilindi. 
        
        **NASA va Google Data Insights** tahlillari shuni ko'rsatadiki, ushbu masala hozirgi global ekologik inqiroz sharoitida juda dolzarbdir. 
        UNEP (BMT Atrof-muhit dasturi) ma'lumotlariga ko'ra, insoniyat 2030-yilgacha ekologik barqarorlikni ta'minlash uchun raqamli monitoring tizimlarini (AI) joriy etishi shart. 
        
        **Xulosa:** Tizim ushbu yo'nalishda ilmiy tadqiqotlarni davom ettirmoqda. Kelajakda barqaror yechimlar faqat ilmiy va texnologik yondashuv orqali amalga oshiriladi.
        """
    
    return detailed_text

@app.route('/')
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="uz">
    <head>
        <meta charset="UTF-8">
        <title>ECO-AI WORLD | Uzb Edition</title>
        <style>
            body { background: #05070a; color: #e6edf3; font-family: 'Segoe UI', sans-serif; margin: 0; padding: 20px; }
            .chat-container { max-width: 900px; margin: 50px auto; background: #0d1117; border: 1px solid #30363d; border-radius: 15px; padding: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
            h1 { color: #00d2ff; text-align: center; }
            #output { min-height: 300px; border-bottom: 1px solid #30363d; margin-bottom: 20px; padding: 10px; white-space: pre-wrap; line-height: 1.6; }
            .input-group { display: flex; gap: 10px; }
            input { flex: 1; background: #010409; border: 1px solid #30363d; color: white; padding: 15px; border-radius: 8px; font-size: 16px; }
            button { background: #00d2ff; color: black; border: none; padding: 15px 30px; border-radius: 8px; font-weight: bold; cursor: pointer; }
            button:hover { background: #0099cc; }
        </style>
    </head>
    <body>
        <div class="chat-container">
            <h1>🌱 ECO-AI GLOBAL PORTAL</h1>
            <div id="output">Tizim tayyor. O'zbek tilida savol bering...</div>
            <div class="input-group">
                <input type="text" id="userInput" placeholder="Savol yozing (masalan: daryolar muammosi)...">
                <button onclick="askAI()">TAHLIL</button>
            </div>
        </div>
        <script>
            function askAI() {
                const inp = document.getElementById('userInput');
                const out = document.getElementById('output');
                if(!inp.value) return;

                out.innerHTML = "Tahlil qilinmoqda...";
                fetch('/process', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({query: inp.value})
                })
                .then(res => res.json())
                .then(data => {
                    out.innerHTML = data.response;
                    inp.value = '';
                });
            }
        </script>
    </body>
    </html>
    """)

@app.route('/process', methods=['POST'])
def process():
    data = request.json
    response = generate_detailed_response(data.get('query', ''))
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
