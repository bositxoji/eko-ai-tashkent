import streamlit as st
import datetime
import os
from groq import Groq

# =========================================================
# 1) GOOGLE SEARCH CONSOLE VERIFICATION
# =========================================================
GOOGLE_TAG = """<meta name="google-site-verification" content="ZkAtTf6Ut4FM76-c3qns2vqHjD4OZLKIxw_i2iw7bTY" />"""

# =========================================================
# 2) STREAMLIT PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="ECO AI WORLD | Enterprise",
    page_icon="🧬",
    layout="wide"
)

# Google verification tag (Streamlit ichida xavfsiz kiritish)
st.markdown(GOOGLE_TAG, unsafe_allow_html=True)

# =========================================================
# 3) API KEY SAFE LOADING (Render/GitHub/Local)
# =========================================================
def get_groq_key() -> str | None:
    # 1) Render / server env
    key = os.getenv("GROQ_API_KEY")
    if key and key.strip():
        return key.strip()

    # 2) Local secrets.toml (agar mavjud bo'lsa)
    # st.secrets yo'q bo'lsa, xato bermasligi uchun try
    try:
        key2 = st.secrets.get("GROQ_API_KEY")
        if key2 and str(key2).strip():
            return str(key2).strip()
    except Exception:
        pass

    return None

GROQ_API_KEY = get_groq_key()

if not GROQ_API_KEY:
    st.error(
        "❌ GROQ_API_KEY topilmadi.\n\n"
        "✅ Render'da: Environment Variables -> GROQ_API_KEY qo‘shing.\n"
        "✅ Local'da: .streamlit/secrets.toml ichiga GROQ_API_KEY yozing."
    )
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# =========================================================
# 4) SILENT THREAT DESIGN
# =========================================================
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

# =========================================================
# 5) SIDEBAR NAVIGATION
# =========================================================
with st.sidebar:
    st.markdown("<h1>💠 ECO AI WORLD</h1>", unsafe_allow_html=True)

    # AUTHORS BLOCK (SODIQJONOV SAMANDARBEK QO‘SHILDI)
    st.markdown("""
    <div class="author-box">
        <p class="author-title">Ilmiy rahbar:</p><p class="author-name">E. EGAMBERDIEV</p>
        <p class="author-title">Asosiy muallif:</p><p class="author-name">A. ATAXOJAYEV</p>
        <p class="author-title">Ham-muallif:</p><p class="author-name">SODIQJONOV SAMANDARBEK</p>
        <p class="author-title">Team:</p><p class="author-name">Egamberdiev Research Group</p>
    </div>
    """, unsafe_allow_html=True)

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

# =========================================================
# 6) PAGES LOGIC
# =========================================================
if page == "1. Monitoring Terminal (Asosiy)":
    st.title("📟 GLOBAL ECO MONITORING")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.link_button("💨 IQAIR", "https://www.iqair.com/")
    with col2:
        st.link_button("🚀 NASA FIRMS", "https://firms.modaps.eosdis.nasa.gov/map/")
    with col3:
        st.link_button("🤖 GROK AI", "https://grok.com")
    with col4:
        st.link_button("🛰️ SENTINEL", "https://apps.sentinel-hub.com/eo-browser/")

    st.components.v1.iframe(
        "https://earth.nullschool.net/#current/wind/surface/level/orthographic=-296.22,40.06,500",
        height=600
    )

elif page == "6. 🧠 AI CORE (Llama 3.3)":
    st.title("🤖 AI CORE: Llama 3.3 Intelligence")
    st.markdown('<div class="main-card">Savolingizga shafqatsiz ilmiy javob oling.</div>', unsafe_allow_html=True)

    user_query = st.text_input("Ekologik muammo haqida so'rang:")

    if st.button("Tahlilni boshlash"):
        if not user_query.strip():
            st.warning("Savol yozing.")
        else:
            with st.spinner("AI tahlil qilmoqda..."):
                try:
                    completion = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": "Sen Silent Threat AI ekologisan. Javobni ilmiy, aniq va qisqa qilib ber."},
                            {"role": "user", "content": user_query}
                        ],
                        model="llama-3.3-70b-versatile"
                    )
                    answer = completion.choices[0].message.content
                    st.markdown(
                        f"<div class='main-card' style='border-color:#FFD400;'>{answer}</div>",
                        unsafe_allow_html=True
                    )
                except Exception as e:
                    st.error(f"Xatolik: {e}")

elif page == "7. YOUR BODY vs ENV. (Xavf)":
    st.title("🫀 YOUR BODY vs ENVIRONMENT")
    age = st.slider("Yoshingizni kiriting:", 1, 100, 25)

    st.markdown(
        f'<div class="main-card">Hududingizdagi ifloslanish {age} yoshli tana uchun kritik darajada.</div>',
        unsafe_allow_html=True
    )

    if st.button("Prognozni ko'rish"):
        st.write(f"Sizning nafas yo'llaringiz {int(age * 1.2)} yoshli odamnikidek yuklama olmoqda.")

elif page == "8. SILENT DISASTER (Haqiqat)":
    st.title("🤫 THE SILENT DISASTER")
    st.image("https://images.unsplash.com/photo-1500382017468-9049fed747ef", use_container_width=True)
    st.markdown(
        '<p class="danger-text">OGOHLANTIRISH: Hamma narsa ko\'ringanidan ko\'ra dahshatliroq.</p>',
        unsafe_allow_html=True
    )

# QOLGAN SAHIFALAR UCHUN SHABLON
else:
    st.title(page)
    st.info("Ushbu bo'lim ma'lumotlari yangilanmoqda...")

# =========================================================
# 7) FOOTER
# =========================================================
st.markdown("""
<div style='text-align: center; border-top: 1px solid #1C1F26; padding: 20px;'>
© 2026 ECO AI WORLD | Egamberdiev Research Group
</div>
""", unsafe_allow_html=True)
