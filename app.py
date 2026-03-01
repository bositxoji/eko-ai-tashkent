import streamlit as st
import datetime
import os
import sqlite3
import requests
from groq import Groq

DB_PATH = "storage.db"

# ----------------------------
# CONFIG
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
# UTIL
# ----------------------------
def clamp(x: float, lo: float = 0, hi: float = 100) -> float:
    return max(lo, min(hi, x))

def risk_level(score: float) -> str:
    if score >= 80: return "Juda yuqori"
    if score >= 60: return "Yuqori"
    if score >= 40: return "O‘rtacha"
    if score >= 20: return "Past"
    return "Juda past"

# ----------------------------
# DB (AUTO INIT) — MUHIM
# ----------------------------
def db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = db()
    conn.execute("""
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TEXT NOT NULL,
        section TEXT NOT NULL,
        title TEXT NOT NULL,
        summary TEXT NOT NULL,
        source TEXT NOT NULL,
        url TEXT NOT NULL,
        lang TEXT NOT NULL
    );
    """)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        year INTEGER NOT NULL,
        month INTEGER NOT NULL,
        lang TEXT NOT NULL,
        content TEXT NOT NULL,
        created_at TEXT NOT NULL,
        UNIQUE(year, month, lang)
    );
    """)
    conn.commit()
    conn.close()

# DB ni app start bo‘lganda yaratib qo‘yamiz → “no such table” yo‘qoladi
init_db()

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
# GROQ (SAFE)
# ----------------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

# ----------------------------
# AIR QUALITY (Open-Meteo)
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
# SIDEBAR
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
        "1. Monitoring Terminal",
        "2. Real-Time Air Quality",
        "3. Industrial Eco Risk Scoring",
        "4. News Feed (AI)",
        "5. Archive",
        "6. Monthly Report",
        "7. 🧠 AI CORE",
        "8. SILENT DISASTER"
    ])
    st.divider()
    st.info(f"Bugun: {datetime.date.today()}")

# ----------------------------
# PAGES
# ----------------------------
if page == "1. Monitoring Terminal":
    st.title("📟 GLOBAL ECO MONITORING")
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.link_button("💨 IQAIR", "https://www.iqair.com/")
    with col2: st.link_button("🚀 NASA FIRMS", "https://firms.modaps.eosdis.nasa.gov/map/")
    with col3: st.link_button("🛰️ SENTINEL", "https://apps.sentinel-hub.com/eo-browser/")
    with col4: st.link_button("🌤️ Open-Meteo", "https://open-meteo.com/")
    st.components.v1.iframe("https://earth.nullschool.net/#current/wind/surface/level/orthographic=-296.22,40.06,500", height=600)

elif page == "2. Real-Time Air Quality":
    st.title("💨 REAL-TIME AIR QUALITY")
    st.markdown("<div class='main-card'>Shahar kiriting va real vaqtga yaqin havo sifatini ko‘ring.</div>", unsafe_allow_html=True)

    city = st.text_input("Shahar:", "Tashkent")
    if st.button("Yangilash"):
        try:
            geo = geocode_city(city.strip())
            if not geo:
                st.warning("Shahar topilmadi. Boshqa nom bilan urinib ko‘ring.")
            else:
                aq = air_quality(geo["lat"], geo["lon"])
                cur = aq.get("current", {})
                st.write(f"📍 {geo['name']}, {geo.get('country','')}")
                c1, c2, c3, c4 = st.columns(4)
                with c1: st.metric("PM2.5", f"{float(cur.get('pm2_5', 0)):.1f} µg/m³")
                with c2: st.metric("PM10", f"{float(cur.get('pm10', 0)):.1f} µg/m³")
                with c3: st.metric("NO₂", f"{float(cur.get('nitrogen_dioxide', 0)):.1f} µg/m³")
                with c4: st.metric("O₃", f"{float(cur.get('ozone', 0)):.1f} µg/m³")
        except Exception:
            st.error("Air Quality API vaqtincha ishlamayapti. Keyinroq urinib ko‘ring.")

elif page == "3. Industrial Eco Risk Scoring":
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
    risk = clamp(risk, 0, 100)

    st.metric("Industrial Eco Risk (0–100)", int(round(risk)))
    st.progress(risk/100)
    st.write("Baholash:", risk_level(risk))

elif page == "4. News Feed (AI)":
    st.title("📰 NEWS FEED (AI)")
    st.markdown("<div class='main-card'>Bu bo‘limni Cron Job (worker.py) avtomatik to‘ldirib boradi.</div>", unsafe_allow_html=True)

    rows = get_latest_posts(25)
    if not rows:
        st.info("Hali yangilik yo‘q. Cron Job ishga tushgach avtomatik paydo bo‘ladi.")
    else:
        for r in rows:
            st.markdown(
                f"<div class='soft-card'><b>{r['title']}</b><br>"
                f"<span class='small-muted'>{r['created_at']} | {r['section']} | {r['source']} | {r['lang']}</span><br>"
                f"{r['summary']}<br>"
                f"<span class='small-muted'>{r['url']}</span></div>",
                unsafe_allow_html=True
            )

elif page == "5. Archive":
    st.title("🗂️ ARCHIVE")
    q = st.text_input("Qidirish (title/summary):")
    rows = search_posts(q) if q.strip() else get_latest_posts(30)

    if not rows:
        st.info("Arxiv bo‘sh. Cron Job ishlaganda avtomatik to‘ldiriladi.")
    else:
        for r in rows:
            st.markdown(
                f"<div class='soft-card'><b>{r['title']}</b><br>"
                f"<span class='small-muted'>{r['created_at']} | {r['section']} | {r['source']} | {r['lang']}</span><br>"
                f"{r['summary']}<br>"
                f"<span class='small-muted'>{r['url']}</span></div>",
                unsafe_allow_html=True
            )

elif page == "6. Monthly Report":
    st.title("📄 MONTHLY REPORT")
    today = datetime.date.today()
    year = st.number_input("Year", value=today.year, step=1)
    month = st.number_input("Month (1-12)", value=today.month, step=1, min_value=1, max_value=12)

    rep = get_month_report(int(year), int(month), lang)
    if not rep:
        st.info("Bu oy uchun report hali yo‘q. Cron Job har oyning 1-kuni yaratadi.")
    else:
        st.markdown("<div class='main-card'><b>Report</b></div>", unsafe_allow_html=True)
        st.write(rep["content"])
        st.caption(f"Created at: {rep['created_at']}")

elif page == "7. 🧠 AI CORE":
    st.title("🧠 AI CORE")

    if client is None:
        st.info("AI hozir mavjud emas (serverda key sozlanmagan).")
        st.stop()

    if "chat" not in st.session_state:
        st.session_state.chat = []

    for msg in st.session_state.chat:
        st.markdown(
            f"<div class='soft-card'><b>{'🧑 Siz' if msg['role']=='user' else '🤖 AI'}:</b><br>{msg['content']}</div>",
            unsafe_allow_html=True
        )

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

elif page == "8. SILENT DISASTER":
    st.title("🤫 SILENT DISASTER")
    st.markdown("<div class='main-card'>Eng keskin ekologik voqealar (arxivdan).</div>", unsafe_allow_html=True)

    rows = get_latest_posts(10)
    if not rows:
        st.info("Hali kontent yo‘q. Cron Job ishlaganda avtomatik to‘lib boradi.")
    else:
        for r in rows[:6]:
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
