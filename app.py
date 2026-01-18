from flask import Flask, render_template_string
import requests
import os

app = Flask(__name__)

def get_eco_status(city="Tashkent"):
    # Dunyo havo sifati API-si (demo token bilan)
    token = "demo"
    url = f"https://api.waqi.info/feed/{city}/?token={token}"
    
    try:
        r = requests.get(url).json()
        if r['status'] == 'ok':
            aqi = r['data']['aqi']
            
            # AI mantiqiy tahlili va tavsiyalari
            if aqi <= 50:
                return aqi, "A’lo ✅", "#2ecc71", "AI tavsiyasi: Havo juda toza! Tashqarida sayr qilish va sport bilan shug'ullanish uchun ajoyib vaqt. 🏃‍♂️"
            elif aqi <= 100:
                return aqi, "Qoniqarli ⚠️", "#f1c40f", "AI tavsiyasi: Havo holati o'rtacha. Sezgir odamlar (allergiya yoki nafas yo'li kasalliklari borlar) ehtiyot bo'lishi tavsiya etiladi. 😷"
            elif aqi <= 150:
                return aqi, "Nosog'lom 🟠", "#e67e22", "AI ogohlantirishi: Havo tarkibi hamma uchun biroz noqulay bo'lishi mumkin. Tashqarida kamroq vaqt o'tkazishga harakat qiling."
            else:
                return aqi, "Xavfli 🚨", "#e74c3c", "AI favqulodda ogohlantirishi: Havo o'ta ifloslangan! Derazalarni mahkam yoping, havo tozalagichlardan foydalaning va faqat zarurat bo'lganda ko'chaga chiqing. 🚨"
        
        return 0, "Noma'lum", "#34495e", "Hozirda ma'lumot olish imkonsiz."
    except Exception as e:
        return 0, "Xato", "#34495e", f"Tizimda xato yuz berdi: {str(e)}"

@app.route('/')
def home():
    # Toshkent shahri uchun ma'lumotlarni olish
    aqi_val, status_text, color_code, advice_text = get_eco_status("Tashkent")
    
    # Zamonaviy Dashboard dizayni (HTML/CSS)
    html_template = """
    <!DOCTYPE html>
    <html lang="uz">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Professional AI Monitoring Dashboard</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f0f2f5; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }
            .card { background: white; padding: 40px; border-radius: 30px; box-shadow: 0 20px 40px rgba(0,0,0,0.1); text-align: center; width: 380px; transition: transform 0.3s ease; }
            .card:hover { transform: translateY(-5px); }
            h2 { color: #2c3e50; margin-bottom: 5px; }
            .location { color: #7f8c8d; font-size: 0.9rem; margin-bottom: 25px; display: block; }
            .circle { width: 140px; height: 140px; border-radius: 50%; border: 12px solid {{color}}; margin: 0 auto 20px; display: flex; flex-direction: column; align-items: center; justify-content: center; transition: all 0.5s ease; }
            .aqi-value { font-size: 42px; font-weight: bold; color: {{color}}; }
            .aqi-label { font-size: 14px; color: #7f8c8d; font-weight: normal; }
            .status { font-size: 22px; font-weight: 600; color: {{color}}; margin-bottom: 15px; }
            .advice-box { background: #f8f9fa; padding: 20px; border-radius: 18px; border-left: 6px solid {{color}}; text-align: left; font-size: 0.95rem; color: #34495e; line-height: 1.5; margin-bottom: 25px; }
            .btn { background: {{color}}; color: white; border: none; padding: 14px 28px; border-radius: 15px; cursor: pointer; font-size: 16px; font-weight: bold; width: 100%; transition: opacity 0.3s; }
            .btn:hover { opacity: 0.85; }
            .footer-info { margin-top: 20px; font-size: 0.75rem; color: #bdc3c7; }
        </style>
    </head>
    <body>
        <div class="card">
            <h2>Toshkent</h2>
            <span class="location">O'zbekiston | Real-vaqt</span>
            
            <div class="circle">
                <div class="aqi-value">{{aqi}}</div>
                <div class="aqi-label">AQI</div>
            </div>
            
            <div class="status">{{status}}</div>
            
            <div class="advice-box">
                {{advice}}
            </div>
            
            <button class="btn" onclick="location.reload()">MALUMOTLARNI YANGILASH</button>
            
            <div class="footer-info">AI Eko-Monitoring Tizimi v1.0</div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_template, aqi=aqi_val, status=status_text, color=color_code, advice=advice_text)

if __name__ == "__main__":
    # Render va boshqa hostinglar uchun portni avtomatik aniqlash
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)