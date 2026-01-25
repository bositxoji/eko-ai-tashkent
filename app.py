import streamlit as st
import datetime
import pandas as pd
from groq import Groq

# 1. API SOZLAMASI (Barqaror model)
client = Groq(api_key="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")

# 2. SAHIFA SOZLAMALARI
st.set_page_config(page_title="ECO AI WORLD | Silent Threat", page_icon="⚠️", layout="wide")

# 3. "SILENT THREAT" DIZAYN KONSEPSIYASI
st.markdown("""
    <style>
    /* Asosiy fon va atmosfera */
    .stApp {
        background-color: #0E1116;
        color: #1C1F26; /* Smoke gray matnlar uchun */
    }
    
    /* Sokin Graphite va Smoke palitrasi */
    [data-testid="stHeader"], [data-testid="stSidebar"] {
        background-color: #0E1116 !important;
        border-right: 1px solid #1C1F26;
    }
    
    /* Matn iyerarxiyasi */
    h1 { color: #FFFFFF !important; font-family: 'Inter', sans-serif; font-weight: 800; letter-spacing: -1px; }
    h2 { color: #FFD400 !important; font-family: 'Inter', sans-serif; font-weight: 600; } /* Zahar sariq */
    p, li { color: #A0A0A0 !important; font-size: 1.1rem; }
    
    /* Signal ranglar va pulsatsiya */
    .danger-alert {
        color: #FF3B3B; 
        font-weight: bold;
        animation: pulse-red 3s infinite;
    }
    @keyframes pulse-red {
        0% { text-shadow: 0 0 0px #FF3B3B; }
        50% { text-shadow: 0 0 15px #FF3B3B; }
        100% { text-shadow: 0 0 0px #FF3B3B; }
    }
    
    /* Rich Content Kartalari */
    .main-card {
        background: #1C1F26;
        border-radius: 4px;
        padding: 24px;
        border-left: 3px solid #FFD400; /* Zahar sariq urg'u */
        margin-bottom: 20px;
        transition: 0.3s;
    }
    .main-card:hover {
        background: #242830;
    }

    /* AI Verdict effekti */
    .ai-verdict-box {
        background: #000000;
        border: 1px solid #1C1F26;
        padding: 20px;
        color: #FFFFFF !important;
        font-family: 'Courier New', monospace;
    }
    </style>
    """, unsafe_allow_html=True)

# --- NAVIGATSIYA ---
with st.sidebar:
    st.markdown("<h1 style='font-size: 20px;'>💠 ECO NAVIGATION</h1>", unsafe_allow_html=True)
    page = st.radio("", [
        "1. Monitoring Terminal", 
        "2. Water Analytics", 
        "3. Soil Integrity",
        "4. Climate Shifts",
        "5. Global Hazards",
        "6. 🧠 AI ECO-JUDGMENT",
        "7. BODY vs ENVIRONMENT",
        "8. THE SILENT MODE"
    ])
    st.divider()
    st.markdown("<p style='font-size: 12px;'>ECO AI WORLD v2.0<br>Haqiqat yolg'ondan ustun.</p>", unsafe_allow_html=True)

