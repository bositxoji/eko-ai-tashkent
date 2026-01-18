from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="uz">
    <head>
        <meta charset="UTF-8">
        <title>Neural Eco v3.6 | Ultimate Global Hub</title>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            :root { --neon: #00f2fe; --bg: #020202; --glass: rgba(255,255,255,0.05); }
            body { background: var(--bg); color: #fff; font-family: 'Segoe UI', sans-serif; margin: 0; scroll-behavior: smooth; }
            .glass { background: var(--glass); backdrop-filter: blur(15px); border: 1px solid rgba(255,255,255,0.1); border-radius: 20px; padding: 25px; margin-bottom: 25px; }
            
            nav { display: flex; justify-content: space-between; align-items: center; padding: 15px 40px; background: rgba(0,0,0,0.9); position: sticky; top: 0; z-index: 1000; border-bottom: 1px solid var(--neon); }
            .lang-btn { background: none; border: 1px solid var(--neon); color: var(--neon); padding: 5px 12px; cursor: pointer; border-radius: 8px; font-weight: bold; margin-left: 8px; transition: 0.3s; }
            .lang-btn.active { background: var(--neon); color: #000; }

            .container { max-width: 1300px; margin: auto; padding: 20px; }
            h2 { color: var(--neon); text-align: center; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 30px; }

            /* Real-Time City Monitoring */
            .city-scroll { display: flex; overflow-x: auto; gap: 15px; padding: 15px 0; border-bottom: 1px solid #222; }
            .city-card { min-width: 160px; text-align: center; border: 1px solid #333; padding: 15px; border-radius: 15px; background: #0a0a0a; }

            /* AI Section */
            #ai-display { min-height: 250px; background: #050505; border: 1px solid #222; border-radius: 15px; padding: 20px; margin-bottom: 15px; line-height: 1.8; color: #d1d1d1; overflow-y: auto; }
            textarea { width: 100%; background: #111; border: 1px solid #333; color: #fff; padding: 15px; border-radius: 12px; box-sizing: border-box; outline: none; }

            /* Map & External Sites */
            .map-container { height: 500px; border-radius: 25px; overflow: hidden; border: 1px solid var(--neon); box-shadow: 0 0 20px rgba(0, 242, 254, 0.2); }
            .link-card { display: block; background: #111; border: 1px solid #222; padding: 15px; border-radius: 12px; color: #fff; text-decoration: none; margin-bottom: 10px; transition: 0.3s; }
            .link-card:hover { border-color: var(--neon); background: rgba(0, 242, 254, 0.05); }

            /* Game UI */
            .bin { border: 2px solid #333; padding: 15px; border-radius: 15px; cursor: pointer; transition: 0.3s; font-weight: bold; text-align: center; }
            .bin:hover { border-color: var(--neon); background: rgba(0, 242, 254, 0.1); }
            .btn-neon { background: var(--neon); color: #000; border: none; padding: 12px 25px; border-radius: 10px; font-weight: bold; cursor: pointer; margin-top: 10px; }
        </style>
    </head>
    <body>

    <nav>
        <div style="font-weight: bold; letter-spacing: 1px;">NEURAL ECO <span style="color:var(--neon)">HUB</span></div>
        <div style="display:flex;">
            <button class="lang-btn active" onclick="setLang('uz', this)">UZ</button>
            <button class="lang-btn" onclick="setLang('ru', this)">RU</button>
            <button class="lang-btn" onclick="setLang('en', this)">EN</button>
        </div>
    </nav>

    <div class="container">
        
        <section id="monitor-sec">
            <h2 id="t-mon">Global Monitoring (Real-Time)</h2>
            <div class="city-scroll" id="city-list"></div>
        </section>

        <div class="glass">
            <h2 id="t-map">Jonli Shamol va Iqlim Oqimi</h2>
            <div class="map-container">
                <iframe src="https://earth.nullschool.net/#current/wind/surface/level/orthographic=69.21,41.26,1200" style="width:100%; height:100%; border:none;"></iframe>
            </div>
        </div>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 25px;">
            <div class="glass">
                <h2 id="t-fore">Prognoz 2025-2080</h2>
                <canvas id="forecastChart"></canvas>
                <p style="font-size:12px; color:#888; margin-top:15px;" id="t-hist">Siyosiy-tarixiy tahlil: 2045-yilda global uglerod solig'i joriy etilishi prognoz qilinmoqda.</p>
            </div>
            <div class="glass">
                <h2 id="t-eco">Eko Resurslar (Vazifa 2)</h2>
                <a href="https://earth911.com" target="_blank" class="link-card">🌐 Earth911 - Recycling Directory</a>
                <a href="https://news.mongabay.com" target="_blank" class="link-card">🍃 Mongabay - Environmental News</a>
                <a href="https://oceana.org" target="_blank" class="link-card">🌊 Oceana - Protect Global Oceans</a>
            </div>
        </div>

        <section class="glass">
            <h2 id="t-ai">Eco AI Expert (Streaming)</h2>
            <div id="ai-display">AI tizimi tayyor. Ekologik savolingizni bering...</div>
            <textarea id="ai-input" rows="3" placeholder="Masalan: Okean ifloslanishining oldini olish yo'llari..."></textarea>
            <div style="display:flex; gap:10px; margin-top:15px;">
                <button class="btn-neon" id="b-send" onclick="runAI()">YUBORISH</button>
                <button class="btn-neon" style="background:#ff4b2b; color:#fff;" onclick="exportDoc('pdf')">PDF</button>
                <button class="btn-neon" style="background:#2b55ff; color:#fff;" onclick="exportDoc('word')">WORD</button>
            </div>
        </section>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 25px;">
            <div class="glass" style="border-color: #0033a0;">
                <h2>🚀 NASA (Vazifa 3)</h2>
                <p id="t-nasa">NASA Climate Monitoring va kosmik tadqiqotlar bo'limi.</p>
                <a href="https://www.nasa.gov" target="_blank" class="btn-neon" style="display:block; text-align:center; background:#0033a0; color:#fff;">NASA OFFICIAL</a>
                <a href="https://climate.nasa.gov" target="_blank" class="link-card" style="margin-top:20px;">NASA Global Climate News</a>
            </div>
            <div class="glass">
                <h2 id="t-game">Eco Game (Ballli)</h2>
                <div style="text-align:center">
                    <div id="game-emoji" style="font-size:60px; margin-bottom:15px;">🧴</div>
                    <p id="t-sort">Ushbu chiqindini qayerga tashlaysiz?</p>
                    <div style="display:grid; grid-template-columns: 1fr 1fr; gap:10px;">
                        <div class="bin" onclick="checkGame('plastic')">PLASTIK</div>
                        <div class="bin" onclick="checkGame('organic')">ORGANIK</div>
                        <div class="bin" onclick="checkGame('paper')">QOG'OZ</div>
                        <div class="bin" onclick="checkGame('hazard')">XAVFLI</div>
                    </div>
                    <h3 style="margin-top:20px;">Score: <span id="game-score" style="color:var(--neon)">0</span></h3>
                </div>
            </div>
        </div>
    </div>

    <script>
