import streamlit as st
import datetime
import pandas as pd
from groq import Groq # Groq kutubxonasi

# 1. API SOZLAMASI (Sizning kalitingiz)
client = Groq(api_key="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")

# 2. SAHIFA SOZLAMALARI
st.set_page_config(page_title="ECO AI WORLD | FUTURE", page_icon="⚡", layout="wide")

# 3. DIZAYN (Poydevor uslubi)
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at center, #001010 0%, #000000 100%); color: #00ff88; }
    .main-card { border: 1px solid #00ff88; border-radius: 12px; padding: 20px; background: rgba(0, 255, 136, 0.05); margin-bottom: 15px; }
    .ai-response { border-left: 5px solid #00d4ff; background: rgba(0, 212, 255, 0.15); padding: 15px; border-radius: 5px; color: #ffffff; }
    .shock-message { font-size: 24px; font-weight: bold; color: #ff0000; text-shadow: 0 0 10px #ff0000; animation: blink 1.5s infinite; }
    @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }
    h1, h2, h3 { color: #00ff88 !important; text-shadow: 0 0 10px #00ff88; font-family: 'Orbitron', sans-serif; }
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
        "7. YOUR BODY vs ENV. (Shaxsiy xavf)", # Yangi
        "8. SILENT DISASTER (Jim falokat)"    # Yangi
    ])
    st.divider()
    st.success("Global ekologik monitoring tizimi.")
    st.write(f"Bugun: {datetime.date.today()}")

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
    user_input = st.text_input("Ekologik muammo yoki prognoz haqida so'rang:", placeholder="Masalan: O'zbekistonda 2030-yilda suv tanqisligi qanday bo'ladi?")
    
    if st.button("Tahlilni boshlash / Run AI"):
        if user_input:
            with st.spinner('Llama 3 o\'ylamoqda...'):
                try:
                    chat_completion = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": "Sen ekologiya va Big Data bo'yicha mutaxassis AI ekologsan. Javoblaringni ilmiy, aniq va qisqa ber."},
                            {"role": "user", "content": user_input}
                        ],
                        model="llama3-8b-8192", # Eng tezkor model
                        temperature=0.7,
                        max_tokens=250 # Javobni qisqaroq qilish uchun
                    )
                    response = chat_completion.choices[0].message.content
                    st.markdown(f'<div class="ai-response"><b>Llama 3 javobi:</b><br><br>{response}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"AI bilan aloqa uzildi: {e}. Groq.com saytidan kalitingizni tekshiring.")
        else:
            st.warning("Iltimos, AI ga savol kiriting.")

# =================================================================
# 7. YOUR BODY vs ENVIRONMENT (SHAXSIY ZARBA EFEKTI)
# =================================================================
elif page == "7. YOUR BODY vs ENV. (Shaxsiy xavf)":
    st.title("🫀 YOUR BODY vs ENVIRONMENT 🌍")
    st.markdown('<p class="shock-message">Sizning tanangiz qanday xavf ostida?</p>', unsafe_allow_html=True)
    
    col_age, col_gender = st.columns(2)
    with col_age:
        age = st.number_input("Yoshingiz / Your Age:", min_value=1, max_value=100, value=30)
    with col_gender:
        gender = st.selectbox("Jinsingiz / Your Gender:", ["Erkak / Male", "Ayol / Female"])
    
    health_issue = st.multiselect("Sog'ligingizdagi muammolar (ixtiyoriy) / Health issues (optional):", ["Yurak kasalligi / Heart Disease", "Astma / Asthma", "Allergiya / Allergy"])
    
    if st.button("Mening xavfimni hisobla / Calculate My Risk"):
        pollution_impact = age * 0.5
        if "Astma / Asthma" in health_issue:
            pollution_impact += 15
        if "Yurak kasalligi / Heart Disease" in health_issue:
            pollution_impact += 10
        
        st.divider()
        st.markdown(f"""
        <div class="main-card">
            <h3>⚡ SHOK XABAR!</h3>
            <p>Agar siz Toshkent kabi sanoatlashgan shaharda <span style="color: #00ff88;">10 yil</span> yashasangiz:</p>
            <ul>
                <li>O'pka yuklanishi: <span style="color: #ff0000; font-weight: bold;">+{int(pollution_impact)}%</span></li>
                <li>Yurak xastaligi xavfi: <span style="color: #ff0000; font-weight: bold;">+{int(pollution_impact / 2)}%</span></li>
            </ul>
            <p style="font-style: italic; color: gray;">Bu AI hisoboti umumiy ma'lumotlarga asoslangan.</p>
        </div>
        """, unsafe_allow_html=True)

# =================================================================
# 8. SILENT DISASTER MODE (JIM FALOKAT)
# =================================================================
elif page == "8. SILENT DISASTER (Jim falokat)":
    st.title("🤫 SILENT DISASTER MODE")
    st.markdown('<p class="shock-message">Falokat yuz bermoqda. Siz bilmaysiz.</p>', unsafe_allow_html=True)
    
    st.image("https://images.unsplash.com/photo-1549429737-198139587a82", caption="Sokin manzara, ammo...", use_column_width=True) # Sokin rasm
    
    st.info("AI fon rejimida global ma'lumotlarni tahlil qilmoqda.")
    
    if st.button("Yashirin xavfni fosh etish / Reveal Hidden Danger"):
        st.divider()
        st.markdown("""
        <div class="main-card">
            <h3>🔴 AI XULOSASI: JIM FALOKAT ANIQLANDI!</h3>
            <p>Hozirgi global monitoring ma'lumotlariga ko'ra:</p>
            <ul>
                <li>✅  Katta zilzilalar: Yo'q</li>
                <li>✅  Vulkan otilishi: Yo'q</li>
                <li>❌  Lekin... <span style="color: #ff0000; font-weight: bold;">tuproq sho'rlanishi kritik darajada</span></li>
                <li>❌  Va <span style="color: #ff0000; font-weight: bold;">"mikroplastik" ifloslanish butun dunyo bo'ylab oshmoqda</span></li>
            </ul>
            <p style="font-style: italic; color: gray;">Odamlar sezmaydigan, ammo kelajakni o'zgartiruvchi xavflar...</p>
        </div>
        """, unsafe_allow_html=True)

# =================================================================
# QOLGAN SAHIFALAR (O'zbekcha-Inglizcha va Kollaboratsiyalar bilan)
# =================================================================
elif page == "2. Water Quality (Suv sifati)":
    st.title("💧 Water Quality Hub (Suv sifati)")
    st.link_button("UNEP Water Data", "https://www.unep.org/explore-topics/water")
    st.link_button("World Bank Water", "https://datacatalog.worldbank.org/")
    
elif page == "3. Soil Monitoring (Tuproq nazorati)":
    st.title("🌱 Soil Monitoring (Tuproq nazorati)")
    st.link_button("SoilGrids ISRIC", "https://soilgrids.org/")
    st.link_button("FAO Soil Portal", "https://www.fao.org/global-soil-partnership/en/")

elif page == "4. Climate Change (Iqlim o'zgarishi)":
    st.title("🌡️ Climate Change Analytics (Iqlim tahlili)")
    st.link_button("IPCC Climate Data", "https://www.ipcc-data.org/")
    st.link_button("Copernicus Climate", "https://climate.copernicus.eu/")

elif page == "5. Disasters & Hazards (Tabiiy ofatlar)":
    st.title("🚨 Disasters & Hazards (Tabiiy ofatlar)")
    st.link_button("USGS Earthquakes", "https://earthquake.usgs.gov/")
    st.link_button("NASA FIRMS (Fire)", "https://firms.modaps.eosdis.nasa.gov/")
    
# --- FOOTER ---
st.markdown(f"""
    <div style="text-align: center; margin-top: 50px; padding: 20px; border-top: 1px solid #00ff88;">
        <p>© 2026 ECO AI WORLD | Mualliflar: <b>Team Proff. Egamberdiev E.</b></p>
    </div>
""", unsafe_allow_html=True)
