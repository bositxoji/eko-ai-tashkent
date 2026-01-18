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
        <title>Neural Eco-Intelligence | Global Portal</title>
        <style>
            :root { --neon: #00f2fe; --bg: #050505; }
            body { background: var(--bg); color: #fff; font-family: 'Segoe UI', sans-serif; margin: 0; padding: 20px; }
            .container { max-width: 1200px; margin: auto; }
            header { text-align: center; padding: 40px 0; border-bottom: 1px solid #222; }
            h1 { color: var(--neon); letter-spacing: 5px; text-transform: uppercase; }
            
            /* 1-Vazifa: Shaharlar Paneli */
            .city-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-top: 30px; }
            .city-card { background: #111; border: 1px solid #333; padding: 20px; border-radius: 20px; transition: 0.3s; }
            .city-card:hover { border-color: var(--neon); transform: translateY(-5px); }
            .city-card h3 { color: var(--neon); margin: 0 0 10px 0; }
            .temp-val { font-size: 32px; font-weight: bold; }

            /* 2 & 3-Vazifa: Tashqi Linklar */
            .sections { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 40px; }
            .link-box { background: linear-gradient(145deg, #1a1a1a, #0a0a0a); padding: 30px; border-radius: 25px; border: 1px solid #444; }
            .link-box h2 { color: var(--neon); font-size: 20px; border-bottom: 1px solid #333; padding-bottom: 10px; }
            .link-list a { display: block; color: #aaa; text-decoration: none; padding: 10px 0; border-bottom: 1px solid #222; transition: 0.2s; }
            .link-list a:hover { color: var(--neon); padding-left: 10px; }
            .nasa-btn { background: #0033a0; color: white !important; padding: 15px !important; border-radius: 10px; text-align: center; font-weight: bold; margin-top: 15px; }
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>Neural Eco-Intelligence</h1>
                <p>Global Ekologik va Koinot Monitoringi Portal</p>
            </header>

            <div class="city-grid" id="cities">
                </div>

            <div class="sections">
                <div class="link-box">
                    <h2>🌱 EKOLOGIK RESURSLAR</h2>
                    <div class="link-list">
                        <a href="https://earth911.com" target="_blank">Earth911 - Qayta ishlash bo'yicha qo'llanma</a>
                        <a href="https://news.mongabay.com" target="_blank">Mongabay - Tabiat yangiliklari</a>
                        <a href="https://oceana.org" target="_blank">Oceana - Okeanlarni himoya qilish</a>
                    </div>
                </div>

                <div class="link-box" style="border-color: #0033a0;">
                    <h2>🚀 NASA & KOINOT BILIMLARI</h2>
                    <p style="font-size: 14px; color: #888;">Yer sayyorasi va koinot haqidagi eng so'nggi yangiliklar va kashfiyotlar.</p>
                    <div class="link-list">
                        <a href="https://www.nasa.gov" target="_blank" class="nasa-btn">NASA RASMIY SAYTI</a>
                        <a href="https://climate.nasa.gov" target="_blank">NASA Climate - Iqlim o'zgarishi</a>
                        <a href="https://images.nasa.gov" target="_blank">NASA Galereya - Koinot suratlari</a>
                    </div>
                </div>
            </div>
        </div>

        <script>
            const cities = [
                {n: "Toshkent", lat: 41.26, lon: 69.21},
                {n: "Berlin", lat: 52.52, lon: 13.40},
                {n: "Pekin", lat: 39.90, lon: 116.40},
                {n: "Seul", lat: 37.56, lon: 126.97},
                {n: "Tokio", lat: 35.68, lon: 139.65},
                {n: "Moskva", lat: 55.75, lon: 37.61},
                {n: "Istanbul", lat: 41.00, lon: 28.97},
                {n: "Qohira", lat: 30.04, lon: 31.23},
                {n: "Rio De Janero", lat: -22.90, lon: -43.17},
                {n: "Bogota", lat: 4.71, lon: -74.07},
                {n: "Washington", lat: 38.89, lon: -77.03},
                {n: "Ottawa", lat: 45.42, lon: -75.69}
            ];

            async function loadCities() {
                const grid = document.getElementById('cities');
                for (let c of cities) {
                    try {
                        const res = await fetch(`https://api.open-meteo.com/v1/forecast?latitude=${c.lat}&longitude=${c.lon}&current=temperature_2m,relative_humidity_2m`);
                        const data = await res.json();
                        
                        grid.innerHTML += `
                            <div class="city-card">
                                <h3>${c.n}</h3>
                                <div class="temp-val">${Math.round(data.current.temperature_2m)}°C</div>
                                <div style="color: #666; font-size: 14px;">Namlik: ${data.current.relative_humidity_2m}%</div>
                            </div>
                        `;
                    } catch(e) { console.log(c.n + " yuklanmadi"); }
                }
            }
            loadCities();
        </script>
    </body>
    </html>
    """)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
