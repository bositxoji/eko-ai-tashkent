import os
import requests
import google.generativeai as genai
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# --- AI SOZLAMALARI ---
# Gemini sozlamasi
GEMINI_KEY = "AIzaSyCl-dBQmgQTJWgA5LR0Fy5Wiq7HLxaHK2Y"
genai.configure(api_key=GEMINI_KEY)
gemini_model = genai.GenerativeModel('gemini-1.5-flash')

# Llama 3 sozlamasi (Groq bepul API orqali)
LLAMA_KEY = "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" # Test uchun

def get_dual_ai_response(prompt):
    # 1. Avval Gemini bilan urinib ko'ramiz
    try:
        response = gemini_model.generate_content(f"Sen ECO-AI yordamchisisan. O'zbek tilida javob ber: {prompt}")
        return f"✨ Gemini: {response.text}"
    except Exception as e:
        print(f"Gemini xatosi: {e}")
        
        # 2. Agar Gemini ishlamasa, Llama 3 (Groq) ishga tushadi
        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {"Authorization": f"Bearer {LLAMA_KEY}", "Content-Type": "application/json"}
            data = {
                "model": "llama3-8b-8192",
                "messages": [{"role": "user", "content": f"Answer in Uzbek: {prompt}"}]
            }
            res = requests.post(url, json=data, headers=headers, timeout=10)
            return f"🦙 Llama 3: {res.json()['choices'][0]['message']['content']}"
        except:
            return "⚠️ Xatolik: Ikkala AI modeli ham vaqtincha aloqaga chiqmayapti. Iltimos, internetni tekshiring."

# --- WEB INTERFEYS ---
@app.route('/')
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="uz">
    <head>
        <meta charset="UTF-8">
        <title>ECO-AI-WORLD | AI CORE</title>
        <style>
            body { background: #000; color: #fff; font-family: 'Courier New', monospace; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
            .terminal { width: 90%; max-width: 800px; background: #050505; border: 2px solid #00f2fe; border-radius: 10px; padding: 20px; box-shadow: 0 0 30px rgba(0,242,254,0.2); }
            .log { height: 400px; overflow-y: auto; border-bottom: 1px solid #333; margin-bottom: 20px; padding: 10px; font-size: 14px; line-height: 1.5; color: #00f2fe; }
            .input-area { display: flex; gap: 10px; }
            textarea { flex: 1; background: #111; border: 1px solid #444; color: #fff; padding: 10px; border-radius: 5px; outline: none; }
            button { background: #00f2fe; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="terminal">
            <div style="color: #00f2fe; font-weight: bold; margin-bottom: 10px;">> ECO-AI-SYSTEM ONLINE...</div>
            <div class="log" id="log">Tizim tayyor. Savolingizni kutmoqdaman...</div>
            <div class="input-area">
                <textarea id="prompt" placeholder="Ekologik tahlil uchun savol yozing..."></textarea>
                <button onclick="send()">YUBORISH</button>
            </div>
        </div>
        <script>
            async function send() {
                const p = document.getElementById('prompt');
                const log = document.getElementById('log');
                if(!p.value) return;
                
                log.innerHTML += `<p style="color:#888;">> Siz: ${p.value}</p>`;
                log.scrollTop = log.scrollHeight;
                
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({prompt: p.value})
                });
                const data = await response.json();
                
                log.innerHTML += `<p style="color:#00f2fe;">> ${data.response}</p>`;
                log.scrollTop = log.scrollHeight;
                p.value = '';
            }
        </script>
    </body>
    </html>
    """)

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('prompt')
    ai_text = get_dual_ai_response(user_input)
    return jsonify({"response": ai_text})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
