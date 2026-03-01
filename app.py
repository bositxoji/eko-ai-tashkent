import streamlit as st
import datetime as dt
import os
import sqlite3
import requests
from groq import Groq

DB_PATH = "storage.db"

# ----------------------------
# UI CONFIG + STYLE
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
</style>
""", unsafe_allow_html=True)

# ----------------------------
# SAFE UTILS
# ----------------------------
def clamp(x: float, lo: float = 0.0, hi: float = 100.0) -> float:
    return max(lo, min(hi, x))

def risk_level(score: float) -> str:
    if score >= 80: return "Juda yuqori"
    if score >= 60: return "Yuqori"
    if score >= 40: return "O‘rtacha"
    if score >= 20: return "Past"
    return "Juda past"

def now_utc_iso() -> str:
    return dt.datetime.utcnow().replace(microsecond=0).isoformat()

# ----------------------------
# DB LAYER (auto init)
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
    conn.execute("""
    CREATE TABLE IF NOT EXISTS meta (
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL
    );
    """)
    conn.commit()
    conn.close()

def meta_get(key: str):
    conn = db()
    r = conn.execute("SELECT value FROM meta WHERE key=?", (key,)).fetchone()
    conn.close()
    return r["value"] if r else None

def meta_set(key: str, value: str):
    conn = db()
    conn.execute("INSERT OR REPLACE INTO meta(key, value) VALUES(?,?)", (key, value))
    conn.commit()
    conn.close()

def get_latest_posts(limit=20, lang=None):
    conn = db()
    if lang:
        rows = conn.execute(
            "SELECT id, created_at, section, title, summary, source, url, lang FROM posts WHERE lang=? ORDER BY created_at DESC LIMIT ?",
            (lang, limit)
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT id, created_at, section, title, summary, source, url, lang FROM posts ORDER BY created_at DESC LIMIT ?",
            (limit,)
        ).fetchall()
    conn.close()
    return rows

def search_posts(q, limit=50, lang=None):
    conn = db()
    if lang:
        rows = conn.execute(
            """SELECT id, created_at, section, title, summary, source, url, lang
               FROM posts
               WHERE lang=? AND (title LIKE ? OR summary LIKE ?)
               ORDER BY created_at DESC LIMIT ?""",
            (lang, f"%{q}%", f"%{q}%", limit)
        ).fetchall()
    else:
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

def post_exists(url: str, lang: str) -> bool:
    conn = db()
    r = conn.execute("SELECT 1 FROM posts WHERE url=? AND lang=? LIMIT 1", (url, lang)).fetchone()
    conn.close()
    return r is not None

def save_post(section, title, summary, source, url, lang):
    conn = db()
    conn.execute(
        "INSERT INTO posts(created_at, section, title, summary, source, url, lang) VALUES (?,?,?,?,?,?,?)",
        (now_utc_iso(), section, title, summary, source, url, lang)
    )
    conn.commit()
    conn.close()

# init DB now (prevents "no such table")
init_db()

# ----------------------------
# GROQ (safe)
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
# SELF-UPDATING ARCHIVE (NO CRON)
# - 6 soatda bir marta RSS dan 3-4 ta item olib DBga yozadi
# - AI bo'lsa: summary qiladi
# - AI bo'lmasa: qisqa fallback summary
# ----------------------------
RSS_SOURCES = [
    ("UN News - Climate", "https://news.un.org/feed/subscribe/en/news/topic/climate-change/feed/rss.xml"),
    ("NASA Earth Observatory", "https://earthobservatory.nasa.gov/feeds/earth-observatory.rss"),
    ("World Bank - Environment", "https://www.worldbank.org/en/topic/environment/rss"),
]

def simple_rss_extract(xml_text: str, limit: int = 4):
    items = []
    parts = xml_text.split("<item>")
    for p in parts[1:limit+1]:
        title = ""
        link = ""
        if "<title>" in p and "</title>" in p:
            title = p.split("<title>")[1].split("</title>")[0].strip()
        if "<link>" in p and "</link>" in p:
            link = p.split("<link>")[1].split("</link>")[0].strip()
        if title and link:
            items.append((title, link))
    return items

def ai_summarize(title: str, url: str, lang: str):
    # fallback
    if client is None:
        return ("Climate", f"{title}. Batafsil: {url}")

    prompt = f"""
Til: {lang}
Sarlavha: {title}
Manba: {url}

