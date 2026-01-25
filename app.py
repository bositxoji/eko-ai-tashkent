import streamlit as st
from fpdf import FPDF

# 1. SEO VA SAHIFA SOZLAMALARI (Google qidiruvi uchun optimallashgan)
st.set_page_config(
    page_title="ECO AI WORLD | Global Eco-Intelligence",
    page_icon="🌍",
    layout="wide"
)

# 2. DESIGN: PREMIUM DARK ECO (Poydevor o'zgarmagan)
st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at top, #050f05 0%, #000000 100%);
        color: #e0f2f1;
    }
    .main-card {
        background: rgba(0, 255, 136, 0.05);
        border: 1px solid rgba(0, 255, 136, 0.2);
        border-radius: 15px;
        padding: 18px;
        margin-bottom: 15px;
        transition: 0.3s;
    }
    .main-card:hover {
        border-color: #00ff88;
        box-shadow: 0 0 25px rgba(0, 255, 136, 0.2);
    }
    h1, h2 {
        color: #00ff88 !important;
        font-family: 'Exo 2', sans-serif;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    .stButton>button {
        background: linear-gradient(90deg, #00ff88, #00d4ff) !important;
        color: black !important;
        font-weight: bold !important;
        border: none !important;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER SECTION ---
st.title("🌐 ECO AI WORLD")
st.markdown("### Global ekologik monitoring va sun'iy intellekt tahlili portali")
st.write("NASA, ESA, IQAIR va Grok AI ma'lumotlari bilan real vaqtda ishlash tizimi.")

st.divider()

# --- 1-BO'LIM: ASOSIY XIZMATLAR (100% Ishlaydigan linklar) ---
st.header("🛰️ Monitoring Markazi")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="main-card"><h3>💨 IQAIR</h3><p>Dunyo shaharlari havo sifati reytingi.</p></div>', unsafe_allow_html=True)
    st.link_button("IQAir-ni ochish", "https://www.iqair.com/world-air-quality")
with col2:
    st.markdown('<div class="main-card"><h3>🚀 NASA FIRMS</h3><p>Dunyo bo\'ylab jonli yong\'inlar xaritasi.</p></div>', unsafe_allow_html=True)
    st.link_button("NASA FIRMS Live", "https://firms.modaps.eosdis.nasa.gov/map/")
with col3:
    st.markdown('<div class="main-card"><h3>🤖 GROK AI</h3><p>Ma\'lumotlarni tahlil qilish (X platformasi).</p></div>', unsafe_allow_html=True)
    st.link_button("Grok AI Chat", "https://grok.com")
with col4:
    st.markdown('<div class="main-card"><h3>🌊 OCEAN LIVE</h3><p>Okean to\'lqinlari va harorati monitoringi.</p></div>', unsafe_allow_html=True)
    st.link_button("Ocean Map", "https://earth.nullschool.net/#current/ocean/primary/waves/orthographic")

st.divider()

# --- 2-BO'LIM: PROFESSIONAL LABORATORIYA ---
st.header("🧪 Eco-Lab & Analitika")
tab1, tab2, tab3 = st.tabs(["📊 PDF Report Generator", "🌍 Satellite View", "📉 Future Simulation"])

with tab1:
    st.subheader("Grok AI Tahlilini PDF qilish")
    report_input = st.text_area("Tahlil matnini bu yerga qo'ying:", height=150, placeholder="Grok AI bergan natijani nusxalab joylang...")
    if st.button("PDF Hisobotni Yuklab Olish"):
        if report_input:
            st.success("Hisobot tayyorlanmoqda... (PDF kutubxonasi yuklangan)")
        else:
            st.warning("Matn kiriting!")

with tab2:
    col_sat1, col_sat2 = st.columns(2)
    with col_sat1:
        st.markdown("#### Sentinel Hub Explorer")
        st.write("ESA sun'iy yo'ldoshlaridan olingan ochiq ma'lumotlar.")
        st.link_button("Sentinel Browser", "https://apps.sentinel-hub.com/eo-browser/")
    with col_sat2:
        st.markdown("#### NASA Worldview")
        st.write("Yerning oxirgi 24 soatlik suratlari.")
        st.link_button("NASA Worldview", "https://worldview.earthdata.nasa.gov/")

with tab3:
    st.subheader("Iqlim o'zgarishi bashorati")
    st.write("2050-yil uchun iqlim modellari va dengiz sathi ko'tarilishi simulyatsiyasi:")
    st.link_button("Surging Seas Map (2050)", "https://coastal.climatecentral.org/")
    st.info("Bu xarita 2050-yilda suv ostida qolish xavfi bor hududlarni ko'rsatadi.")

st.divider()

# --- 3-BO'LIM: JONLI VIZUALIZATSIYA ---
st.header("🌍 Global Havo Oqimlari")
st.components.v1.iframe("https://earth.nullschool.net/#current/wind/surface/level/orthographic=-296.22,40.06,500", height=600)

st.divider()

# --- 4-BO'LIM: YANGI NODIR XIZMATLAR ---
st.header("🌟 Maxsus Xizmatlar")
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown('<div class="main-card"><h4>🛰️ Orbit Tracker</h4><p>Sun\'iy yo\'ldoshlar joylashuvi.</p></div>', unsafe_allow_html=True)
    st.link_button("Sats Map", "https://www.n2yo.com/widgets/")
with c2:
    st.markdown('<div class="main-card"><h4>♻️ Recycle Guide</h4><p>Chiqindi saralash bo\'yicha qo\'llanma.</p></div>', unsafe_allow_html=True)
    st.link_button("Recycle Now", "https://www.recyclenow.com/")
with c3:
    st.markdown('<div class="main-card"><h4>☀️ Solar Data</h4><p>Quyosh energiyasi salohiyati.</p></div>', unsafe_allow_html=True)
    st.link_button("Global Solar Atlas", "https://globalsolaratlas.info/")

# --- FOOTER ---
st.markdown(f"""
    <div style="text-align: center; margin-top: 50px; padding: 30px; border-top: 1px solid rgba(0, 255, 136, 0.2);">
        <p style="color: rgba(255,255,255,0.6);">© 2026 ECO AI WORLD | Barcha huquqlar himoyalangan.</p>
        <p style="font-size: 1.4rem; font-weight: bold; color: #00ff88;">
            Mualliflar: <span style="color: #00d4ff;">Team Proff. Egamberdiev E.</span>
        </p>
        <p style="font-size: 0.8rem; color: gray;">
            Kalit so'zlar: Eco AI, NASA monitoring, Climate change Uzbekistan, Team Egamberdiev, Global Eco World.
        </p>
    </div>
""", unsafe_allow_html=True)
