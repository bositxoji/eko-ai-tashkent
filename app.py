import streamlit as st

# 1. SEO va Sahifa sozlamalari
st.set_page_config(
    page_title="ECO-INSIGHT | Global Monitoring Center",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Professional Dizayn (CSS)
st.markdown("""
    <style>
    /* Asosiy fon va matn */
    .stApp {
        background: linear-gradient(135deg, #0a0f0d 0%, #020205 100%);
        color: #e0e0e0;
    }
    
    /* Kartalar uslubi */
    .service-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 25px;
        border: 1px solid rgba(0, 212, 255, 0.2);
        transition: 0.3s;
        height: 250px;
    }
    .service-card:hover {
        border-color: #00ff88;
        box-shadow: 0 0 20px rgba(0, 255, 136, 0.2);
        transform: translateY(-5px);
    }
    
    /* Sarlavhalar */
    h1, h2, h3 {
        color: #00ff88 !important;
        font-family: 'Orbitron', sans-serif;
    }
    
    /* Tugmalar */
    .stLinkButton > a {
        background: linear-gradient(90deg, #00ff88 0%, #00d4ff 100%) !important;
        color: black !important;
        font-weight: bold !important;
        border-radius: 10px !important;
        border: none !important;
        text-align: center;
        display: block;
    }
    </style>
    """, unsafe_allow_html=True)

# Sarlavha qismi
st.title("🌱 ECO-INSIGHT GLOBAL PORTAL")
st.markdown("#### *Dunyo ekologiyasini real vaqt rejimida kuzatish va tahlil qilish tizimi*")

st.divider()

# --- XIZMATLAR QATORI ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""<div class="service-card">
        <h3>💨 IQAIR</h3>
        <p>Havo sifati, PM2.5 zarralari va shahar reytinglari.</p>
    </div>""", unsafe_allow_html=True)
    st.link_button("Havoni tekshirish", "https://www.iqair.com")

with col2:
    st.markdown("""<div class="service-card">
        <h3>🛰️ NASA EARTH</h3>
        <p>Sun'iy yo'ldosh tasvirlari va global harorat o'zgarishi.</p>
    </div>""", unsafe_allow_html=True)
    st.link_button("Kosmosdan ko'rish", "https://earth.gsfc.nasa.gov")

with col3:
    st.markdown("""<div class="service-card">
        <h3>🤖 GROK AI</h3>
        <p>X-Grok orqali ekologik ma'lumotlarni chuqur tahlil qilish.</p>
    </div>""", unsafe_allow_html=True)
    st.link_button("AI Tahlilni boshlash", "https://grok.com")

with col4:
    st.markdown("""<div class="service-card">
        <h3>🔥 DISASTER MAP</h3>
        <p>Dunyo bo'ylab yong'in va tabiiy ofatlar monitoringi.</p>
    </div>""", unsafe_allow_html=True)
    st.link_button("Ofatlarni kuzatish", "https://firms.modaps.eosdis.nasa.gov/map/")

st.divider()

# --- JONLI XARITA (Siz aytgan hayratlanarli qism) ---
st.subheader("🌐 Global havo oqimlari (Live Wind & Weather)")
# Bu qism saytingiz ichida jonli shamol xaritasini ko'rsatadi
st.components.v1.iframe("https://earth.nullschool.net/#current/wind/surface/level/orthographic=-296.22,40.06,600", height=600)

st.divider()

# --- EKOLOGIK KALKULYATOR (Interaktiv xizmat) ---
st.subheader("📊 Shaxsiy Eco-Kalkulyator")
c1, c2 = st.columns(2)
with c1:
    km = st.number_input("Bir kunda necha km mashina haydaysiz?", 0, 500, 10)
    meat = st.selectbox("Go'sht iste'moli darajasi", ["Kam", "O'rtacha", "Ko'p"])
with c2:
    carbon = (km * 0.12) + (10 if meat == "Ko'p" else 5)
    st.metric("Sizning kunlik CO2 chiqindingiz (taxminan):", f"{carbon} kg")

# Footer - SEO uchun
st.markdown("""
---
*Kalit so'zlar: Eco Portal, NASA Data Analysis, IQAir Uzbekistan, Global Climate Tracker, Grok AI Ecology*
""")
