from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Tashkent Eco Live</title>
        <style>
            body { background: #050505; color: #00f2fe; font-family: 'Segoe UI', sans-serif; text-align: center; padding-top: 80px; }
            .main-card { border: 2px solid #00f2fe; display: inline-block; padding: 40px; border-radius: 30px; box-shadow: 0 0 30px rgba(0,242,254,0.3); background: #111; }
            .temp { font-size: 90px; font-weight: bold; margin: 10px 0; }
            .info { color: #fff; font-size: 18px; margin-bottom: 20px; }
            .status-ok { color: #0f0; font-size: 12px; }
        </style>
    </head>
    <body>
        <div class="main-card">
            <h2 style="letter-spacing: 5px;">TASHKENT</h2>
            <div class="info" id="desc">Ob-havo yuklanmoqda...</div>
            <div class="temp" id="temp">--°C</div>
            <div class="info">Namlik: <span id="hum">--</span>%</div>
            <p class="status-ok">● Live Data (No Token Required)</p>
        </div>

        <script>
            async function getStaticData() {
                try {
                    // Bu API kalit talab qilmaydi va bloklanmaydi
                    const res = await fetch('https://api.open-meteo.com/v1/forecast?latitude=41.2647&longitude=69.2163&current=temperature_2m,relative_humidity_2m,weather_code');
                    const data = await res.json();
                    
                    if(data.current) {
                        document.getElementById('temp').innerText = Math.round(data.current.temperature_2m) + "°C";
                        document.getElementById('hum').innerText = data.current.relative_humidity_2m;
                        document.getElementById('desc').innerText = "Hozirgi harorat va namlik";
                    }
                } catch(e) {
                    document.getElementById('desc').innerText = "Qayta yangilang";
                }
            }
            getStaticData();
        </script>
    </body>
    </html>
    """)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
