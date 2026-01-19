import os
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# --- OFFLINE INTELLIGENCE ENGINE ---
def get_offline_analysis(prompt):
    p = prompt.lower()
    
    # Ekologik bilimlar bazasi
    responses = {
        "suv": "Suv resurslari tahlili: Global miqyosda chuchuk suvning 70% qishloq xo'jaligiga sarflanadi. NASA ma'lumotlariga ko'ra, 2030-yilga kelib global suv tanqisligi 40% ga yetishi mumkin.",
        "havo": "Havo sifati monitoringi: PM2.5 zarralari miqdori ko'p shaharlarda me'yordan 10 barobar yuqori. Bu asosan sanoat va filtrlanmagan transport emissiyalari natijasidir.",
        "chiqindi": "Chiqindilarni boshqarish: Dunyoda har yili 2.1 milliard tonna qattiq maishiy chiqindi hosil bo'ladi. Ularning atigi 16 foizi qayta ishlanadi.",
        "daryo": "Daryolar ekotizimi: Daryolarning plastik bilan ifloslanishi okeanlardagi 'chiqindi orollari'ning asosiy manbaidir. Biologik tozalash inshootlarini o'rnatish shart.",
        "energiya": "Yashil energiya: Quyosh va shamol energiyasiga o'tish karbonat angidrid emissiyasini 80% gacha kamaytirishi isbotlangan.",
        "salom": "Assalomu alaykum! ECO-AI tizimi ishga tushdi. Ekologiya, tahlillar va prognozlar bo'yicha savol berishingiz mumkin."
    }

    # Kalit so'zlarni qidirish
    for key in responses:
        if key in p:
            return responses[key]
            
    return "Tahlil: Siz so'ragan mavzu bo'yicha ma'lumotlar bazasi yangilanmoqda. Umuman olganda, ushbu masala barqaror rivojlanish maqsadlari uchun juda dolzarb hisoblanadi."

@app.route('/')
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="uz">
    <head>
        <meta charset="UTF-8">
        <title>ECO-AI | CORE ENGINE</title>
        <style>
            body { background: #050505; color: #00f2fe; font-family: 'Segoe UI', sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
            .terminal { width: 90%; max-width: 800px; background: #000; border: 2px solid #00f2fe; border-radius: 15px; padding: 25px; box-shadow: 0 0 40px rgba(0,242,254,0.15); }
            #screen { height: 350px; overflow-y: auto; border-bottom: 1px solid #222; margin-bottom: 20px; font-size: 16px; line-height: 1.6; padding-right: 10px; color: #e0e0e0; }
            .input-box { display: flex; gap: 10px; }
            input { flex: 1; background: #0a0a0a; border: 1px solid #333; color: #fff; padding: 15px; border-radius: 8px; outline: none; font-size: 16px; }
            input:focus { border-color: #00f2fe; }
            button { background: #00f2fe; color: #000; border: none; padding: 10px 25px; border-radius: 8px; font-weight: bold; cursor: pointer; transition: 0.3s; }
            button:hover { background: #fff; box-shadow: 0 0 15px #fff; }
            .status { font-size: 12px; color: #555; margin-top: 15px; text-align: center; }
        </style>
    </head>
    <body>
        <div class="terminal">
            <div style="font-weight: bold; margin-bottom: 15px;">[ SYSTEM: OFFLINE INTELLIGENCE ACTIVE ]</div>
            <div id="screen">Tizim tayyor. Savolingizni yozing (masalan: daryolar, suv, havo)...</div>
            <div class="input-box">
                <input type="text" id="userInput" placeholder="Savol yozing..." onkeypress="if(event.key==='Enter') send()">
                <button onclick="send()">YUBORISH</button>
            </div>
            <div class="status">Neural Eco Engine v10.1 | 100% Reliability Mode</div>
        </div>

        <script>
            function send() {
                const inp = document.getElementById('userInput');
                const scr = document.getElementById('screen');
                if(!inp.value) return;

                const userMsg = inp.value;
                scr.innerHTML += `<div style="color:#00f2fe; margin-top:10px;">> Siz: ${userMsg}</div>`;
                
                // Serverga so'rov yuborish
                fetch('/get_analysis', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({prompt: userMsg})
                })
                .then(res => res.json())
                .then(data => {
                    scr.innerHTML += `<div style="margin-top:5px;">🤖 AI: ${data.response}</div>`;
                    scr.scrollTop = scr.scrollHeight;
                });

                inp.value = '';
            }
        </script>
    </body>
    </html>
    """)

@app.route('/get_analysis', methods=['POST'])
def analyze():
    data = request.json
    res = get_offline_analysis(data['prompt'])
    return jsonify({"response": res})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
