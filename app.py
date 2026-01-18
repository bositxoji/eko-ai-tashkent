import os
from flask import Flask, render_template_string, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="uz">
    <head>
        <meta charset="UTF-8">
        <title>ECO-AI-WORLD | NASA & Science</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            :root { --neon: #00f2fe; --bg: #000; --glass: rgba(255,255,255,0.05); }
            body { background: var(--bg); color: #fff; font-family: 'Segoe UI', sans-serif; margin: 0; }
            nav { display: flex; justify-content: space-between; padding: 15px 40px; border-bottom: 2px solid var(--neon); background: #080808; position: sticky; top: 0; z-index: 1000; }
            .container { max-width: 1400px; margin: auto; padding: 20px; }
            
            /* 12 TA SHAHAR */
            .city-scroll { display: flex; overflow-x: auto; gap: 15px; padding-bottom: 15px; scrollbar-width: none; }
            .city-card { min-width: 140px; background: #111; border: 1px solid #333; border-radius: 12px; padding: 15px; text-align: center; border-left: 3px solid var(--neon); }
            .temp { font-size: 24px; color: var(--neon); font-weight: bold; }

            .main-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; margin-top: 10px; }
            .glass { background: var(--glass); border: 1px solid rgba(255,255,255,0.1); border-radius: 15px; padding: 20px; }
            
            /* NASA & LIBRARY */
            .lib-link { display: flex; align-items: center; background: #111; padding: 12px; margin-bottom: 10px; border-radius: 8px; text-decoration: none; color: #fff; border: 1px solid #222; transition: 0.3s; }
            .lib-link:hover { border-color: var(--neon); transform: translateX(5px); }
            .lib-icon { font-size: 20px; margin-right: 12px; }

            iframe { width: 100%; height: 350px; border-radius: 15px; border: 1px solid var(--neon); }
            textarea { width: 100%; background: #000; border: 1px solid #444; color: #fff; padding: 12px; border-radius: 8px; margin-top: 10px; }
            .btn { background: var(--neon); color: #000; border: none; padding: 10px 20px; border-radius: 5px; font-weight: bold; cursor: pointer; }
            #ai-box { height: 200px; background: #050505; padding: 15px; border-radius: 10px; overflow-y: auto; color: var(--neon); border: 1px solid #222; }
        </style>
    </head>
    <body>
        <nav>
            <div style="font-size: 22px; font-weight: bold; color: var(--neon);">ECO-AI-WORLD</div>
            <div style="text-align: right; font-size: 11px;">Muallif: <b>A.A Ataxojayev</b> | Rahbar: <b>E.A Egamberdiev</b></div>
        </nav>

        <div class="container">
            <div class="city-scroll" id="cities"></div>

            <div class="main-grid">
                <div class="glass">
                    <h3>🌍 GLOBAL MONITORING</h3>
                    <iframe src="https://earth.nullschool.net/#current/wind/surface/level/orthographic=69.21,41.26,1000"></iframe>
                    <p style="font-size: 12px; color: #888; margin-top: 10px;">NASA va NOAA ma'lumotlari asosida jonli havo oqimi.</p>
                </div>

                <div class="glass">
                    <h3>🤖 SMART AI EXPERT</h3>
                    <div id="ai-box">Salom! Men NASA va ekologik ma'lumotlar bazasi bilan ishlovchi aqlli tizimman.</div>
                    <textarea id="
