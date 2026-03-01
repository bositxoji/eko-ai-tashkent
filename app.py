import streamlit as st
import datetime
import os
import sqlite3
import requests
from groq import Groq

DB_PATH = "storage.db"

# ----------------------------
# Page config + style
# ----------------------------
st.set_page_config(page_title="ECO AI WORLD | Enterprise", page_icon="🧬", layout="wide")

st.markdown("""
<style>
.stApp { background-color: #0E1116; color: #A0A0A0; }
[data-testid="stSidebar"] { background-color: #050505 !important; border-right: 1px solid #1C1F26; }
.author-box { padding: 15px; background: rgba(28, 31, 38, 0.8); border-radius: 8px; border-left: 3px solid #FFD400; margin-bottom: 20px; }
.author-title { color: #FFD400; font-size: 11px; font-weight: bold; margin: 0; }
.author-name { color: #FFFFFF; font-size: 13px; margin-bottom: 8px; }
.main-card { background: #1C1F26; padding: 18px; border-radius: 10px; border-left: 4px solid #FF3B3B; margin-bottom: 14px; }
.soft-card { background: #141821; padding: 16px; border-radius: 10px; border: 1px solid #1C1F26; margin-bottom: 14px; }
.small-muted { color: #808080; font-size: 12px; }
h1, h2, h3 { color: #FFFFFF !important; font-family: 'Inter', sans-serif; }
.danger-text { color: #FF3B3B; font-weight: bold; animation: pulse 2s infinite; }
@keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Safe Groq client (no traceback)
# ----------------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

# ----------------------------
# DB helpers
# ----------------------------
def db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def get_latest_posts(limit=20):
    conn = db()
    rows = conn.execute(
        "SELECT id, created_at, section, title, summary, source, url, lang FROM posts ORDER BY created_at DESC LIMIT ?",
        (limit,)
    ).fetchall()
    conn.close()
    return rows

def search_posts(q, limit=50):
    conn = db()
    rows = conn.execute(
        """SELECT id, created_at, section, title, summary, source, url, lang
           FROM posts
           WHERE title LIKE ? OR summary LIKE ?
           ORDER BY created_at DESC LIMIT ?""",
        (f"%{q}%", f"%{q}%", limit)
    ).fetchall()
    conn.close()
    return rows

def get_month_report(year: int, month: int, lang: str):
    conn = db()
    r = conn.execute(
        "SELECT year, month, lang, content, created_at FROM reports WHERE year=? AND month=? AND lang=?",
        (year, month, lang)
    ).fetchone()
    conn.close()
    return r

# ----------------------------
# Air quality (Open-Meteo, key-free)
# ----------------------------
@st.cache_data(ttl=600)
def geocode_city(city: str):
    url = "https://geocoding-api.open-meteo.com/v1/search"
    r = requests.get(url, params={"name": city, "count": 1, "language": "en", "format": "json"}, timeout=20)
    r.raise_for_status()
    data = r.json()
    if not data.get("results"):
        return None
    p = data["results"][0]
    return {"lat": p["latitude"], "lon": p["longitude"], "name": p["name"], "country": p.get("country")}

@st.cache_data(ttl=600)
def air_quality(lat: float, lon: float):
    url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    params = {
        "latitude": lat, "longitude": lon,
        "current": ["pm2_5", "pm10", "nitrogen_dioxide", "ozone", "sulphur_dioxide", "carbon_monoxide"],
        "timezone": "auto"
    }
    r = requests.get(url, params=params, timeout=20)
    r.raise_for_status()
    return r.json()

# ----------------------------
# Sidebar
# ----------------------------
with st.sidebar:
    st.markdown("<h1>💠 ECO AI WORLD</h1>", unsafe_allow_html=True)
    st.markdown("""
    <div class="author-box">
        <p class="author-title">Ilmiy rahbar:</p><p class="author-name">E. EGAMBERDIEV</p>
        <p class="author-title">Asosiy muallif:</p><p class="author-name">A. ATAXOJAYEV</p>
        <p class="author-title">Ham-muallif:</p><p class="author-name">SODIQJONOV SAMANDARBEK</p>
        <p class="author-title">Team:</p><p class="author-name">Egamberdiev Research Group</p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    lang = st.selectbox("Til / Language", ["uz", "ru", "en", "tr"], index=0)

    page = st.radio("BO'LIMNI TANLANG:", [
        "1. Monitoring Terminal (Asosiy)",
        "2. Real-Time Air Quality (API)",
        "3. Industrial Eco Risk Scoring (Sanoat)",
        "4. Archive (Arxiv)",
        "5. Monthly Report (Oylik)",
        "6. 🧠 AI CORE (Llama 3.3)",
        "7. SILENT DISASTER (Dynamic)"
    ])
    st.divider()
    st.info(f"Bugun: {datetime.date.today()}")

# ----------------------------
# Pages
# ----------------------------
if page == "1. Monitoring Terminal (Asosiy)":
    st.title("📟 GLOBAL ECO MONITORING")
    st.markdown("<div class='main-card'>Global monitoring manbalari va jonli xaritalar.</div>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.link_button("💨 IQAIR", "https://www.iqair.com/")
    with col2: st.link_button("🚀 NASA FIRMS", "https://firms.modaps.eosdis.nasa.gov/map/")
    with col3: st.link_button("🛰️ SENTINEL", "https://apps.sentinel-hub.com/eo-browser/")
    with col4: st.link_button("🌤️ Open-Meteo", "https://open-meteo.com/")
    st.components.v1.iframe("https://earth.nullschool.net/#current/wind/surface/level/orthographic=-296.22,40.06,500", height=600)

elif page == "2. Real-Time Air Quality (API)":
    st.title("💨 REAL-TIME AIR QUALITY (API)")
    st.markdown("<div class='main-card'>Open-Meteo orqali real-time havo sifati. 401 bo‘lmaydi.</div>", unsafe_allow_html=True)

    city = st.text_input("Shahar:", "Tashkent")
    if st.button("Yangilash"):
        try:
            geo = geocode_city(city.strip())
            if not geo:
                st.warning("Shahar topilmadi.")
            else:
                aq = air_quality(geo["lat"], geo["lon"])
                cur = aq.get("current", {})
                st.write(f"📍 {geo['name']}, {geo.get('country','')}")
                c1, c2, c3 = st.columns(3)
                with c1: st.metric("PM2.5 (µg/m³)", f"{cur.get('pm2_5', 0):.1f}")
                with c2: st.metric("PM10 (µg/m³)", f"{cur.get('pm10', 0):.1f}")
                with c3: st.metric("NO₂ (µg/m³)", f"{cur.get('nitrogen_dioxide', 0):.1f}")
        except Exception:
            st.error("Air Quality API vaqtincha ishlamayapti. Keyinroq urinib ko‘ring.")

elif page == "3. Industrial Eco Risk Scoring (Sanoat)":
    st.title("🏭 INDUSTRIAL ECO RISK SCORING")
    st.markdown("<div class='main-card'>Sanoat obyektlari uchun risk scoring.</div>", unsafe_allow_html=True)

    a1, a2, a3 = st.columns(3)
    with a1:
        industry = st.selectbox("Sanoat turi", ["Neft/gaz", "Kimyo", "Metallurgiya", "Tekstil", "Oziq-ovqat", "Energetika", "Boshqa"])
        production = st.slider("Quvvat (1–10)", 1, 10, 6)
        incidents = st.slider("Incidentlar (yiliga)", 0, 20, 1)
    with a2:
        air = st.slider("Havo emissiya riski (1–10)", 1, 10, 6)
        water = st.slider("Oqava suv riski (1–10)", 1, 10, 6)
        waste = st.slider("Chiqindi riski (1–10)", 1, 10, 5)
    with a3:
        compliance = st.slider("Compliance/ISO (1–10)", 1, 10, 5)
        controls = st.slider("Filtr/ETP nazorat (1–10)", 1, 10, 5)
        community = st.slider("Aholiga yaqinlik (1–10)", 1, 10, 6)

    base = {"Neft/gaz": 15, "Kimyo": 18, "Metallurgiya": 16, "Tekstil": 10, "Oziq-ovqat": 8, "Energetika": 14, "Boshqa": 12}[industry]
    risk = base + production*3 + incidents*2.5 + air*4 + water*4 + waste*3 + community*2 - compliance*3.5 - controls*3.5
    risk = max(0, min(100, risk))

    st.metric("Industrial Eco Risk (0–100)", int(round(risk)))
    st.progress(risk/100)
    st.write("Baholash:", risk_level(risk))

elif page == "4. Archive (Arxiv)":
    st.title("🗂️ ARCHIVE")
    q = st.text_input("Qidirish (title/summary):")
    rows = search_posts(q) if q.strip() else get_latest_posts(30)

    if not rows:
        st.info("Arxiv bo‘sh. Cron job ishlaganda avtomatik to‘ldiriladi.")
    else:
        for r in rows:
            st.markdown(
                f"<div class='soft-card'><b>{r['title']}</b><br>"
                f"<span class='small-muted'>{r['created_at']} | {r['section']} | {r['source']} | {r['lang']}</span><br>"
                f"{r['summary']}<br>"
                f"<span class='small-muted'>{r['url']}</span></div>",
                unsafe_allow_html=True
            )

elif page == "5. Monthly Report (Oylik)":
    st.title("📄 MONTHLY REPORT")
    today = datetime.date.today()
    year = st.number_input("Year", value=today.year, step=1)
    month = st.number_input("Month (1-12)", value=today.month, step=1, min_value=1, max_value=12)

    rep = get_month_report(int(year), int(month), lang)
    if not rep:
        st.info("Bu oy uchun report yo‘q. Cron job har oyning 1-kuni yaratadi.")
    else:
        st.markdown("<div class='main-card'><b>Report</b></div>", unsafe_allow_html=True)
        st.write(rep["content"])
        st.caption(f"Created at: {rep['created_at']}")

elif page == "6. 🧠 AI CORE (Llama 3.3)":
    st.title("🧠 AI CORE")

    if client is None:
        st.markdown("<div class='soft-card'><b>AI vaqtincha o‘chiq</b><div class='small-muted'>Render ENV’da GROQ_API_KEY bo‘lsa ishlaydi.</div></div>", unsafe_allow_html=True)
        st.stop()

    if "chat" not in st.session_state:
        st.session_state.chat = []

    for msg in st.session_state.chat:
        st.markdown(f"<div class='soft-card'><b>{'🧑 Siz' if msg['role']=='user' else '🤖 AI'}:</b><br>{msg['content']}</div>", unsafe_allow_html=True)

    q = st.text_input("Savol:", placeholder="Ekologiya bo‘yicha savol bering...")
    if st.button("Yuborish") and q.strip():
        st.session_state.chat.append({"role": "user", "content": q.strip()})
        try:
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "Sen ekolog-analitik AI'san. Javobni ilmiy, aniq va amaliy ber."},
                    *st.session_state.chat
                ],
            )
            ans = completion.choices[0].message.content
            st.session_state.chat.append({"role": "assistant", "content": ans})
            st.rerun()
        except Exception:
            st.error("AI xizmatida muammo. Keyinroq urinib ko‘ring.")

elif page == "7. SILENT DISASTER (Dynamic)":
    st.title("🤫 SILENT DISASTER (Dynamic)")
    st.markdown("<div class='main-card'>Bu bo‘lim endi arxivdan avtomatik yangilanadi.</div>", unsafe_allow_html=True)

    rows = get_latest_posts(10)
    if not rows:
        st.info("Hali kontent yo‘q. Cron job ishlaganda bu bo‘lim avtomatik to‘lib boradi.")
    else:
        for r in rows[:5]:
            st.markdown(
                f"<div class='soft-card'><b>{r['title']}</b><br>"
                f"<span class='small-muted'>{r['created_at']} | {r['section']}</span><br>"
                f"{r['summary']}</div>",
                unsafe_allow_html=True
            )

st.markdown("""
<div style='text-align: center; border-top: 1px solid #1C1F26; padding: 18px;'>
© 2026 ECO AI WORLD | Egamberdiev Research Group
</div>
""", unsafe_allow_html=True)
