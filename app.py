import streamlit as st
import datetime

# 1. SEO VA SAHIFA SOZLAMALARI
st.set_page_config(
    page_title="ECO AI WORLD | Global Mega-Portal",
    page_icon="🌍",
    layout="wide"
)

# 2. PREMIUM DIZAYN (Poydevor saqlangan)
st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at center, #001010 0%, #000000 100%);
        color: #00ff88;
    }
    .main-card {
        background: rgba(0, 255, 136, 0.05);
        border: 1px solid #00ff88;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
    }
    h1, h2, h3 { font-family: 'Orbitron', sans-serif; text-shadow: 0 0 10px #00ff88; }
    .stat-num { font-size: 30px; font-weight: bold; color: #ff4b4b; }
    [data-testid="stSidebar"] { background-color: #050505 !important; border-right: 1px solid #00ff88; }
    </style>
    """, unsafe_allow_html=True)

# --- NAVIGATSIYA ---
with st.sidebar:
    st.title("💠 ECO AI WORLD")
    page = st.radio("MENYU:", [
        "1. Asosiy Terminal", 
        "2. Carbon & Finance", 
        "3. Future Lab",
        "4. Space Debris Live",
        "5. Green Planner",
        "6. Global News",
        "7. Magma & Tectonic",
        "8. Bio-Diversity Clock"
    ])
    st.divider()
    st.success("Global ekologik monitoring tizimi.")
    st.write(f"Bugun: {datetime.date.today()}")

# =================================================================
# SAHIFALAR LOGIKASI
# =================================================================

if page == "1. Asosiy Terminal":
    st.title("🛰️ GLOBAL MONITORING HUB")
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.markdown('<div class="main-card"><h3>💨 IQAIR</h3><p>Havo sifati.</p></div>', unsafe_allow_html=True)
    with col2: st.markdown('<div class="main-card"><h3>🚀 NASA</h3><p>Ofatlar monitoringi.</p></div>', unsafe_allow_html=True)
    with col3: st.markdown('<div class="main-card"><h3>🤖 GROK AI</h3><p>AI Analitika.</p></div>', unsafe_allow_html=True)
    with col4: st.markdown('<div class="main-card"><h3>🌊 WIND</h3><p>Global oqim.</p></div>', unsafe_allow_html=True)
    st.components.v1.iframe("https://earth.nullschool.net/#current/wind/surface/level/orthographic=-296.22,40.06,500", height=600)

elif page == "2. Carbon & Finance":
    st.title("📈 UGLEROD BIRJASI")
    st.metric("EU ETS Carbon", "€85.20", "+1.2%")
    st.info("Katta kompaniyalarning ifloslanish uchun to'lovlari monitoringi.")

elif page == "3. Future Lab":
    st.title("🧪 KELAJAK PROGNOZLARI")
    
    st.link_button("2050-yil simulyatsiyasi", "https://coastal.climatecentral.org/")

elif page == "4. Space Debris Live":
    st.title("🛰️ KOINOT CHIQINDILARI")
    
    st.link_button("Jonli koinot xaritasi", "http://stuffin.space/")

elif page == "5. Green Planner":
    st.title("🌳 ECO CITY PLANNER")
    st.write("Shaharni yashillashtirish bo'yicha AI tavsiyalari yuklanmoqda...")
    st.link_button("Global Tree Canopy Map", "https://www.google.com/earth/outreach/special-projects/air-quality-and-trees/")

elif page == "6. Global News":
    st.title("📰 GLOBAL ECO-NEWS")
    st.write("🌍 NASA: Ozon qatlamining tiklanish jarayoni o'rganilmoqda.")
    st.write("🌿 O'zbekiston: 'Yashil Makon' umummilliy loyihasi tahlili.")

elif page == "7. Magma & Tectonic":
    st.title("🌋 MAGMA VA TEKTONIK MONITORING")
    
    st.components.v1.iframe("https://www.volcanodiscovery.com/daily-map-active-volcanoes.html", height=600)

elif page == "8. Bio-Diversity Clock":
    st.title("🧬 BIO-XILMA-XILLIK SOATI")
    c1, c2 = st.columns(2)
    with c1:
        forest_lost = (datetime.datetime.now().hour * 3600 + datetime.datetime.now().minute * 60) * 0.5
        st.markdown(f"<h4>Yo'qolgan o'rmonlar (Bugun):</h4><p class='stat-num'>{forest_lost:,.1f} ha</p>", unsafe_allow_html=True)
    with c2:
        species_lost = datetime.datetime.now().hour * 6
        st.markdown(f"<h4>Yo'qolgan turlar (Bugun):</h4><p class='stat-num'>{species_lost:.0f} tur</p>", unsafe_allow_html=True)
    

# --- FOOTER ---
st.markdown(f"""
    <div style="text-align: center; margin-top: 50px; padding: 20px; border-top: 1px solid #00ff88;">
        <p>© 2026 ECO AI WORLD | Muallif: <b>Team Proff. Egamberdiev E.</b></p>
    </div>
""", unsafe_allow_html=True)
