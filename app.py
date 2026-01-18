import os
from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def index():
    # API kalitlarini to'g'ridan-to'g'ri JavaScript-ga beramiz
    # Bu usulda server blokirovkalari aylanib o'tiladi
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="uz">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Eco AI World | Tashkent</title>
        <style>
            body { background: #050505; color: #fff; font-family: 'Segoe UI', sans-serif; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }
            .card { background: #111; padding: 40px; border-radius: 30px; border: 2px solid #00f2fe; box-shadow: 0 0 30px rgba(0,242,254,0.2); text-align: center; width: 90%; max-width: 400px; }
            .aqi-val { font-size: 100px; font-weight: bold; color: #00f2fe; margin: 10px 0; }
            .ai-box { background: rgba(0,242,254,0.05); padding: 20px; border-radius: 15px; border-left: 5px solid #00f2fe; margin: 20px 0; text-align: left; font-style: italic; font-size: 14px; }
            .grid { display: flex; justify-content: space-around; border-top: 1px solid #222; padding-top: 20px; }
            .item b { color: #00f2fe; font-size: 18px; }
            .loader { color: #555; font-size: 12px; }
        </style>
    </head>
    <body>
        <div class="card">
            <h2 style="letter-spacing: 3px; color: #00f2fe;">TASHKENT</h2>
            <div class="aqi-val" id="aqi">--</div>
            <p style="color: #666; font-size: 12px;">HAVO SIFATI INDEKSI</p>
            
            <div class="ai-box" id="ai-msg">AI tahlil qilmoqda...</div>
            
            <div class="grid">
                <div class="item">TEMP<br><b id="temp">--</b>°C</div>
                <div class="item">NAMLYK<br><b id="hum">--</b>%</div>
            </div>
            <p class="loader" id="status">Tizim ulanmoqda...</p>
        </div>

        <script>
            const WAQI_TOKEN = "68f561578e030386d0800b656708306059b02a46";
            const GEMINI_KEY = "AIzaSyCl-dBQmgQTJWgA5LR0Fy5Wiq7HLxaHK2Y";

            async function fetchData() {
                try {
                    // 1. Havo ma'lumotlarini olish (Brauzer orqali)
                    const response = await fetch(`https://api.waqi.info/feed/tashkent/?token=${WAQI_TOKEN}`);
                    const data = await response.json();
                    
                    if (data.status === 'ok') {
                        const aqi = data.data.aqi;
                        document.getElementById('aqi').innerText = aqi;
                        document.getElementById('temp').innerText = data.data.iaqi.t.v;
                        document.getElementById('hum').innerText = data.data.iaqi.h.v;
                        document.getElementById('status').innerText = "Ma'lumotlar yangilandi";

                        // 2. Gemini AI tahlili (Brauzer orqali)
                        const aiResponse = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${GEMINI_KEY}`, {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({
                                contents: [{ parts: [{ text: `Havo AQI indeksi ${aqi}. 1 ta qisqa jumlada o'zbek tilida maslahat ber.` }] }]
                            })
                        });
                        const aiData = await aiResponse.json();
                        document.getElementById('ai-msg').innerText = aiData.candidates[0].content.parts[0].text;
                    }
                } catch (error) {
                    document.getElementById('status').innerText = "Ulanishda xatolik!";
                    document.getElementById('ai-msg').innerText = "AI hozircha ma'lumotni tahlil qila olmaydi.";
                }
            }
            fetchData();
        </script>
    </body>
    </html>
    """)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
