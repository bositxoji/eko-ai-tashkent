import streamlit as st
import datetime
import pandas as pd
from groq import Groq

# 1. API VA GOOGLE VERIFICATION SOZLAMASI
# Siz bergan Google Search Console kodi shu yerda:
GOOGLE_VERIFICATION_CODE = """
<head>
    <meta name="google-site-verification" content="ZkAtTf6Ut4FM76-c3qns2vqHjD4OZLKIxw_i2iw7bTY" />
</head>
"""

client = Groq(api_key="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")

# 2. SAHIFA SOZLAMALARI
st.set_page_config(page_title="ECO AI WORLD | Enterprise", page_icon="🧬", layout="wide")

# Google tasdiqlash kodini saytga yashirincha kiritish
st.markdown(GOOGLE_VERIFICATION_CODE, unsafe_allow_html=True)

# 3. "SILENT THREAT" PREMIUM DIZAYNI
st.markdown("""
    <style>
    .stApp { background-color: #0E1116; color: #A0A0A0; }
    [data-testid="stSidebar"] { background-color: #050505 !important; border-right: 1px solid #1C1F26; }
    
    .author-box {
        padding: 15px;
        background: rgba(28, 31, 38, 0.8);
        border-radius: 8px;
        border-left: 3px solid #FFD400;
        margin-top: 10px;
        margin-bottom: 20px;
    }
    .author-title { color: #FFD400; font-size: 11px; font-weight: bold; margin: 0; text-transform: uppercase; }
    .author-name { color: #FFFFFF; font-size: 13px; margin-bottom: 8px; font-weight: 500; }

    h1 { color: #FFFFFF !important; font-family: 'Inter', sans-serif; text-shadow: 0 0 10px rgba(0,255,136,0.2); }
    h2 { color: #FFD400 !important; }
    .main-card { background: #1C1F26; padding: 25px; border-radius: 8px; border-left: 4px solid #FF3B3B; margin-bottom: 20px; }
    .danger-alert { color: #FF3B3B; font-weight: bold; animation: pulse 2s infinite; }
    @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.4; } 100% { opacity: 1; } }
    </style>
    """, unsafe_allow_html=True)

