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
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Eco AI World | Tashkent</title>
        <style>
            body { background: #050505; color: #fff; font-family: sans-serif; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }
            .card { background: #111; padding: 40px; border-radius: 30px; border: 2px solid #00f2fe; box-shadow: 0 0 30px rgba(0,242,254,0.2); text-align: center; width: 90%; max-width: 400px; }
            .aqi-val { font-size: 100px; font-weight: bold; color: #00f2fe; margin: 10px 0; }
            .ai-box { background: rgba(0,242,254,0.05); padding: 15px; border-radius: 15px; border-left: 5px solid #00f2fe; margin: 20px 0; text-align: left; font-size: 14px; min-height: 50px; }
            .grid { display: flex; justify-content: space-around; border-top: 1px solid #222; padding-top: 20px; }
            b { color: #00f2fe; font-size: 18px; }
        </style>
    </head>
    <body>
        <div class="card">
            <h2 style="letter-spacing: 3px; color: #00f2fe;">TASHKENT</h2>
            <div class="aqi-val" id="aqi_display">--</div>
            <p style="color: #666; font-size: 12px; letter-spacing: 2px;">HAVO SIFATI INDEKSI</p>
            
            <div class="ai-box" id="ai_status">AI tahlil qilmoqda...</div>
            
            <div class="grid">
                <div class="item">TEMP<br><b id="temp_display">--</b>°C</div>
                <div class="item">NAMLYK<br><b id="hum_display">--</b>%</div>
            </div>
        </div>

        <script>
            // API ma'lumotlarini brauzerning o'zida chaqiramiz (Server cheklovlarini aylanib o'tish)
            async function loadEcoData() {
                const token = "68f561578e030386d0800b656708306059b02a46";
                const gemini_key = "AIzaSyCl-dBQmgQTJWgA5LR0Fy5Wiq7HLxaHK2Y";
                
                try {
                    // 1. Havo ma'lumotlarini olish
                    const response = await fetch(`https://api.waqi.info/feed/tashkent/?token=${token}`);
                    const result = await response.json();
                    
                    if(result.status === 'ok') {
                        const val = result.data;
                        document.getElementById('aqi_display').innerText = val.aqi;
                        document.getElementById('temp_display').innerText = val.iaqi.t ? val.iaqi.t.v : "20";
                        document.getElementById('hum_display').innerText = val.iaqi.h ? val.iaqi.h.v : "35";
                        
                        // 2. Gemini AI tahlilini brauzer orqali yuborish
                        const ai_res = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${gemini_key}`, {
                            method: 'POST',
                            headers: {'Content-Type': 'application/json'},
                            body: JSON.stringify({
                                contents: [{parts: [{text: "Havo AQI indeksi " + val.aqi + ". O'zbek tilida 1 ta qisqa gapda maslahat ber."}]}]
                            })
                        });
                        const ai_data = await ai_res.json();
                        document.getElementById('ai_status').innerText = ai_data.candidates[0].content.parts[0].text;
                    }
                } catch (e) {
                    document.getElementById('ai_status').innerText = "Hozircha ma'lumot yuklanmadi. Iltimos, sahifani yangilang.";
                }
            }
            loadEcoData();
        </script>
    </body>
    </html>
    """)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
