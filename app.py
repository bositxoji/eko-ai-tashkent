import os
import google.generativeai as genai
from flask import Flask, render_template_string, request

app = Flask(__name__)

GEMINI_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyCl-dBQmgQTJWgA5LR0Fy5Wiq7HLxaHK2Y")
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/')
def index():
    city = "Tashkent"
    # AI xabari tayyorlab qo'yiladi, lekin raqamlarni JS oladi
    ai_msg = "AI tizimi tayyor. Ma'lumotlar yuklanmoqda..."
    
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Neural Eco-Intelligence</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body { background: #050505; color: #fff; font-family: sans-serif; text-align: center; padding: 50px 20px; }
            .card { border: 1px solid #00f2fe; padding: 30px; border-radius: 25px; max-width: 400px; margin: auto; box-shadow: 0 0 20px rgba(0,242,254,0.2); }
            .aqi-num { font-size: 80px; color: #00f2fe; margin: 10px 0; }
            .details { display: flex; justify-content: space-around; margin-top: 20px; font-size: 14px; }
            .ai-box { background: rgba(0,242,254,0.1); padding: 15px; border-radius: 15px; margin: 20px 0; font-style: italic; }
        </style>
    </head>
    <body>
        <div class="card">
            <h2 id="city-name">YUKLANMOQDA...</h2>
            <div class="aqi-num" id="aqi-val">--</div>
            <p>HAVO SIFATI INDEKSI</p>
            <div class="ai-box" id="ai-text">{{ ai_msg }}</div>
            <div class="details">
                <div>TEMP: <span id="temp-val">--</span>°C</div>
                <div>HUM: <span id="hum-val">--</span>%</div>
            </div>
        </div>

        <script>
            async function getWeatherData() {
                try {
                    // To'g'ridan-to'g'ri ochiq API dan olish
                    const res = await fetch('https://api.waqi.info/feed/tashkent/?token=68f561578e030386d0800b656708306059b02a46');
                    const data = await res.json();
                    if(data.status === 'ok') {
                        document.getElementById('aqi-val').innerText = data.data.aqi;
                        document.getElementById('temp-val').innerText = data.data.iaqi.t.v;
                        document.getElementById('hum-val').innerText = data.data.iaqi.h.v;
                        document.getElementById('city-name').innerText = 'TASHKENT';
                    }
                } catch (e) {
                    document.getElementById('ai-text').innerText = "Ma'lumot olishda xatolik yuz berdi.";
                }
            }
            getWeatherData();
        </script>
    </body>
    </html>
    """, ai_msg=ai_msg)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
