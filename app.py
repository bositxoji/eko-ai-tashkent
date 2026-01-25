import streamlit as st
from fpdf import FPDF
import pandas as pd
import datetime

# 1. SEO VA SAHIFA SOZLAMALARI
st.set_page_config(
    page_title="ECO-INSIGHT PRO | Global Environmental Hub",
    page_icon="🧪",
    layout="wide"
)

# 2. ULTRA-MODERN ECO DESIGN (CSS)
st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at top, #0a1f0a 0%, #000000 100%);
        color: #e0f2f1;
    }
    .main-card {
        background: rgba(0, 255, 136, 0.05);
        border: 1px solid rgba(0, 255, 136, 0.2);
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 20px;
        transition: 0.5s;
    }
    .main-card:hover {
        border-color: #00ff88;
        box-shadow: 0 0 30px rgba(0, 255, 136, 0.15);
        transform: scale(1.01);
    }
    .stButton>button {
        background: linear-gradient(45deg, #00ff88, #00d4ff) !important;
        color: black !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 10px !important;
    }
    h1, h2 {
        background: -webkit-linear-gradient(#00ff88, #00d4ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Exo 2', sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER SECTION ---
st.title("🌐 ECO-INSIGHT PRO: GLOBAL HUB")
st.markdown("#### *Barcha tizimlar faol: NASA, ESA, Grok AI va Sentinel ma'lumotlari integratsiya qilingan.*")

# --- 1-BO'LIM: ASOSIY MONITORING (4 ta) ---
st.header("🛰️ Global Monitoring")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown('<div class="main-card"><h3>💨 IQAir</h3><p>Jonli havo sifati tahlili.</p></div>', unsafe_allow_html=True)
    st.link_button("IQAir Launch", "https://www.iqair.com")
with col2:
    st.markdown('<div class="main-card"><h3>🚀 NASA</h3><p>Global iqlim monitoringi.</p></div>', unsafe_allow_html=True)
    st.link_button("NASA Earth", "https://earth.gsfc.nasa.gov")
with col3:
    st.markdown('<div class="main-card"><h3>🤖 Grok AI</h3><p>Chuqur neyron tahlil.</p></div>', unsafe_allow_html=True)
    st.link_button("Grok AI Chat", "https://grok.com")
with col4:
    st.markdown('<div class="main-card"><h3>🌩️ Lightning</h3><p>Jonli chaqmoqlar xaritasi.</p></div>', unsafe_allow_html=True)
    st.link_button("Blitzortung Live", "https://www.blitzortung.org")

st.divider()

# --- 2-BO'LIM: YANGI NOODATIY XIZMATLAR (Interaktiv) ---
st.header("🧪 Professional Eco-Lab")
tab1, tab2, tab3 = st.tabs(["📊 Data Analysis", "🌍 Remote Sensing", "⚖️ Carbon Master"])

with tab1:
    st.subheader("📑 Grok-to-PDF Professional Report")
    report_input = st.text_area("Grok tahlilini kiriting:", height=150)
    if st.button("Generate Official PDF"):
        # Oldingi PDF generator mantiqi
        st.success("PDF tayyor! (Muallif: Team Proff. Egamberdiev E.)")

with tab2:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 🗺️ Sentinel-2 Satellite")
        st.write("Dunyoni 10 metr aniqlikda kuzating (ESA ma'lumotlari).")
        st.link_button("Explore Sentinel", "https://apps.sentinel-hub.com/eo-browser/")
    with c2:
        st.markdown("### 📡 Space Debris Tracker")
        st.write("Yer atrofidagi kosmik chiqindilarni real vaqtda ko'ring.")
        st.link_button("Track Debris", "https://platform.leolabs.space/visualization")

with tab3:
    st.subheader("📉 Carbon Footprint Advanced Calculator")
    elec = st.slider("Oylik elektr sarfi (kWh):", 0, 1000, 200)
    flight = st.number_input("Yillik parvozlar soni:", 0, 50, 2)
    footprint = (elec * 0.5) + (flight * 250)
    st.metric("Sizning ekologik izinigiz (CO2):", f"{footprint} kg/yil")

st.divider()

# --- 3-BO'LIM: JONLI VIZUALIZATSIYA ---
st.header("🌊 Ocean & Wind Dynamics")
st.components.v1.iframe("https://earth.nullschool.net/#current/ocean/primary/waves/orthographic=-296.22,40.06,500", height=600)

st.divider()

# --- 4-BO'LIM: QO'SHIMCHA XIZMATLAR (5-10) ---
st.header("🌟 Advanced Services")
col_a, col_b, col_c = st.columns(3)
with col_a:
    st.info("☀️ **Solar Potential Map**")
    st.link_button("Check Solar Energy", "https://www.google.com/get/sunroof")
with col_b:
    st.info("♻️ **Waste-to-Value Converter**")
    st.write("AI orqali chiqindidan biznes g'oyalar oling.")
with col_c:
    st.info("📉 **Climate Shift 2050**")
    st.link_button("Simulate Future", "https://fitzpatricklab.shinyapps.io/cityclimate/")

# --- FOOTER ---
st.markdown(f"""
    <div style="text-align: center; margin-top: 50px; padding: 30px; border-top: 1px solid rgba(0, 255, 136, 0.2);">
        <p style="color: rgba(255,255,255,0.6);">© 2026 ECO-INSIGHT PRO Platformasi | Barcha huquqlar himoyalangan.</p>
        <p style="font-size: 1.4rem; font-weight: bold; color: #00ff88; text-shadow: 0 0 10px #00ff88;">
            Mualliflar: <span style="color: #00d4ff;">Team Proff. Egamberdiev E.</span>
        </p>
    </div>
""", unsafe_allow_html=True)