# --- NAVIGATSIYA ---
with st.sidebar:
    st.markdown("<h1>💠 ECO NAVIGATION</h1>", unsafe_allow_html=True)
    
    # MUALLIFLAR TARKIBI
    st.markdown("""
    <div class="author-box">
        <p class="author-title">Ilmiy rahbar:</p>
        <p class="author-name">E. EGAMBERDIEV</p>
        <p class="author-title">Muallif:</p>
        <p class="author-name">A. ATAXOJAYEV</p>
        <p class="author-title">Team:</p>
        <p class="author-name">Egamberdiev</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    page = st.radio("MENYU / MENU:", [
        "1. Monitoring Terminal (Asosiy)", 
        "2. Water Quality (Suv sifati)", 
        "3. Soil Monitoring (Tuproq nazorati)",
        "4. Climate Change (Iqlim o'zgarishi)",
        "5. Disasters & Hazards (Tabiiy ofatlar)",
        "6. 🧠 AI CORE (Llama 3 Yadro)",
        "7. YOUR BODY vs ENV. (Shaxsiy xavf)",
        "8. SILENT DISASTER (Jim falokat)"
    ])
    st.divider()
    st.success("Global ekologik monitoring tizimi.")

# =================================================================
# 1. MONITORING TERMINAL
# =================================================================
if page == "1. Monitoring Terminal (Asosiy)":
    st.title("📟 ECO AI WORLD: GLOBAL MONITORING")
    st.markdown("<h2>Real-vaqt rejimida global ekologik razvedka tizimi.</h2>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="main-card"><h3>💨 IQAIR</h3><p>Havo sifati monitoringi.</p></div>', unsafe_allow_html=True)
        st.link_button("Launch IQAir", "https://www.iqair.com/")
    with col2:
        st.markdown('<div class="main-card"><h3>🚀 NASA FIRMS</h3><p>Yong\'inlar va ofatlar.</p></div>', unsafe_allow_html=True)
        st.link_button("NASA FIRMS", "https://firms.modaps.eosdis.nasa.gov/map/")
    with col3:
        st.markdown('<div class="main-card"><h3>🤖 GROK AI</h3><p>AI Analitika tizimi.</p></div>', unsafe_allow_html=True)
        st.link_button("Grok Chat", "https://grok.com")
    with col4:
        st.markdown('<div class="main-card"><h3>🛰️ SENTINEL</h3><p>Sputnik tasvirlari.</p></div>', unsafe_allow_html=True)
        st.link_button("Sentinel-2 Explorer", "https://apps.sentinel-hub.com/eo-browser/")

    st.divider()
    st.subheader("🌍 Jonli Global Oqimlar (Wind / Particulates)")
    st.components.v1.iframe("https://earth.nullschool.net/#current/wind/surface/level/orthographic=-296.22,40.06,500", height=600)

# =================================================================
# 6. 🧠 AI CORE (LLAMA 3.3)
# =================================================================
elif page == "6. 🧠 AI CORE (Llama 3 Yadro)":
    st.title("🤖 AI CORE: Llama 3 Intelligence")
    st.markdown('<div class="main-card"><h4>Llama 3: Big Data Eksperti</h4><p>Haqiqatni soniyalar ichida fosh qiladi.</p></div>', unsafe_allow_html=True)

    user_input = st.text_input("Ekologik savol yoki prognoz so'rang:", placeholder="Masalan: 2050-yilda global isish oqibatlari...")
    
    if st.button("Tahlilni boshlash / Run AI"):
        if user_input:
            with st.spinner('AI oylamoqda...'):
                try:
                    completion = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": "Sen Silent Threat loyihasining professional AI ekologisan. Javoblaring aniq, ilmiy va qisqa bo'lsin."},
                            {"role": "user", "content": user_input}
                        ],
                        model="llama-3.3-70b-versatile",
                    )
                    st.markdown(f'<div style="background:black; padding:20px; border-left: 5px solid #FFD400; color:white;"><b>AI HUKMI:</b><br><br>{completion.choices[0].message.content}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Xato: {e}")

# =================================================================
# 7. YOUR BODY vs ENVIRONMENT
# =================================================================
elif page == "7. YOUR BODY vs ENV. (Shaxsiy xavf)":
    st.title("🫀 YOUR BODY vs ENVIRONMENT 🌍")
    st.markdown('<p class="danger-alert">Tanangiz tashqi muhit bilan urushda.</p>', unsafe_allow_html=True)
    
    
    
    age = st.number_input("Yoshingiz:", 1, 100, 25)
    st.markdown('<div class="main-card">Sizning tanangiz hozirgi havoda filtr vazifasini o\'tamoqda.</div>', unsafe_allow_html=True)
    
    if st.button("Xavfni hisoblash"):
        impact = age * 0.7
        st.subheader(f"Prognoz: Ekologik yuklama darajasi +{int(impact)}% ga teng.")

# =================================================================
# 8. SILENT DISASTER (JIM FALOKAT)
# =================================================================
elif page == "8. SILENT DISASTER (Jim falokat)":
    st.title("🤫 THE SILENT THREAT")
    st.markdown("<p style='color: #FFD400;'>Hamma narsa tinchdek tuyuladi. Ammo ma'lumotlar boshqa narsani aytmoqda.</p>", unsafe_allow_html=True)
    
    st.image("https://images.unsplash.com/photo-1464822759023-fed622ff2c3b", use_container_width=True)
    
    if st.button("Yashirin xavfni ko'rish"):
        st.markdown("""
        <div class="main-card">
            <h3 class="danger-alert">🔴 STATUS: KRITIK</h3>
            <p>Ko'rinmas mikroplastiklar va yer osti suvlari zaharlanishi allaqachon qaytarilmas nuqtada.</p>
        </div>
        """, unsafe_allow_html=True)

# QOLGAN SAHIFALAR
elif page == "2. Water Quality (Suv sifati)":
    st.title("💧 Water Quality Hub")
    st.link_button("UNEP Water", "https://www.unep.org/explore-topics/water")
elif page == "5. Disasters & Hazards (Tabiiy ofatlar)":
    st.title("🚨 Ofatlar monitoringi")
    st.link_button("USGS Earthquake", "https://earthquake.usgs.gov/")

# --- FOOTER ---
st.markdown("<div style='text-align: center; border-top: 1px solid #1C1F26; padding: 20px;'>© 2026 ECO AI WORLD | Team Egamberdiev</div>", unsafe_allow_html=True)
