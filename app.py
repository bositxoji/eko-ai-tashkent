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
            
            # AI Mantiqiy Tahlili (Ranglar va Tavsiyalar)
            if aqi <= 50:
                return aqi, "A’lo ✅", "#2ecc71", "AI tavsiyasi: Havo juda toza! Tashqarida sayr qilish, yugurish va derazalarni ochib qo'yish uchun ajoyib vaqt. 🏃‍♂️"
            elif aqi <= 100:
                return aqi, "Qoniqarli ⚠️", "#f1c40f", "AI tavsiyasi: Havo holati o'rtacha. Sezgir odamlar (allergiya borlar) uzoq vaqt ko'chada qolmagani ma'qul. 😷"
            elif aqi <= 150:
                return aqi, "Nosog'lom 🟠", "#e67e22", "AI ogohlantirishi: Havo tarkibi buzilmoqda. Yosh bolalar va keksalar ko'chaga chiqishni kamaytirishi kerak."
            else:
                return aqi, "Xavfli 🚨", "#e74c3c", "AI favqulodda ogohlantirishi: Havo o'ta ifloslangan! Niqob taqing, derazalarni yoping va uyda qoling. 🚨"
        
        return 0, "Noma'lum", "#34495e", "Hozirda ma'lumot olish imkonsiz."
    except Exception as e:
        return 0, "Xato", "#34495e", f"Tizimda xato yuz berdi: {str(e)}"

@app.route('/')
def home():
    aqi_val, status_text, color_code, advice_text = get_eco_status("Tashkent")
    
    # HTML shablon (Google SEO va Mobile Design bilan)
    html_template = """
    <!DOCTYPE html>
    <html lang="uz">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        
        <title>Eko-AI | Toshkent Havo Sifati Monitoringi</title>
        <meta name="description" content="Toshkent shahri uchun real vaqtda ishlovchi sun'iy intellekt (AI) Eko-monitoring tizimi. Havo sifati, AQI darajasi va salomatlik bo'yicha tavsiyalar.">
        <meta name="keywords" content="eko-ai, eko ai, havo toshkent, aqi uzbekistan, havo monitoringi, eko monitoring, toshkent havo sifati">
        <meta name="author" content="Eko-AI Team">
        
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f0f2f5; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; padding: 20px; box-sizing: border-box; }
            .card { background: white; padding: 40px; border-radius: 30px; box-shadow: 0 20px 40px rgba(0,0,0,0.1); text-align: center; width: 100%; max-width: 400px; transition: transform 0.3s ease; }
            .card:hover { transform: translateY(-5px); }
            h1 { color: #2c3e50; margin-bottom: 5px; font-size: 28px; }
            .location { color: #7f8c8d; font-size: 0.9rem; margin-bottom: 25px; display: block; text-transform: uppercase; letter-spacing: 1px; }
            .circle { width: 150px; height: 150px; border-radius: 50%; border: 15px solid {{color}}; margin: 0 auto 25px; display: flex; flex-direction: column; align-items: center; justify-content: center; position: relative; }
            .aqi-value { font-size: 48px; font-weight: bold; color: {{color}}; line-height: 1; }
            .aqi-label { font-size: 14px; color: #95a5a6; margin-top: 5px; }
            .status { font-size: 24px; font-weight: 700; color: {{color}}; margin-bottom: 20px; }
            .advice-box { background: #f8f9fa; padding: 20px; border-radius: 15px; border-left: 5px solid {{color}}; text-align: left; font-size: 0.95rem; color: #555; line-height: 1.6; margin-bottom: 30px; }
            .btn { background: {{color}}; color: white; border: none; padding: 15px 30px; border-radius: 15px; cursor: pointer; font-size: 16px; font-weight: bold; width: 100%; box-shadow: 0 5px 15px rgba(0,0,0,0.1); transition: opacity 0.3s; }
            .btn:hover { opacity: 0.85; }
            .footer { margin-top: 25px; font-size: 0.8rem; color: #bdc3c7; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>Eko-AI Monitoring</h1>
            <span class="location">Toshkent, O'zbekiston</span>
            
            <div class="circle">
                <div class="aqi-value">{{aqi}}</div>
                <div class="aqi-label">AQI INDEX</div>
            </div>
            
            <div class="status">{{status}}</div>
            
            <div class="advice-box">
                <strong>💡 AI Xulosasi:</strong><br>
                {{advice}}
            </div>
            
            <button class="btn" onclick="location.reload()">🔄 Yangilash</button>
            
            <div class="footer">Eko-AI Tizimi v2.0 | Real-vaqt rejimi</div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_template, aqi=aqi_val, status=status_text, color=color_code, advice=advice_text)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
