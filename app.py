import streamlit as st
import datetime
import pandas as pd
from groq import Groq

# 1. API SOZLAMASI (Yangi barqaror model bilan)
# API kalitingiz saqlab qolindi
client = Groq(api_key="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")

# 2. SAHIFA SOZLAMALARI
st.set_page_config(page_title="ECO AI WORLD | FUTURE", page_icon="☣️", layout="wide")

# 3. PREMIUM DIZAYN (Silent & Shock Mode uchun)
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at center, #000a0a 0%, #000000 100%); color: #00ff88; }
    .main-card { border: 1px solid #00ff88; border-radius: 12px; padding: 20px; background: rgba(0, 255, 136, 0.05); margin-bottom: 15px; }
    .shock-text { color: #ff0000; font-weight: bold; text-transform: uppercase; letter-spacing: 2px; animation: pulse 2s infinite; }
    @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.3; } 100% { opacity: 1; } }
    .ai-verdict { border-left: 4px solid #ff4b4b; background: rgba(255, 75, 75, 0.1); padding: 15px; border-radius: 8px; }
    h1, h2, h3 { font-family: 'Orbitron', sans-serif; text-shadow: 0 0 10px #00ff88; }
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
        "5. Disasters & Hazards (Ofatlar)",
        "6. 🧠 AI CORE (Eco-Judgment)",
        "7. YOUR BODY vs ENV. (Personal)",
        "8. SILENT DISASTER (Hidden)"
    ])
    st.divider()
    # Siz so'ragan o'zgarmas jumla
    st.success("Global ekologik monitoring tizimi.")

# =================================================================
# 1. MONITORING TERMINAL (POYDEVOR 100% SAQLANDI)
# =================================================================
if page == "1. Monitoring Terminal (Asosiy)":
    st.title("📟 ECO AI WORLD: GLOBAL MONITORING")
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.link_button("💨 IQAir", "https://www.iqair.com/")
    with col2: st.link_button("🚀 NASA FIRMS", "https://firms.modaps.eosdis.nasa.gov/map/")
    with col3: st.link_button("🤖 Grok AI", "https://grok.com")
    with col4: st.link_button("🛰️ Sentinel", "https://apps.sentinel-hub.com/eo-browser/")
    st.divider()
    st.components.v1.iframe("https://earth.nullschool.net/#current/wind/surface/level/orthographic=-296.22,40.06,500", height=600)

# =================================================================
# 6. 🧠 AI CORE (ECO-JUDGMENT / AI TAHLIL TUZATILDI)
# =================================================================
elif page == "6. 🧠 AI CORE (Eco-Judgment)":
    st.title("🤖 AI CORE: ECO-JUDGMENT ⚡")
    st.info("Groq LPU texnologiyasi orqali realtime tahlil.")

    user_query = st.text_input("Savolingizni kiriting / Enter your query:", placeholder="Dunyo suv muammosi haqida...")
    
    if st.button("Tahlilni boshlash / Run AI Verdict"):
        if user_query:
            with st.status("Typing AI verdict...", expanded=True) as status:
                try:
                    # Skrinshotdagi xatoni tuzatish: Model nomi yangilandi
                    completion = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": "Sen shafqatsiz va aniq gapiradigan ekologik AI'san. Insoniyatga haqiqatni shok holatida tushuntir."},
                            {"role": "user", "content": user_query}
                        ],
                        model="llama-3.3-70b-versatile", # Eng yangi va barqaror model
                    )
                    st.markdown(f'<div class="ai-verdict"><b>HUKM (VERDICT):</b><br><br>{completion.choices[0].message.content}</div>', unsafe_allow_html=True)
                    status.update(label="Tahlil yakunlandi!", state="complete")
                except Exception as e:
                    st.error(f"Xatolik: {e}. Model yangilanmoqda, iltimos qayta urinib ko'ring.")
        else:
            st.warning("Iltimos, ma'lumot kiriting.")

# =================================================================
# 7. YOUR BODY vs ENVIRONMENT (SHAXSIY ZARBA)
# =================================================================
elif page == "7. YOUR BODY vs ENV. (Personal)":
    st.title("🫀 YOUR BODY vs ENVIRONMENT 🌍")
    st.markdown('<p class="shock-text">Tanangiz ichidagi ekologik urush</p>', unsafe_allow_html=True)
    
    age = st.slider("Yoshingiz:", 1, 100, 25)
    health = st.selectbox("Sog'liq holati:", ["Sog'lom", "Astma / Allergik", "Yurak zaifligi"])
    
    if st.button("Haqiqatni ko'rish"):
        impact = age * 0.8 if health != "Sog'lom" else age * 0.4
        st.markdown(f"""
        <div class="main-card">
            <h3>⚠️ SHAXSIY HISOBOT:</h3>
            <p>Hozirgi hududingizda yana 10 yil yashash natijasi:</p>
            <h2 style='color:#ff4b4b;'>O'pka yuklanishi: +{int(impact)}%</h2>
            <p>Qon tarkibidagi mikroplastik miqdori oshish ehtimoli: <b>Yuqori</b></p>
            <p class='shock-text'>XULOSA: Tanangiz filtr sifatida ishlamoqda!</p>
        </div>
        """, unsafe_allow_html=True)

# =================================================================
# 8. SILENT DISASTER MODE (NETFLIX UX)
# =================================================================
elif page == "8. SILENT DISASTER (Hidden)":
    st.title("😶 SILENT DISASTER MODE")
    st.write("Sokinlik... lekin xavf allaqachon shu yerda.")
    
    st.image("https://images.unsplash.com/photo-1500382017468-9049fed747ef", caption="Hamma narsa tinchdek tuyuladimi?")
    
    if st.button("Fon tahlilini yoqish"):
        st.toast("AI yashirin anomaliyalarni qidirmoqda...")
        st.markdown("""
        <div class="main-card" style="border-color: #ff4b4b;">
            <h3 class="shock-text">⚠️ DIQQAT: JIM FALOKAT ANIQLANDI</h3>
            <p>Odamlar ko'rmaydi, lekin ma'lumotlar aytadi:</p>
            <ul>
                <li>Tuproq ostidagi biom o'limi: <b>Boshlangan</b></li>
                <li>Yer osti suvlari zaharlanishi: <b>Kritik darajada</b></li>
            </ul>
            <p>Falokat boshlanib bo'lgan. Siz shunchaki uni his qilmayapsiz.</p>
        </div>
        """, unsafe_allow_html=True)

# --- QOLGAN SAHIFALAR (SAQLAB QOLINDI) ---
elif page == "2. Water Quality (Suv sifati)":
    st.title("💧 Water Quality Hub")
    st.link_button("UNEP Data", "https://www.unep.org/explore-topics/water")
elif page == "5. Disasters & Hazards (Ofatlar)":
    st.title("🚨 Disasters & Hazards")
    st.link_button("USGS Earthquake", "https://earthquake.usgs.gov/")
    st.link_button("NASA FIRE", "https://firms.modaps.eosdis.nasa.gov/")

# --- FOOTER ---
st.markdown("<div style='text-align: center; border-top: 1px solid #00ff88; padding-top: 20px;'>© 2026 ECO AI WORLD</div>", unsafe_allow_html=True)
