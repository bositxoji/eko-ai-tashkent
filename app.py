import streamlit as st
import pandas as pd
import datetime

# 1. SEO VA SAHIFA SOZLAMALARI
st.set_page_config(
    page_title="ECO AI WORLD | Carbon & Eco Terminal",
    page_icon="💎",
    layout="wide"
)

# 2. DESIGN: CYBER-ECO STYLE
st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at center, #001a1a 0%, #000000 100%);
        color: #00ff88;
    }
    .market-card {
        background: rgba(0, 255, 136, 0.02);
        border: 1px solid #00ff88;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
    }
    .price-up { color: #00ff88; font-weight: bold; font-size: 20px; }
    .price-down { color: #ff4b4b; font-weight: bold; font-size: 20px; }
    h1, h2, h3 { font-family: 'Courier New', monospace; text-shadow: 0 0 10px #00ff88; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.title("📟 ECO AI WORLD: TERMINAL")
st.markdown("#### *Global Ekologik Resurslar va Uglerod Birjasi Monitoringi*")

st.divider()

# --- 1-BO'LIM: CARBON STOCK MARKET (YANGI) ---
st.header("📈 Carbon Stock Market (EU/Global)")
m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown('<div class="market-card"><p>EU ETS Carbon Price</p><p class="price-up">€85.42 ▲ 1.2%</p></div>', unsafe_allow_html=True)
with m2:
    st.markdown('<div class="market-card"><p>UK Carbon Price</p><p class="price-down">£42.10 ▼ 0.5%</p></div>', unsafe_allow_html=True)
with m3:
    st.markdown('<div class="market-card"><p>Gold Standard Credits</p><p class="price-up">$12.50 ▲ 4.8%</p></div>', unsafe_allow_html=True)
with m4:
    st.markdown('<div class="market-card"><p>Global Carbon Tax Avg</p><p class="price-up">$31.00 ▲ 0.2%</p></div>', unsafe_allow_html=True)

st.link_button("To'liq birja tahlilini ko'rish (Grok orqali)", "https://grok.com/?q=latest+carbon+credit+market+prices+analysis")

st.divider()

# --- 2-BO'LIM: NOODATIY MONITORINGLAR ---
st.header("🛰️ Noodatiy Ekologik Analitika")
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("🌌 Night Earth Explorer")
    st.write("Dunyodagi yorug'lik ifloslanishi va energiya isrofini NASA tungi suratlari orqali ko'ring.")
    st.link_button("Night Map Launch", "https://www.lightpollutionmap.info/")

with col_b:
    st.subheader("🧬 De-Extinction Status")
    st.write("Yo'qolib ketgan turlarni qayta tiklash bo'yicha ilmiy loyihalar monitoringi.")
    st.link_button("Colossal Projects", "https://colossal.com/")

st.divider()

# --- 3-BO'LIM: ASOSIY XIZMATLAR (SAQLANGAN) ---
st.header("🌍 Global Hub Services")
s1, s2, s3, s4 = st.columns(4)
with s1:
    st.info("**💨 IQAIR**")
    st.link_button("Air Quality", "https://www.iqair.com/")
with s2:
    st.info("**🚀 NASA FIRMS**")
    st.link_button("Fire Map", "https://firms.modaps.eosdis.nasa.gov/map/")
with s3:
    st.info("**🇺🇿 YASHIL MAKON**")
    st.link_button("Uzbekistan Eco", "https://yashilmakon.eco/")
with s4:
    st.info("**🌊 WIND & OCEAN**")
    st.link_button("Live Globe", "https://earth.nullschool.net/")

st.divider()

# --- JONLI VIZUALIZATSIYA ---
st.subheader("🗺️ Real-Time Global Flow")
st.components.v1.iframe("https://earth.nullschool.net/#current/wind/surface/level/orthographic=-296.22,40.06,500", height=600)

# --- FOOTER ---
st.markdown(f"""
    <div style="text-align: center; margin-top: 50px; padding: 30px; border-top: 1px solid #00ff88;">
        <p>© 2026 ECO AI WORLD | Barcha huquqlar himoyalangan.</p>
        <p style="font-size: 1.4rem; font-weight: bold; color: #00ff88;">
            Mualliflar: <span style="color: #00d4ff;">Team Proff. Egamberdiev E.</span>
        </p>
    </div>
""", unsafe_allow_html=True)
