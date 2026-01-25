import streamlit as st
import pandas as pd
import datetime

# 1. SEO VA SAHIFA SOZLAMALARI
st.set_page_config(
    page_title="ECO AI WORLD | Multi-Dimensional Portal",
    page_icon="💎",
    layout="wide"
)

# 2. DESIGN: PREMIUM CYBER-ECO (Poydevor dizayni saqlangan)
st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at center, #001a1a 0%, #000000 100%);
        color: #00ff88;
    }
    .main-card {
        background: rgba(0, 255, 136, 0.05);
        border: 1px solid #00ff88;
        border-radius: 12px;
        padding: 15px;
        transition: 0.3s;
    }
    .main-card:hover { box-shadow: 0 0 20px rgba(0, 255, 136, 0.3); }
    h1, h2, h3 { font-family: 'Orbitron', sans-serif; text-shadow: 0 0 10px #00ff88; }
    /* Navigatsiya tugmalari stili */
    .stSelectbox label { color: #00ff88 !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- NAVIGATSIYA MENYUSI (Poydevorni buzmaslik uchun yon menyuda) ---
with st.sidebar:
    st.title("🧭 NAVIGATSIYA")
    page = st.radio("Sahifani tanlang:", ["1. Asosiy Terminal", "2. Carbon & Finance", "3. Future Lab"])
    st.divider()
    st.info("ECO AI WORLD - Global ekologik razvedka tizimi.")

# =================================================================
# 1-SAHIFA: ASOSIY TERMINAL (Sizning poydevoringiz - 100% saqlangan)
# =================================================================
if page == "1. Asosiy Terminal":
    st.title("📟 ECO AI WORLD: ASOSIY TERMINAL")
    st.markdown("#### *Global Monitoring va NASA/ESA Integratsiyasi*")
    
    # Poydevordagi asosiy xizmatlar
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="main-card"><h3>💨 IQAIR</h3><p>Havo sifati monitoringi.</p></div>', unsafe_allow_html=True)
        st.link_button("Launch IQAir", "https://www.iqair.com/")
    with col2:
        st.markdown('<div class="main-card"><h3>🚀 NASA</h3><p>Yong\'inlar va ofatlar.</p></div>', unsafe_allow_html=True)
        st.link_button("NASA FIRMS", "https://firms.modaps.eosdis.nasa.gov/map/")
    with col3:
        st.markdown('<div class="main-card"><h3>🤖 GROK AI</h3><p>AI Analitika.</p></div>', unsafe_allow_html=True)
        st.link_button("Grok Chat", "https://grok.com")
    with col4:
        st.markdown('<div class="main-card"><h3>🛰️ SENTINEL</h3><p>Sputnik Explorer.</p></div>', unsafe_allow_html=True)
        st.link_button("Sentinel-2", "https://apps.sentinel-hub.com/eo-browser/")

    st.divider()
    st.subheader("🗺️ Real-Time Global Flow")
    st.components.v1.iframe("https://earth.nullschool.net/#current/wind/surface/level/orthographic=-296.22,40.06,500", height=600)

# =================================================================
# 2-SAHIFA: CARBON & FINANCE (YANGI)
# =================================================================
elif page == "2. Carbon & Finance":
    st.title("📈 ECO-FINANCE & CARBON HUB")
    st.markdown("#### *Uglerod Birjasi va Yashil Investitsiyalar Markazi*")
    
    
    
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("EU Carbon Permits (ETS)", "€84.12", "+1.2%")
    with m2:
        st.metric("Global Green Bond Index", "$1,420B", "+5.8%")
    with m3:
        st.metric("Nature Debt Clock", "$4.2 Trillion", "Growing")
    
    st.divider()
    st.subheader("📊 Carbon Market Deep Analysis")
    st.write("Bu yerda uglerod kreditlarining so'nggi 12 oylik tendentsiyasi va bashoratlari joylashadi.")
    st.info("Grok AI tahlili: Hozirgi kunda 'Green Credits' bozori yiliga 15% ga o'smoqda.")

# =================================================================
# 3-SAHIFA: FUTURE LAB (YANGI)
# =================================================================
elif page == "3. Future Lab":
    st.title("🧪 FUTURE LAB: SIMULATIONS")
    st.markdown("#### *Kelajak iqlimi va Bio-genetika simulyatsiyalari*")
    
    
    
    tab1, tab2 = st.tabs(["🧬 Species Resurrection", "⏳ Climate Time Machine"])
    
    with tab1:
        st.subheader("Yo'qolgan turlarni qayta tiklash monitoringi")
        st.write("Colossal Biosciences va boshqa loyihalar holati:")
        st.progress(65, text="Mammoth De-extinction Project: 65%")
        st.progress(40, text="Tasmanian Tiger Project: 40%")
    
    with tab2:
        st.subheader("Iqlimiy o'zgarish bashorati (2050-2100)")
        st.link_button("Simulyatsiyani boshlash", "https://coastal.climatecentral.org/")
        st.warning("Eslatma: Bu ma'lumotlar ilmiy modellarga asoslangan.")

# --- FOOTER (Barcha sahifalar uchun bir xil) ---
st.markdown(f"""
    <div style="text-align: center; margin-top: 50px; padding: 30px; border-top: 1px solid #00ff88;">
        <p>© 2026 ECO AI WORLD | Barcha huquqlar himoyalangan.</p>
        <p style="font-size: 1.3rem; font-weight: bold; color: #00ff88;">
            Mualliflar: <span style="color: #00d4ff;">Team Proff. Egamberdiev E.</span>
        </p>
    </div>
""", unsafe_allow_html=True)
