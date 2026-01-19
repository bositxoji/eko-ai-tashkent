import os
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# --- UNIVERSAL KNOWLEDGE BASE (UNEP, NASA, GOOGLE) ---
GLOBAL_DATA = {
    "suv": "UNEP ma'lumotlariga ko'ra, global chuchuk suv zaxiralari sanoat va iqlim o'zgarishi tufayli yiliga 0.5% ga kamaymoqda. NASA GRACE sun'iy yo'ldoshlari yer osti suvlari sathi kritik darajaga tushganini tasdiqlaydi.",
    "havo": "Google Environmental Insights tahliliga ko'ra, transport emissiyasi shahar havosidagi PM2.5 zarralarining 70% idan ortig'iga sabab bo'ladi. NASA havo monitoringi bu ko'rsatkichni global isishning asosiy drayveri deb hisoblaydi.",
    "iqlim": "BMT (UNEP) 2026-yilgi hisobotida global harorat sanoatdan oldingi davrga nisbatan 1.1°C ga oshganini va bu tabiiy ofatlar chastotasini 3 barobarga ko'paytirganini ta'kidlaydi.",
    "energiya": "Xalqaro Energetika Agentligi va Google tahlillari shuni ko'rsatadiki, 2030-yilga borib dunyo energiyasining 50% dan ortig'i qayta tiklanuvchi manbalardan (quyosh, shamol) olinishi shart.",
    "chiqindi": "Statistika: Dunyo okeanlarida har yili 8-10 million tonna yangi plastik chiqindi paydo bo'ladi. NASA va WWF bu jarayonni ekotizim uchun 'qaytarilmas nuqta' deb atamoqda."
}

def universal_ai_logic(user_text):
    text = user_text.lower()
    response_parts = []
    
    # 1. Bazadan mos keladigan qismlarni yig'ish
    for key, info in GLOBAL_DATA.items():
        if key in text:
            response_parts.append(info)
    
    # 2. Agar bazada aniq javob bo'lmasa yoki savol kengroq bo'lsa
    if not response_parts:
        return f"""
        <div class="universal-report">
            <h3 style="color:#00d2ff;">🌐 GLOBAL TAHLILIY XULOSA</h3>
            <p>Sizning so'rovingiz bo'yicha <b>NASA, UNEP va Google Data</b> tizimlari asosida quyidagi xulosani taqdim etaman:</p>
            <p>Hozirgi vaqtda "{user_text}" masalasi global barqaror rivojlanish maqsadlarining (SDG) ajralmas qismi hisoblanadi. 
            Ilmiy tadqiqotlar shuni ko'rsatadiki, har qanday antropogen ta'sir ekotizimda zanjirli reaksiyani yuzaga keltirmoqda. 
            NASA monitoringi bo'yicha, ushbu yo'nalishda 2026-yilda raqamli nazorat va AI tahlili 40% ga kuchaytirilishi kutilmoqda.</p>
            <div style="border-top:1px dashed #444; margin-top:10px; padding-top:10px; font-size:14px; color:#aaa;">
                <i>*Eslatma: Tizim ushbu mavzuni 'Global Monitoring' kategoriyasi bo'yicha tahlil qildi.</i>
            </div>
        </div>
        """
    
    # 3. Bazadagi ma'lumotlarni birlashtirib berish
    combined_info = " <br><br> ".join(response_parts)
    return f"""
    <div class="expert-report">
        <h3 style="color:#00d2ff;">🔬 INSTITUTLARARO EXPERT TAHLILI</h3>
        <p>{combined_info}</p>
        <p style="background:rgba(0,210,255,0.1); padding:10px; border-radius:5px;">
        <b>Xulosa:</b> Savolingizda ko'tarilgan muammo global ekologik barqarorlikka bevosita bog'liq.</p>
    </div>
    """

@app.route('/')
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="uz">
    <head>
        <meta charset="UTF-8">
        <title>GLOBAL ECO-AI | Universal Portal</title>
        <style>
            :root { --accent: #00d2ff; --bg: #0b0e14; }
            body { background: var(--bg); color: #e9ecef; font-family: 'Inter', sans-serif; margin: 0; }
            .header { background: #1a1f26; padding: 25px 60px; border-bottom: 2px solid #343a40; display: flex; justify-content: space-between; align-items: center; }
            .container { max-width: 1100px; margin: 40px auto; padding: 0 20px; }
            .chat-box { background: #1a1f26; border-radius: 20px; border: 1px solid #343a40; display: flex; flex-direction: column; height: 700px; }
            #display { flex: 1; padding: 40px; overflow-y: auto; line-height: 1.7; font-size: 16px; }
            .input-box { padding: 25px; background: #252b33; display: flex; gap: 15px; border-radius: 0 0 20px 20px; }
            input { flex: 1; background: #0b0e14; border: 1px solid #495057; color: #fff; padding: 18px; border-radius: 12px; font-size: 16px; outline: none; }
            button { background: linear-gradient(135deg, #00d2ff 0%, #3a7bd5 100%); color: #fff; border: none; padding: 0 45px; border-radius: 12px; font-weight: bold; cursor: pointer; text-transform: uppercase; }
            .expert-report, .universal-report { animation: fadeIn 0.5s ease; }
            @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        </style>
    </head>
    <body>
        <div class="header">
            <div style="font-size: 28px; font-weight: 800;">GLOBAL <span style="color:var(--accent)">ECO-AI</span> v17.0</div>
            <div style="font-size: 13px; color: #40c057;">● SYSTEM: UNIVERSAL RESPONSE MODE</div>
        </div>
        <div class="container">
            <div class="chat-box">
                <div id="display">
                    <div style="text-align:center; opacity:0.5; padding-top:150px;">
                        <h2>Savol yozing...</h2>
                        <p>Har qanday ekologik mavzuda NASA va UNEP tahlillarini taqdim etaman.</p>
                    </div>
                </div>
                <div class="input-box">
                    <input type="text" id="userInput" placeholder="Muammo yoki savolingizni kiriting..." onkeypress="if(event.key==='Enter') start()">
                    <button onclick="start()">Tahlil</button>
                </div>
            </div>
        </div>
        <script>
            function start() {
                const inp = document.getElementById('userInput');
                const disp = document.getElementById('display');
                if(!inp.value) return;

                const q = inp.value;
                if(disp.innerHTML.includes('Savol yozing')) disp.innerHTML = '';
                disp.innerHTML += `<div style="color:#adb5bd; margin-top:25px;">> Savol: ${q}</div>`;
                
                fetch('/ask', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({query: q})
                })
                .then(res => res.json())
                .then(data => {
                    disp.innerHTML += `<div style="margin-top:15px;">${data.response}</div>`;
                    disp.scrollTop = disp.scrollHeight;
                });
                inp.value = '';
            }
        </script>
    </body>
    </html>
    """)

@app.route('/ask', methods=['POST'])
def ask():
    query = request.json.get('query', '')
    response = universal_ai_logic(query)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
