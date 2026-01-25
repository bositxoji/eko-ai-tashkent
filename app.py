import streamlit as st
import datetime
from groq import Groq

# 1. GOOGLE SEARCH CONSOLE VERIFICATION
# Bu kod Google botlari saytingizni tasdiqlashi uchun shart!
GOOGLE_TAG = """<meta name="google-site-verification" content="ZkAtTf6Ut4FM76-c3qns2vqHjD4OZLKIxw_i2iw7bTY" />"""

# 2. API SOZLAMASI
client = Groq(api_key="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")

# 3. SAHIFA SOZLAMALARI
st.set_page_config(page_title="ECO AI WORLD | Enterprise", page_icon="🧬", layout="wide")
st.markdown(f"<head>{GOOGLE_TAG}</head>", unsafe_allow_html=True)

# 4. SILENT THREAT DIZAYNI
st.markdown("""
    <style>
    .stApp { background-color: #0E1116; color: #A0A0A0; }
    [data-testid="stSidebar"] { background-color: #050505 !important; border-right: 1px solid #1C1F26; }
    .author-box { padding: 15px; background: rgba(28, 31, 38, 0.8); border-radius: 8px; border-left: 3px solid #FFD400; margin-bottom: 20px; }
    .author-title { color: #FFD400; font-size: 11px; font-weight: bold; margin: 0; }
    .author-name { color: #FFFFFF; font-size: 13px; margin-bottom: 8px; }
    .main-card { background: #1C1F26; padding: 25px; border-radius: 8px; border-left: 4px solid #FF3B3B; margin-bottom: 20px; }
    h1, h2, h3 { color: #FFFFFF !important; font-family: 'Inter', sans-serif; }
    .danger-text { color: #FF3B3B; font-weight: bold; animation: pulse 2s infinite; }
    @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }
    </style>
    """, unsafe_allow_html=True)

# --- NAVIGATSIYA (8 TA TO'LIQ BO'LIM) ---
with st.sidebar:
    st.markdown("<h1>💠 ECO AI WORLD</h1>", unsafe_allow_html=True)
    
    # MUALLIFLAR BLOKI (Siz xohlagandek)
    st.markdown(f"""<div class="author-box">
        <p class="author-title">Ilmiy rahbar:</p><p class="author-name">E. EGAMBERDIEV</p>
        <p class="author-title">Muallif:</p><p class="author-name">A. ATAXOJAYEV</p>
        <p class="author-title">Team:</p><p class="author-name">Egamberdiev</p>
    </div>""", unsafe_allow_html=True)
    
    st.divider()
    page = st.radio("BO'LIMNI TANLANG:", [
        "1. Monitoring Terminal (Asosiy)", 
        "2. Water Quality (Suv sifati)", 
        "3. Soil Monitoring (Tuproq)",
        "4. Climate Change (Iqlim)",
        "5. Disasters & Hazards (Ofatlar)",
        "6. 🧠 AI CORE (Llama 3.3)",
        "7. YOUR BODY vs ENV. (Xavf)",
        "8. SILENT DISASTER (Haqiqat)"
    ])
    st.divider()
    st.info(f"Bugun: {datetime.date.today()}")

# =================================================================
# SAHIFALAR LOGIKASI
# =================================================================

if page == "1. Monitoring Terminal (Asosiy)":
    st.title("📟 GLOBAL ECO MONITORING")
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.link_button("💨 IQAIR", "https://www.iqair.com/")
    with col2: st.link_button("🚀 NASA FIRMS", "https://firms.modaps.eosdis.nasa.gov/map/")
    with col3: st.link_button("🤖 GROK AI", "https://grok.com")
    with col4: st.link_button("🛰️ SENTINEL", "https://apps.sentinel-hub.com/eo-browser/")
    st.components.v1.iframe("https://earth.nullschool.net/#current/wind/surface/level/orthographic=-296.22,40.06,500", height=600)

elif page == "6. 🧠 AI CORE (Llama 3.3)":
    st.title("🤖 AI CORE: Llama 3.3 Intelligence")
    st.markdown('<div class="main-card">Savolingizga shafqatsiz ilmiy javob oling.</div>', unsafe_allow_html=True)
    user_query = st.text_input("Ekologik muammo haqida so'rang:")
    
    if st.button("Tahlilni boshlash"):
        if user_query:
            with st.spinner("AI tahlil qilmoqda..."):
                try:
                    # MODEL llama-3.3-70b-versatile GA O'ZGARTIRILDI
                    completion = client.chat.completions.create(
                        messages=[{"role": "system", "content": "Sen Silent Threat AI ekologisan."}, {"role": "user", "content": user_query}],
                        model="llama-3.3-70b-versatile" 
                    )
                    st.markdown(f"<div class='main-card' style='border-color:#FFD400;'>{completion.choices[0].message.content}</div>", unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Xatolik: {e}. Iltimos model nomini tekshiring.")

elif page == "7. YOUR BODY vs ENV. (Xavf)":
    st.title("🫀 YOUR BODY vs ENVIRONMENT")
    age = st.slider("Yoshingizni kiriting:", 1, 100, 25)
    st.markdown(f'<div class="main-card">Hududingizdagi ifloslanish {age} yoshli tana uchun kritik darajada.</div>', unsafe_allow_html=True)
    if st.button("Prognozni ko'rish"):
        st.write(f"Sizning nafas yo'llaringiz {int(age*1.2)} yoshli odamnikidek yuklama olmoqda.")

elif page == "8. SILENT DISASTER (Haqiqat)":
    st.title("🤫 THE SILENT DISASTER")
    st.image("https://images.unsplash.com/photo-1500382017468-9049fed747ef")
    st.markdown('<p class="danger-text">OGOHLANTIRISH: Hamma narsa ko\'ringanidan ko\'ra dahshatliroq.</p>', unsafe_allow_html=True)

# QOLGAN SAHIFALAR UCHUN SHABLON
else:
    st.title(page)
    st.info("Ushbu bo'lim ma'lumotlari yangilanmoqda...")

# --- FOOTER ---
st.markdown("<div style='text-align: center; border-top: 1px solid #1C1F26; padding: 20px;'>© 2026 ECO AI WORLD | Team Egamberdiev</div>", unsafe_allow_html=True)
