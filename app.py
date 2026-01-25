import streamlit as st
import datetime
import pandas as pd

# 1. SAHIFA SOZLAMALARI
st.set_page_config(page_title="ECO AI WORLD | Enterprise", page_icon="🧬", layout="wide")

# 2. DIZAYN (O'zgarmas poydevor)
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at center, #001010 0%, #000000 100%); color: #00ff88; }
    .main-card { border: 1px solid #00ff88; border-radius: 12px; padding: 20px; background: rgba(0, 255, 136, 0.05); margin-bottom: 15px; }
    .ai-core { border: 2px solid #00d4ff; background: rgba(0, 212, 255, 0.05); padding: 20px; border-radius: 15px; }
    h1, h2, h3 { color: #00ff88 !important; text-shadow: 0 0 10px #00ff88; }
    </style>
    """, unsafe_allow_html=True)

# --- NAVIGATSIYA ---
with st.sidebar:
    st.title("💠 ECO NAVIGATION")
    page = st.radio("MENYU:", [
        "1. Asosiy Terminal", 
        "2. Water Quality Hub", 
        "3. Soil Monitoring",
        "4. Climate Change Analytics",
        "5. Disasters & Hazards",
        "6. 🧠 AI CORE (Yadro)",
        "7. User Dashboard"
    ])
    st.divider()
    st.success("ECO AI WORLD - Global ekologik monitoring tizimi.")

# =================================================================
# 1. ASOSIY TERMINAL (Poydevor)
# =================================================================
if page == "1. Asosiy Terminal":
    st.title("🛰️ GLOBAL MONITORING HUB")
    st.components.v1.iframe("https://earth.nullschool.net/#current/wind/surface/level/orthographic=-296.22,40.06,500", height=600)

# =================================================================
# 2. WATER QUALITY HUB
# =================================================================
elif page == "2. Water Quality Hub":
    st.title("💧 Global Suv Resurslari va Sifati")
    st.markdown('<div class="main-card"><h4>📌 Kollaboratsiya va Ma\'lumotlar:</h4></div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.info("🌊 UNEP Water")
        st.link_button("UNEP Data", "https://www.unep.org/explore-topics/water")
    with c2:
        st.info("🏦 World Bank Water")
        st.link_button("Water Data Portal", "https://datacatalog.worldbank.org/search/dataset/0037584")
    with c3:
        st.info("🌾 FAO AQUASTAT")
        st.link_button("Global Water Stats", "https://www.fao.org/aquastat/en/")
    

# =================================================================
# 3. SOIL MONITORING
# =================================================================
elif page == "3. Soil Monitoring":
    st.title("🌱 Tuproq Monitoringi va Degradatsiyasi")
    st.markdown('<div class="main-card"><h4>🌍 Global Tuproq Ma\'lumotlari:</h4></div>', unsafe_allow_html=True)
    sc1, sc2 = st.columns(2)
    with sc1:
        st.info("🌍 ISRIC Global Soil")
        st.link_button("SoilGrids Explorer", "https://soilgrids.org/")
    with sc2:
        st.info("🛰️ FAO Global Soil Partnership")
        st.link_button("Soil Portal", "https://www.fao.org/global-soil-partnership/gsis/en/")
    

# =================================================================
# 4. CLIMATE CHANGE ANALYTICS
# =================================================================
elif page == "4. Climate Change Analytics":
    st.title("🌡️ Iqlim O'zgarishi Analitikasi")
    st.markdown('<div class="main-card"><h4>📉 Global Isish va Emissiya:</h4></div>', unsafe_allow_html=True)
    st.link_button("IPCC Data Center", "https://www.ipcc-data.org/")
    st.link_button("NOAA Climate Monitoring", "https://www.climate.gov/maps-data")
    st.link_button("Copernicus Climate Change", "https://climate.copernicus.eu/")

# =================================================================
# 5. DISASTERS & HAZARDS
# =================================================================
elif page == "5. Disasters & Hazards":
    st.title("🌋 Tabiiy Ofatlar Monitoringi")
    col_d1, col_d2, col_d3 = st.columns(3)
    with col_d1:
        st.error("🚨 Zilzila (USGS/EMSC)")
        st.link_button("USGS Live", "https://earthquake.usgs.gov/earthquakes/map/")
    with col_d2:
        st.error("🌋 Vulkanlar")
        st.link_button("Volcano Live", "https://www.volcanodiscovery.com/daily-map-active-volcanoes.html")
    with col_d3:
        st.error("🔥 Yong'in (NASA FIRMS)")
        st.link_button("NASA FIRMS Map", "https://firms.modaps.eosdis.nasa.gov/map/")
    

# =================================================================
# 6. 🧠 AI CORE (Eng muhim qism)
# =================================================================
elif page == "6. 🧠 AI CORE (Yadro)":
    st.title("🤖 AI YADROSI: INTELLEKTUAL TAHLIL")
    
    st.markdown("""
    <div class="ai-core">
        <h3>🚀 AI Imkoniyatlari</h3>
        <ul>
            <li><b>Big Data:</b> Millionlab sensor va sputnik ma'lumotlarini qayta ishlash.</li>
            <li><b>Anomaliya:</b> Tabiatdagi keskin o'zgarishlarni soniyalarda aniqlash.</li>
            <li><b>Risk Scoring:</b> Hududlar uchun xavf darajasini (0-100) hisoblash.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    
    
    st.subheader("🧠 Amaldagi AI Modellar")
    m1, m2, m3, m4 = st.columns(4)
    m1.code("LSTM\n(Time Series)", language="text")
    m2.code("Random Forest\n(Classification)", language="text")
    m3.code("CNN\n(Satellite Vision)", language="text")
    m4.code("NLP\n(Report Analysis)", language="text")

# =================================================================
# 7. USER DASHBOARD
# =================================================================
elif page == "7. User Dashboard":
    st.title("👤 FOYDALANUVCHI INTERFEYSI")
    u_type = st.selectbox("Siz kimsiz?", ["Oddiy Foydalanuvchi", "Kompaniya / Zavod", "Davlat / NGO"])
    
    if u_type == "Oddiy Foydalanuvchi":
        st.success("📍 Hududingiz: Toshkent | Havo: To'q sariq (Xavfli) | Tavsiya: Niqob taqing.")
    elif u_type == "Kompaniya / Zavod":
        st.warning("⚠️ ESG Hisobot: Emissiya limiti 15% ga oshgan. Jarima xavfi bor.")
    elif u_type == "Davlat / NGO":
        st.info("📊 Siyosiy qaror uchun: Orolbo'yi hududida sho'rlanish 3% ga kamaydi.")
        st.button("Statistik Eksport (CSV/PDF)")

# --- FOOTER ---
st.markdown(f"""
    <div style="text-align: center; margin-top: 50px; padding: 20px; border-top: 1px solid #00ff88;">
        <p>© 2026 ECO AI WORLD | Muallif: <b>Team Proff. Egamberdiev E.</b></p>
    </div>
""", unsafe_allow_html=True)
