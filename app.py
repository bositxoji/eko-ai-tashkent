import streamlit as st
import datetime
import pandas as pd
from groq import Groq

# 1. GOOGLE VERIFICATION & API SOZLAMASI
GOOGLE_VERIFICATION_CODE = """
<head>
    <meta name="google-site-verification" content="ZkAtTf6Ut4FM76-c3qns2vqHjD4OZLKIxw_i2iw7bTY" />
</head>
"""

client = Groq(api_key="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")

# 2. SAHIFA SOZLAMALARI
st.set_page_config(page_title="ECO AI WORLD | Enterprise", page_icon="🧬", layout="wide")
st.markdown(GOOGLE_VERIFICATION_CODE, unsafe_allow_html=True)

# 3. PREMIUM DIZAYN
st.markdown("""
    <style>
    .stApp { background-color: #0E1116; color: #A0A0A0; }
    [data-testid="stSidebar"] { background-color: #050505 !important; border-right: 1px solid #1C1F26; }
    .author-box { padding: 15px; background: rgba(28, 31, 38, 0.8); border-radius: 8px; border-left: 3px solid #FFD400; margin-bottom: 20px; }
    .author-title { color: #FFD400; font-size: 11px; font-weight: bold; margin: 0; }
    .author-name { color: #FFFFFF; font-size: 13px; margin-bottom: 8px; }
    .main-card { background: #1C1F26; padding: 25px; border-radius: 8px; border-left: 4px solid #FF3B3B; margin-bottom: 20px; }
    h1, h2 { color: #FFFFFF !important; font-family: 'Inter', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# --- NAVIGATSIYA ---
with st.sidebar:
    st.markdown("<h1>💠 ECO NAVIGATION</h1>", unsafe_allow_html=True)
    st.markdown(f"""<div class="author-box">
        <p class="author-title">Ilmiy rahbar:</p><p class="author-name">E. EGAMBERDIEV</p>
        <p class="author-title">Muallif:</p><p class="author-name">A. ATAXOJAYEV</p>
        <p class="author-title">Team:</p><p class="author-name">Egamberdiev</p>
    </div>""", unsafe_allow_html=True)
    page = st.radio("MENYU:", ["1. Monitoring Terminal (Asosiy)", "6. 🧠 AI CORE (Llama 3 Yadro)", "7. YOUR BODY vs ENV.", "8. SILENT DISASTER"])
    st.success("Tizim 2026-yil holatida.")

# =================================================================
# 1. MONITORING TERMINAL
# =================================================================
if page == "1. Monitoring Terminal (Asosiy)":
    st.title("📟 ECO AI WORLD: GLOBAL MONITORING")
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.link_button("💨 IQAIR", "https://www.iqair.com/")
    with col2: st.link_button("🚀 NASA FIRMS", "https://firms.modaps.eosdis.nasa.gov/map/")
    with col3: st.link_button("🤖 GROK AI", "https://grok.com")
    with col4: st.link_button("🛰️ SENTINEL", "https://apps.sentinel-hub.com/eo-browser/")
    st.components.v1.iframe("https://earth.nullschool.net/#current/wind/surface/level/orthographic=-296.22,40.06,500", height=600)

# =================================================================
# 6. 🧠 AI CORE (MUAMMO SHU YERDA HAL ETILDI)
# =================================================================
elif page == "6. 🧠 AI CORE (Llama 3 Yadro)":
    st.title("🤖 AI CORE: Llama 3 Intelligence")
    user_input = st.text_input("Ekologik savol bering:", placeholder="Masalan: 2030-yilda iqlim...")
    
    if st.button("Tahlilni boshlash"):
        if user_input:
            with st.spinner('AI tizimi tahlil qilmoqda...'):
                # AVTOMATIK MODEL ALMASHTIRISH (Xatoga o'rin yo'q)
                models_to_try = ["llama-3.3-70b-versatile", "llama3-70b-8192", "mixtral-8x7b-32768"]
                response_received = False
                
                for model_name in models_to_try:
                    if response_received: break
                    try:
                        completion = client.chat.completions.create(
                            messages=[{"role": "system", "content": "Professional AI ekolog."}, {"role": "user", "content": user_input}],
                            model=model_name
                        )
                        st.markdown(f'<div style="background:black; padding:20px; border-left: 5px solid #FFD400;"><b>AI HUKMI ({model_name}):</b><br><br>{completion.choices[0].message.content}</div>', unsafe_allow_html=True)
                        response_received = True
                    except:
                        continue # Agar model ishlamasa, keyingisiga o'tadi
                
                if not response_received:
                    st.error("Barcha AI modellari band yoki API kalitida xato bor.")

# Boshqa sahifalar (7 va 8) original holatda saqlangan...
elif page == "7. YOUR BODY vs ENV.":
    st.title("🫀 YOUR BODY vs ENVIRONMENT")
    st.write("Sizning yoshingiz bo'yicha ekologik tahlil.")
elif page == "8. SILENT DISASTER":
    st.title("🤫 THE SILENT THREAT")
    st.write("Jim falokat rejimi faol.")

st.markdown("<div style='text-align: center; border-top: 1px solid #1C1F26; padding: 20px;'>© 2026 ECO AI WORLD</div>", unsafe_allow_html=True)