2-3 gaplik ekologik summary yoz.
Bo‘limni tanla: Air / Water / Climate / Disasters / Industry.
Faqat shu formatda qaytar:
SECTION: ...
SUMMARY: ...
"""
    try:
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
        )
        text = res.choices[0].message.content.strip()
        section = "Climate"
        summary = text[:280]
        if "SECTION:" in text:
            section = text.split("SECTION:")[1].splitlines()[0].strip() or "Climate"
        if "SUMMARY:" in text:
            summary = text.split("SUMMARY:")[1].strip()
        return (section, summary)
    except Exception:
        return ("Climate", f"{title}. Batafsil: {url}")

def refresh_archive_if_needed(lang: str, hours: int = 6):
    """
    Sayt ochilganda chaqiriladi.
    Ekranga xato/traceback chiqarmaydi.
    """
    last = meta_get(f"last_update_{lang}")
    do_refresh = True
    if last:
        try:
            last_dt = dt.datetime.fromisoformat(last)
            do_refresh = (dt.datetime.utcnow() - last_dt) > dt.timedelta(hours=hours)
        except Exception:
            do_refresh = True

    if not do_refresh:
        return

    # yangilash (silent)
    try:
        for source_name, rss in RSS_SOURCES:
            try:
                r = requests.get(rss, timeout=25)
                r.raise_for_status()
                items = simple_rss_extract(r.text, limit=3)
            except Exception:
                continue

            for title, url in items:
                if post_exists(url, lang):
                    continue
                section, summary = ai_summarize(title, url, lang)
                save_post(section, title, summary, source_name, url, lang)

        meta_set(f"last_update_{lang}", now_utc_iso())
    except Exception:
        # butunlay jim: foydalanuvchiga sharmandali traceback yo‘q
        return

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

    # Self-updating: sahifaga kirganda arxivni yangilab turadi (jim)
    refresh_archive_if_needed(lang=lang, hours=6)

    page = st.radio("BO'LIMNI TANLANG:", [
        "1. Monitoring Terminal",
        "2. Real-Time Air Quality",
        "3. Industrial Eco Risk Scoring",
        "4. Archive",
        "5. Monthly Report",
        "6. 🧠 AI CORE",
        "7. SILENT DISASTER"
    ])

    st.divider()
    st.info(f"Bugun: {dt.date.today()}")

# ----------------------------
# PAGES (NO TRACEBACK: everything guarded)
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

elif page == "4. Archive":
    st.title("🗂️ ARCHIVE")
    st.markdown("<div class='main-card'>Arxiv o‘zi yangilanadi (Cron shart emas).</div>", unsafe_allow_html=True)

    q = st.text_input("Qidirish (title/summary):")
    try:
        rows = search_posts(q, lang=lang) if q.strip() else get_latest_posts(30, lang=lang)
    except Exception:
        rows = []

    if not rows:
        st.info("Arxiv hozircha bo‘sh. Saytga yana kirilganda u o‘zi to‘lib boradi.")
    else:
        for r in rows:
            st.markdown(
                f"<div class='soft-card'><b>{r['title']}</b><br>"
                f"<span class='small-muted'>{r['created_at']} | {r['section']} | {r['source']} | {r['lang']}</span><br>"
                f"{r['summary']}<br>"
                f"<span class='small-muted'>{r['url']}</span></div>",
                unsafe_allow_html=True
            )

elif page == "5. Monthly Report":
    st.title("📄 MONTHLY REPORT")
    st.markdown("<div class='main-card'>Hozircha report qo‘lda/AI bilan keyin avtomatlashtiramiz. (Free rejimda ham bo‘ladi)</div>", unsafe_allow_html=True)

    today = dt.date.today()
    year = st.number_input("Year", value=today.year, step=1)
    month = st.number_input("Month (1-12)", value=today.month, step=1, min_value=1, max_value=12)

    try:
        rep = get_month_report(int(year), int(month), lang)
    except Exception:
        rep = None

    if not rep:
        st.info("Bu oy uchun report hali yo‘q.")
        # xohlasangiz: “Generate report now” tugmasini keyingi bosqichda qo‘shamiz
    else:
        st.write(rep["content"])
        st.caption(f"Created at: {rep['created_at']}")

elif page == "6. 🧠 AI CORE":
    st.title("🧠 AI CORE")

    if client is None:
        st.info("AI hozir mavjud emas (serverda GROQ_API_KEY yo‘q).")
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

elif page == "7. SILENT DISASTER":
    st.title("🤫 SILENT DISASTER")
    st.markdown("<div class='main-card'>Arxivdan eng keskin ekologik voqealar.</div>", unsafe_allow_html=True)

    try:
        rows = get_latest_posts(12, lang=lang)
    except Exception:
        rows = []

    if not rows:
        st.info("Hali kontent yo‘q. Saytga keyinroq kirganda avtomatik to‘lib boradi.")
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
