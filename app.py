import streamlit as st

# 1. SEO VA SAHIFA SOZLAMALARI
st.set_page_config(
    page_title="ECO-INSIGHT | Global Monitoring Center",
    page_icon="🌍",
    layout="wide"
)

# 2. PROFESSIONAL ECO-DIZAYN (CSS) - Barcha elementlar saqlangan
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(180deg, #050a05 0%, #000000 100%);
        color: #e0f2f1;
    }
    .service-card {
        background: rgba(0, 255, 136, 0.03);
        border: 1px solid rgba(0, 255, 136, 0.2);
        border-radius: 15px;
        padding: 20px;
        transition: 0.4s;
        height: 200px;
    }
    .service-card:hover {
        background: rgba(0, 255, 136, 0.08);
        border-color: #00ff88;
        box-shadow: 0 0 15px rgba(0, 255, 136, 0.3);
        transform: translateY(-5px);
    }
    h1, h2, h3 { color: #00ff88 !important; }
    .stLinkButton > a {
        background: transparent !important;
        border: 1px solid #00ff88 !important;
        color: #00ff88 !important;
        width: 100%;
        text-align: center;
        border-radius: 8px;
        font-weight: bold;
    }
    .stLinkButton > a:hover {
        background: #00ff88 !important;
        color: black !important;
    }
    /* Footer dizayni */
    .footer-container {
        text-align: center;
        margin-top: 50px;
        padding: 30px;
        border-top: 1px solid rgba(0, 255, 136, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)

# --- SAHIFA BOSH QISMI ---
st.title("🌐 ECO-INSIGHT: GLOBAL EKOLOGIK MONITORING")
st.markdown("""
    **Ushbu platforma NASA, IQAIR va Grok AI ma'lumotlari asosida global ekologik holatni tahlil qiladi.**
    *Maqsadimiz: Sayyoramizning real vaqtdagi holatini hamma uchun ochiq va tushunarli qilish.*
""")

st.divider()

# --- ASOSIY XIZMATLAR (4 ta ustun) ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="service-card"><h3>💨 IQAIR</h3><p>Havo sifati va PM2.5 monitoringi. Dunyo shaharlari reytingi.</p></div>', unsafe_allow_html=True)
    st.link_button("Havoni tekshirish", "https://www.iqair.com")

with col2:
    st.markdown('<div class="service-card"><h3>🛰️ NASA EARTH</h3><p>Kosmosdan yerning real holati va sun\'iy yo\'ldosh tasvirlari.</p></div>', unsafe_allow_html=True)
    st.link_button("NASA tasvirlari", "https://earth.gsfc.nasa.gov")

with col3:
    st.markdown('<div class="service-card"><h3>🤖 GROK AI</h3><p>Ekologik ma’lumotlarni chuqur tahlil qilish uchun AI yordamchisi.</p></div>', unsafe_allow_html=True)
    st.link_button("AI Tahlilni boshlash", "https://grok.com/?q=Analyze+the+latest+global+environmental+news+for+today")

with col4:
    st.markdown('<div class="service-card"><h3>🔥 FIRE MAP</h3><p>NASA FIRMS: Dunyo bo‘ylab yong‘inlar va ofatlar monitoringi.</p></div>', unsafe_allow_html=True)
    st.link_button("Jonli xarita", "https://firms.modaps.eosdis.nasa.gov/map/")

st.divider()

# --- JONLI XARITA (Live Wind & Weather) ---
st.subheader("🌍 Real vaqtdagi Global Havo Oqimlari (Live)")
st.markdown("Xaritani aylantirish orqali global shamol yo'nalishlarini kuzating:")
st.components.v1.iframe("https://earth.nullschool.net/#current/wind/surface/level/orthographic=-296.22,40.06,500", height=600)

st.divider()

# --- SEO VA MA'LUMOT MATNI ---
st.subheader("Nega ECO-INSIGHT platformasidan foydalanish kerak?")
st.write("""
Bizning platformamiz O'zbekistonda birinchilardan bo'lib global ekologik ma'lumotlarni bitta oynada jamlaydi. 
IQAir ma'lumotlari orqali havo ifloslanishini, NASA sun'iy yo'ldoshlari orqali iqlim o'zgarishini va 
Grok AI orqali kelajakdagi ekologik prognozlarni kuzatish mumkin.
""")

# --- FOOTER (Siz aytgan mualliflar qismi) ---
st.markdown(f"""
    <div class="footer-container">
        <p style="color: rgba(255,255,255,0.6);">© 2026 ECO-INSIGHT Platformasi | Barcha huquqlar himoyalangan.</p>
        <p style="font-size: 1.3rem; font-weight: bold; color: #00ff88;">
            Mualliflar: <span style="color: #00d4ff;">Team Proff. Egamberdiev E.</span>
        </p>
    </div>
""", unsafe_allow_html=True)