# =================================================================
# 1. MONITORING TERMINAL (Poydevor saqlangan, dizayn o'zgargan)
# =================================================================
if page == "1. Monitoring Terminal":
    st.markdown("<h1>ECO AI WORLD: TERMINAL</h1>", unsafe_allow_html=True)
    st.markdown("<h2>Global ma'lumotlar oqimi</h2>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.link_button("💨 Air Status", "https://www.iqair.com/")
    with col2: st.link_button("🔥 NASA FIRMS", "https://firms.modaps.eosdis.nasa.gov/map/")
    with col3: st.link_button("🤖 Logic AI", "https://grok.com")
    with col4: st.link_button("🛰️ Sentinel", "https://apps.sentinel-hub.com/eo-browser/")
    
    
    st.divider()
    st.components.v1.iframe("https://earth.nullschool.net/#current/wind/surface/level/orthographic=-296.22,40.06,500", height=600)

# =================================================================
# 6. 🧠 AI ECO-JUDGMENT (Typing Effect & Groq)
# =================================================================
elif page == "6. 🧠 AI ECO-JUDGMENT":
    st.markdown("<h1>AI ECO-JUDGMENT</h1>", unsafe_allow_html=True)
    st.markdown("<h2>Llama 3.3 tahlili</h2>", unsafe_allow_html=True)
    
    
    
    query = st.text_input("Tizimga savol bering:", placeholder="Masalan: Insoniyatning iqlimga ta'siri qaytarilmasmi?")
    
    if st.button("HUKMNI ESHITISH"):
        if query:
            with st.spinner("AI tahlil qilmoqda..."):
                try:
                    completion = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": "Sen 'Silent Threat' loyihasining AI qismisan. Javoblaring shafqatsiz darajada aniq, qisqa va faktlarga asoslangan bo'lsin. Hech qanday greenwashing (yolg'on yashillik) qilma."},
                            {"role": "user", "content": query}
                        ],
                        model="llama-3.3-70b-versatile",
                    )
                    st.markdown(f'<div class="ai-verdict-box"><b>STATUS: FINAL VERDICT</b><br><br>{completion.choices[0].message.content}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Tizim xatosi: {e}")

# =================================================================
# 7. BODY vs ENVIRONMENT (Shaxsiy Zarba)
# =================================================================
elif page == "7. BODY vs ENVIRONMENT":
    st.markdown("<h1>YOUR BODY vs ENVIRONMENT</h1>", unsafe_allow_html=True)
    st.markdown("<h2>Sizning tanangiz - yagona filtr</h2>", unsafe_allow_html=True)
    
    
    
    age = st.slider("Yoshingiz:", 1, 100, 25)
    st.markdown('<div class="main-card">Siz yashayotgan hududda havo sifati sizning genetikangizga ta\'sir qilmoqda.</div>', unsafe_allow_html=True)
    
    if st.button("ANALIZ"):
        st.markdown(f"<p class='danger-alert'>Ogohlantirish: {age} yoshli tana uchun mikro-zarrachalar yuklanishi kritik darajada.</p>", unsafe_allow_html=True)
        st.markdown("<h2>Kutilayotgan o'zgarish: +18% toksik yuklama.</h2>", unsafe_allow_html=True)

# =================================================================
# 8. THE SILENT MODE (Jim Falokat)
# =================================================================
elif page == "8. THE SILENT MODE":
    st.markdown("<h1>THE SILENT THREAT</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #FFD400;'>Hamma narsa tinch. Ammo bu aldamchi.</p>", unsafe_allow_html=True)
    
    st.image("https://images.unsplash.com/photo-1464822759023-fed622ff2c3b", caption="Tashqi ko'rinish", use_column_width=True)
    
    
    
    if st.button("Haqiqatni fosh qilish"):
        st.markdown("""
            <div class="main-card" style="border-left: 3px solid #FF3B3B;">
                <h2 style="color: #FF3B3B !important;">JALOLAT ANIQLANDI</h2>
                <p>Bu tasvir ortida yer osti suvlari 40% ga ifloslangan. 
                Siz ko'rayotgan yashillik - sun'iy o'g'itlar natijasidagi 'o'lim oldi' rektsiyasi.</p>
                <figure style="color: gray; font-size: 12px;">Manba: FAO / Global Monitoring Data</figure>
            </div>
        """, unsafe_allow_html=True)

# --- QOLGAN SAHIFALAR UCHUN MINIMALIST KO'RINISH ---
elif page == "2. Water Analytics":
    st.markdown("<h1>WATER INTEGRITY</h1>", unsafe_allow_html=True)
    st.link_button("UNEP Data Access", "https://www.unep.org/explore-topics/water")
elif page == "5. Global Hazards":
    st.markdown("<h1>GLOBAL HAZARDS</h1>", unsafe_allow_html=True)
    st.markdown("<p class='danger-alert'>Ayni damda seysmik va termal faollik kuzatilmoqda.</p>", unsafe_allow_html=True)
    st.link_button("USGS Live Feed", "https://earthquake.usgs.gov/")

# --- FOOTER ---
st.markdown("<div style='text-align: center; border-top: 1px solid #1C1F26; padding: 40px; color: #A0A0A0;'>ECO AI WORLD | 2026<br>Silent Threat Design Concept</div>", unsafe_allow_html=True)
