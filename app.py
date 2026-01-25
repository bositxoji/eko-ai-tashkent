import streamlit as st
import datetime
import pandas as pd
from groq import Groq  # Yangi kutubxona

# 1. API SOZLAMASI
client = Groq(api_key="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")

# 2. SAHIFA SOZLAMALARI
st.set_page_config(page_title="ECO AI WORLD | Enterprise", page_icon="🧬", layout="wide")

# 3. DIZAYN (Poydevor uslubi)
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at center, #001010 0%, #000000 100%); color: #00ff88; }
    .main-card { border: 1px solid #00ff88; border-radius: 12px; padding: 20px; background: rgba(0, 255, 136, 0.05); margin-bottom: 15px; }
    .ai-response { border-left: 5px solid #00d4ff; background: rgba(0, 212, 255, 0.1); padding: 15px; border-radius: 5px; color: #ffffff; }
    h1, h2, h3 { color: #00ff88 !important; text-shadow: 0 0 10px #00ff88; }
    [data-testid="stSidebar"] { background-color: #050505 !important; border-right: 1px solid #00ff88; }
    </style>
    """, unsafe_allow_html=True)

# --- NAVIGATSIYA (O'zbekcha-Inglizcha) ---
with st.sidebar:
    st.title("💠 ECO NAVIGATION")
    page = st.radio("MENYU / MENU:", [
        "1. Monitoring Terminal (Asosiy)", 
        "2. Water Quality (Suv sifati)", 
        "3. Soil Monitoring (Tuproq nazorati)",
        "4. Climate Change (Iqlim o'zgarishi)",
        "5. Disasters & Hazards (Tabiiy ofatlar)",
        "6. 🧠 AI CORE (Llama 3 Yadro)",
        "7. User Dashboard (Panel)"
    ])
    st.divider()
    st.success("Global ekologik monitoring tizimi.")

# =================================================================
# 1. MONITORING TERMINAL (POYDEVOR SAQLANDI)
# =================================================================
if page == "1. Monitoring Terminal (Asosiy)":
    st.title("📟 ECO AI WORLD: GLOBAL MONITORING")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="main-card"><h3>💨 IQAIR</h3><p>Havo sifati / Air Quality.</p></div>', unsafe_allow_html=True)
        st.link_button("Launch IQAir", "https://www.iqair.com/")
    with col2:
        st.markdown('<div class="main-card"><h3>🚀 NASA FIRMS</h3><p>Yong\'inlar / Fires.</p></div>', unsafe_allow_html=True)
        st.link_button("NASA FIRMS", "https://firms.modaps.eosdis.nasa.gov/map/")
    with col3:
        st.markdown('<div class="main-card"><h3>🤖 GROK AI</h3><p>AI Analitika / Analysis.</p></div>', unsafe_allow_html=True)
        st.link_button("Grok Chat", "https://grok.com")
    with col4:
        st.markdown('<div class="main-card"><h3>🛰️ SENTINEL</h3><p>Sputnik / Satellite.</p></div>', unsafe_allow_html=True)
        st.link_button("Sentinel-2", "https://apps.sentinel-hub.com/eo-browser/")

    st.divider()
    st.components.v1.iframe("https://earth.nullschool.net/#current/wind/surface/level/orthographic=-296.22,40.06,500", height=600)

# =================================================================
# 6. 🧠 AI CORE (LLAMA 3 REAL-TIME CHAT & DATA)
# =================================================================
elif page == "6. 🧠 AI CORE (Llama 3 Yadro)":
    st.title("🤖 AI CORE: Llama 3 Intelligence")
    
    st.markdown("""
    <div style="background: rgba(0, 212, 255, 0.1); padding: 20px; border-radius: 10px; border: 1px solid #00d4ff;">
        <h4>Llama 3: Ekologik Big Data Eksperti</h4>
        <p>Savollaringizga soniyalar ichida ilmiy javob oling.</p>
    </div>
    """, unsafe_allow_html=True)

    # Big Data Fayl Yuklash
    st.subheader("📊 Big Data Upload")
    up_file = st.file_uploader("Ekologik CSV faylni tahlil uchun yuklang", type=["csv"])
    if up_file:
        data = pd.read_csv(up_file)
        st.dataframe(data.head(10))
        st.info("Ma'lumotlar yuklandi. Llama 3 ularni tahlil qilishga tayyor.")

    st.divider()
    
    # AI Chat Bo'limi
    st.subheader("💬 AI bilan Ilmiy Muloqot")
    user_input = st.text_input("Ekologik muammo yoki prognoz haqida so'rang:", placeholder="Masalan: O'zbekistonda 2030-yilda suv darajasi qanday bo'ladi?")
    
    if st.button("Tahlilni boshlash / Run AI"):
        if user_input:
            with st.spinner('Llama 3 oylamoqda...'):
                try:
                    chat_completion = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": "Sen ekologiya va Big Data bo'yicha mutaxassis AI ekologsan. Javoblaringni ilmiy va aniq ber."},
                            {"role": "user", "content": user_input}
                        ],
                        model="llama3-8b-8192",
                    )
                    response = chat_completion.choices[0].message.content
                    st.markdown(f'<div class="ai-response"><b>Llama 3 javobi:</b><br><br>{response}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Xato yuz berdi: {e}")
        else:
            st.warning("Iltimos, savol kiriting.")

# =================================================================
# QOLGAN SAHIFALAR (Siz xohlagan kollaboratsiyalar bilan)
# =================================================================
elif page == "2. Water Quality (Suv sifati)":
    st.title("💧 Water Quality Hub")
    st.link_button("UNEP Water Data", "https://www.unep.org/explore-topics/water")
    st.link_button("World Bank Water", "https://datacatalog.worldbank.org/")
    

elif page == "5. Disasters & Hazards (Tabiiy ofatlar)":
    st.title("🚨 Tabiiy ofatlar monitoringi")
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.error("Zilzilalar (USGS)")
        st.link_button("USGS Live Map", "https://earthquake.usgs.gov/")
    with col_d2:
        st.error("Yong'inlar (NASA)")
        st.link_button("NASA FIRMS", "https://firms.modaps.eosdis.nasa.gov/")
    

# Sahifalar kodi davom etadi... (Poydevor saqlangan)

# --- FOOTER ---
st.markdown(f"""
    <div style="text-align: center; margin-top: 50px; padding: 20px; border-top: 1px solid #00ff88;">
        <p>© 2026 ECO AI WORLD | Mualliflar: <b>Team Proff. Egamberdiev E.</b></p>
    </div>
""", unsafe_allow_html=True)
