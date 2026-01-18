from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="uz">
    <head>
        <meta charset="UTF-8">
        <title>Eco AI World | Live</title>
        <style>
            body { background: #050505; color: #fff; font-family: sans-serif; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }
            .card { background: #111; padding: 40px; border-radius: 30px; border: 2px solid #00f2fe; text-align: center; width: 90%; max-width: 400px; box-shadow: 0 0 30px rgba(0,242,254,0.2); }
            .aqi-val { font-size: 100px; font-weight: bold; color: #00f2fe; margin: 10px 0; }
            .ai-box { background: rgba(0,242,254,0.1); padding: 20px; border-radius: 15px; margin: 20px 0; font-size: 14px; border-left: 5px solid #00f2fe; text-align: left; }
            .grid { display: flex; justify-content: space-around; margin-top: 20px; }
            b { color: #00f2fe; font-size: 20px; }
        </style>
    </head>
    <body>
        <div class="card">
            <h2 style="color: #00f2fe; letter-spacing: 3px;">TASHKENT LIVE</h2>
            <div class="aqi-val" id="aqi">...</div>
            <p style="color: #666;">HAVO SIFATI INDEKSI</p>
            <div class="ai-box" id="ai">AI ma'lumotlarni tahlil qilmoqda...</div>
            <div class="grid">
                <div>TEMP<br><b id="t">--</b>°C</div>
                <div>NAMLYK<br><b id="h">--</b>%</div>
            </div>
        </div>

        <script>
            async function start() {
                try {
                    // 1. Havo ma'lumotini olish (To'g'ridan-to'g'ri brauzerdan)
                    const res = await fetch('https://api.waqi.info/feed/tashkent/?token=68f561578e030386d0800b656708306059b02a46');
                    const d = await res.json();
                    if(d.status === 'ok') {
                        document.getElementById('aqi').innerText = d.data.aqi;
                        document.getElementById('t').innerText = d.data.iaqi.t.v;
                        document.getElementById('h').innerText = d.data.iaqi.h.v;

                        // 2. AI Tahlili
                        const aiRes = await fetch('https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=AIzaSyCl-dBQmgQTJWgA5LR0Fy5Wiq7HLxaHK2Y', {
                            method: 'POST',
                            body: JSON.stringify({contents: [{parts: [{text: "Havo AQI " + d.data.aqi + ". O'zbek tilida 1 ta qisqa maslahat ber."}]}]})
                        });
                        const aiD = await aiRes.json();
                        document.getElementById('ai').innerText = aiD.candidates[0].content.parts[0].text;
                    }
                } catch(e) { document.getElementById('ai').innerText = "Qayta yuklang..."; }
            }
            start();
        </script>
    </body>
    </html>
    """)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
