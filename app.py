import streamlit as st
import streamlit.components.v1 as components
import datetime as dt
import os
import sqlite3
import requests
from groq import Groq

import folium
from streamlit_folium import st_folium

DB_PATH = "storage.db"

# ============================
# PAGE CONFIG
# ============================
st.set_page_config(page_title="ECO AI WORLD | Enterprise", page_icon="🧬", layout="wide")

# ============================
# WOW EFFECTS (premium background + top banner)
# ============================
st.markdown("""
<style>
/* Premium animated dot grid background */
.stApp::before{
  content:"";
  position: fixed;
  inset: -40%;
  background:
    radial-gradient(circle, rgba(255,212,0,0.06) 1px, transparent 1px),
    radial-gradient(circle, rgba(255,59,59,0.04) 1px, transparent 1px);
  background-size: 46px 46px, 70px 70px;
  animation: moveBg 28s linear infinite;
  z-index: -1;
  filter: blur(.2px);
}
@keyframes moveBg{
  from{ transform: translate(0,0); }
  to{ transform: translate(-200px,-200px); }
}
.stApp{
  background: radial-gradient(1200px 600px at 40% 0%, rgba(255,59,59,0.10), transparent 60%),
              radial-gradient(1000px 500px at 80% 20%, rgba(255,212,0,0.08), transparent 60%),
              #0E1116;
  color: #A0A0A0;
}

/* Sidebar */
[data-testid="stSidebar"]{
  background: #050505 !important;
  border-right: 1px solid #1C1F26;
}

/* Typography */
h1,h2,h3 { color:#FFFFFF !important; font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, sans-serif; }
.small-muted { color:#7b8794; font-size:12px; }

/* Cards */
.author-box{
  padding: 15px;
  background: rgba(28, 31, 38, 0.80);
  border-radius: 10px;
  border-left: 3px solid #FFD400;
  margin-bottom: 18px;
}
.author-title{
  color: #FFD400;
  font-size: 11px;
  font-weight: 800;
  margin: 0;
  letter-spacing: .3px;
}
.author-name{
  color:#FFFFFF;
  font-size: 13px;
  margin-bottom: 8px;
}
.hero{
  background: linear-gradient(135deg, rgba(28,31,38,0.95), rgba(14,17,22,0.95));
  border: 1px solid #1C1F26;
  border-radius: 14px;
  padding: 18px 18px 14px 18px;
  box-shadow: 0 12px 40px rgba(0,0,0,0.35);
  margin-bottom: 14px;
  animation: fadeIn .25s ease-out;
}
.badge{
  display:inline-block;
  padding:4px 10px;
  border-radius:999px;
  font-size:12px;
  border: 1px solid rgba(255,255,255,0.10);
  background: rgba(255,255,255,0.04);
  margin-bottom: 8px;
}
.soft-card{
  background: rgba(20,24,33,0.92);
  padding: 14px;
  border-radius: 12px;
  border: 1px solid #1C1F26;
  margin-bottom: 12px;
  animation: fadeIn .2s ease-out;
}
@keyframes fadeIn { from { opacity: 0; transform: translateY(6px);} to { opacity: 1; transform: translateY(0);} }

/* Accent borders */
.accent-air { border-left: 4px solid #3b82f6; }
.accent-water { border-left: 4px solid #22c55e; }
.accent-soil { border-left: 4px solid #a16207; }
.accent-climate { border-left: 4px solid #06b6d4; }
.accent-disaster { border-left: 4px solid #ef4444; }
.accent-ai { border-left: 4px solid #a855f7; }
.accent-archive { border-left: 4px solid #f59e0b; }
.accent-industrial { border-left: 4px solid #fb7185; }
.accent-action { border-left: 4px solid #eab308; }
.accent-map { border-left: 4px solid #60a5fa; }

/* Live banner */
.live-banner{
  background: linear-gradient(90deg,#ff3b3b,#ff9900);
  padding: 10px 12px;
  border-radius: 10px;
  color: white;
  font-weight: 800;
  letter-spacing: .2px;
  text-align: center;
  border: 1px solid rgba(255,255,255,0.12);
  box-shadow: 0 12px 26px rgba(0,0,0,0.25);
  margin-bottom: 14px;
}
</style>
""", unsafe_allow_html=True)

def hero(title: str, subtitle: str, badge: str):
    st.markdown(f"""
    <div class="hero">
      <div class="badge">{badge}</div>
      <h1 style="margin:0">{title}</h1>
      <div class="small-muted">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)

# ============================
# AUTO LANGUAGE DETECTION (FREE)
# Works by redirecting user to ?lang=xx based on navigator.language
# ============================
TRANSLATIONS = {
    "uz": {
        "choose_lang": "Til / Language",
        "choose_section": "BO'LIMNI TANLANG:",
        "today": "Bugun",
        "monitoring": "1. Monitoring Terminal (Asosiy)",
        "air": "2. Real-Time Air Quality (API)",
        "water": "3. Water Quality (Suv sifati)",
        "soil": "4. Soil Monitoring (Tuproq)",
        "climate": "5. Climate Change (Iqlim)",
        "disasters": "6. Disasters & Hazards (Ofatlar)",
        "ai_core": "7. 🧠 AI CORE (Llama 3.3)",
        "silent": "8. SILENT DISASTER (Dynamic) + Arxiv",
        "industrial": "9. Industrial Eco Risk Scoring",
        "action": "10. ECO ACTION PLAN (AI)",
        "map": "11. 🌍 GLOBAL RISK MAP (WOW)",
        "city": "Shahar",
        "update": "Yangilash",
        "search": "Arxivdan qidirish (title/summary):",
        "send": "Yuborish",
        "plan": "Reja yaratish",
        "ai_missing": "AI hozir mavjud emas (serverda GROQ_API_KEY yo‘q yoki muammo bor).",
        "api_down": "API vaqtincha ishlamayapti. Keyinroq urinib ko‘ring.",
        "archive_empty": "Arxiv hozircha bo‘sh. Saytga kirilganda u o‘zi to‘lib boradi.",
        "risk": "Industrial Eco Risk (0–100)",
        "rating": "Baholash",
    },
    "en": {
        "choose_lang": "Language",
        "choose_section": "SELECT SECTION:",
        "today": "Today",
        "monitoring": "1. Monitoring Terminal (Main)",
        "air": "2. Real-Time Air Quality (API)",
        "water": "3. Water Quality",
        "soil": "4. Soil Monitoring",
        "climate": "5. Climate Change",
        "disasters": "6. Disasters & Hazards",
        "ai_core": "7. 🧠 AI CORE (Llama 3.3)",
        "silent": "8. SILENT DISASTER (Dynamic) + Archive",
        "industrial": "9. Industrial Eco Risk Scoring",
        "action": "10. ECO ACTION PLAN (AI)",
        "map": "11. 🌍 GLOBAL RISK MAP (WOW)",
        "city": "City",
        "update": "Update",
        "search": "Search archive (title/summary):",
        "send": "Send",
        "plan": "Generate plan",
        "ai_missing": "AI is unavailable (missing GROQ_API_KEY or service issue).",
        "api_down": "API is temporarily unavailable. Please try again later.",
        "archive_empty": "Archive is empty for now. It will auto-fill when the site is used.",
        "risk": "Industrial Eco Risk (0–100)",
        "rating": "Rating",
    },
    "ru": {
        "choose_lang": "Язык / Language",
        "choose_section": "ВЫБЕРИТЕ РАЗДЕЛ:",
        "today": "Сегодня",
        "monitoring": "1. Мониторинг (Основной)",
        "air": "2. Качество воздуха (API)",
        "water": "3. Качество воды",
        "soil": "4. Мониторинг почвы",
        "climate": "5. Изменение климата",
        "disasters": "6. Катастрофы и риски",
        "ai_core": "7. 🧠 AI CORE",
        "silent": "8. ТИХАЯ КАТАСТРОФА + Архив",
        "industrial": "9. Промышленный эко-риск",
        "action": "10. ЭКО ПЛАН (AI)",
        "map": "11. 🌍 ГЛОБАЛЬНАЯ КАРТА РИСКОВ (WOW)",
        "city": "Город",
        "update": "Обновить",
        "search": "Поиск в архиве (title/summary):",
        "send": "Отправить",
        "plan": "Создать план",
        "ai_missing": "AI недоступен (нет GROQ_API_KEY или ошибка сервиса).",
        "api_down": "API временно недоступен. Попробуйте позже.",
        "archive_empty": "Архив пока пуст. Он будет автоматически пополняться.",
        "risk": "Промышленный эко-риск (0–100)",
        "rating": "Оценка",
    },
    "tr": {
        "choose_lang": "Dil / Language",
        "choose_section": "BÖLÜM SEÇİN:",
        "today": "Bugün",
        "monitoring": "1. İzleme Terminali (Ana)",
        "air": "2. Hava Kalitesi (API)",
        "water": "3. Su Kalitesi",
        "soil": "4. Toprak İzleme",
        "climate": "5. İklim Değişikliği",
        "disasters": "6. Afetler ve Riskler",
        "ai_core": "7. 🧠 AI CORE",
        "silent": "8. SILENT DISASTER + Arşiv",
        "industrial": "9. Endüstriyel Eko Risk",
        "action": "10. EKO AKSİYON PLANI (AI)",
        "map": "11. 🌍 KÜRESEL RİSK HARİTASI (WOW)",
        "city": "Şehir",
        "update": "Güncelle",
        "search": "Arşivde ara (title/summary):",
        "send": "Gönder",
        "plan": "Plan oluştur",
        "ai_missing": "AI kullanılamıyor (GROQ_API_KEY eksik ya da servis sorunu).",
        "api_down": "API geçici olarak çalışmıyor. Sonra tekrar deneyin.",
        "archive_empty": "Arşiv şimdilik boş. Site kullanıldıkça otomatik dolacak.",
        "risk": "Endüstriyel Eko Risk (0–100)",
        "rating": "Değerlendirme",
    }
}

def normalize_lang(code: str) -> str:
    if not code:
        return "uz"
    code = code.lower()
    if code.startswith("ru"): return "ru"
    if code.startswith("tr"): return "tr"
    if code.startswith("en"): return "en"
    # default: Uzbek
    return "uz"

# Read query param
qp = st.query_params
lang_from_qp = normalize_lang(qp.get("lang", None))

if "lang" not in st.session_state:
    st.session_state.lang = lang_from_qp

# If user opened without lang param, redirect using browser language
# (This is the "auto-detect" piece.)
components.html("""
<script>
(function(){
  const url = new URL(window.location.href);
  if(!url.searchParams.get("lang")){
    const nav = (navigator.language || "uz").toLowerCase();
    let out = "uz";
    if(nav.startsWith("ru")) out="ru";
    else if(nav.startsWith("tr")) out="tr";
    else if(nav.startsWith("en")) out="en";
    url.searchParams.set("lang", out);
    window.location.replace(url.toString());
  }
})();
</script>
""", height=0)

lang = st.session_state.lang
def t(key: str) -> str:
    return TRANSLATIONS.get(lang, TRANSLATIONS["uz"]).get(key, key)

# ============================
# SAFE UTILS
# ============================
def now_utc_iso() -> str:
    return dt.datetime.utcnow().replace(microsecond=0).isoformat()

def clamp(x: float, lo: float = 0.0, hi: float = 100.0) -> float:
    return max(lo, min(hi, x))

def risk_level(score: float) -> str:
    if score >= 80: return {"uz":"Juda yuqori","en":"Very high","ru":"Очень высокий","tr":"Çok yüksek"}[lang]
    if score >= 60: return {"uz":"Yuqori","en":"High","ru":"Высокий","tr":"Yüksek"}[lang]
    if score >= 40: return {"uz":"O‘rtacha","en":"Medium","ru":"Средний","tr":"Orta"}[lang]
    if score >= 20: return {"uz":"Past","en":"Low","ru":"Низкий","tr":"Düşük"}[lang]
    return {"uz":"Juda past","en":"Very low","ru":"Очень низкий","tr":"Çok düşük"}[lang]

# ============================
# DB (AUTO INIT)
# ============================
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

def post_exists(url: str, lang_: str) -> bool:
    conn = db()
    r = conn.execute("SELECT 1 FROM posts WHERE url=? AND lang=? LIMIT 1", (url, lang_)).fetchone()
    conn.close()
    return r is not None

def save_post(section, title, summary, source, url, lang_):
    conn = db()
    conn.execute(
        "INSERT INTO posts(created_at, section, title, summary, source, url, lang) VALUES (?,?,?,?,?,?,?)",
        (now_utc_iso(), section, title, summary, source, url, lang_)
    )
    conn.commit()
    conn.close()

def get_latest_posts(limit=25, lang_=None):
    conn = db()
    if lang_:
        rows = conn.execute(
            "SELECT created_at, section, title, summary, source, url FROM posts WHERE lang=? ORDER BY created_at DESC LIMIT ?",
            (lang_, limit)
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT created_at, section, title, summary, source, url, lang FROM posts ORDER BY created_at DESC LIMIT ?",
            (limit,)
        ).fetchall()
    conn.close()
    return rows

def search_posts(q, limit=60, lang_=None):
    conn = db()
    if lang_:
        rows = conn.execute(
            """SELECT created_at, section, title, summary, source, url FROM posts
               WHERE lang=? AND (title LIKE ? OR summary LIKE ?)
               ORDER BY created_at DESC LIMIT ?""",
            (lang_, f"%{q}%", f"%{q}%", limit)
        ).fetchall()
    else:
        rows = conn.execute(
            """SELECT created_at, section, title, summary, source, url, lang FROM posts
               WHERE title LIKE ? OR summary LIKE ?
               ORDER BY created_at DESC LIMIT ?""",
            (f"%{q}%", f"%{q}%", limit)
        ).fetchall()
    conn.close()
    return rows

init_db()

# ============================
# GROQ (SAFE)
# ============================
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

# ============================
# Open-Meteo (Air Quality) - no annoying messages unless error
# ============================
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

# ============================
# SELF-UPDATING ARCHIVE (NO CRON)
# Fills DB silently when site is used (every 6h per language)
# ============================
RSS_SOURCES = [
    ("UN News - Climate", "https://news.un.org/feed/subscribe/en/news/topic/climate-change/feed/rss.xml"),
    ("NASA Earth Observatory", "https://earthobservatory.nasa.gov/feeds/earth-observatory.rss"),
    ("World Bank - Environment", "https://www.worldbank.org/en/topic/environment/rss"),
]

def simple_rss_extract(xml_text: str, limit: int = 3):
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

def ai_summarize(title: str, url: str, lang_: str):
    # Fallback if AI is missing
    if client is None:
        return ("Climate", f"{title}. {url}")

    prompt = f"""
Language: {lang_}
Title: {title}
Source URL: {url}

Write a 2-3 sentence environmental summary.
Pick section: Air / Water / Climate / Disasters / Soil / Industry.
Return ONLY this format:
SECTION: ...
SUMMARY: ...
"""
    try:
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
        )
        text = (res.choices[0].message.content or "").strip()
        section = "Climate"
        summary = text[:280]
        if "SECTION:" in text:
            section = text.split("SECTION:")[1].splitlines()[0].strip() or "Climate"
        if "SUMMARY:" in text:
            summary = text.split("SUMMARY:")[1].strip()
        return (section, summary)
    except Exception:
        return ("Climate", f"{title}. {url}")

def refresh_archive_if_needed(lang_: str, hours: int = 6):
    last = meta_get(f"last_update_{lang_}")
    do_refresh = True
    if last:
        try:
            last_dt = dt.datetime.fromisoformat(last)
            do_refresh = (dt.datetime.utcnow() - last_dt) > dt.timedelta(hours=hours)
        except Exception:
            do_refresh = True

    if not do_refresh:
        return

    try:
        for source_name, rss in RSS_SOURCES:
            try:
                r = requests.get(rss, timeout=25)
                r.raise_for_status()
                items = simple_rss_extract(r.text, limit=3)
            except Exception:
                continue

            for title, url in items:
                if post_exists(url, lang_):
                    continue
                section, summary = ai_summarize(title, url, lang_)
                save_post(section, title, summary, source_name, url, lang_)

        meta_set(f"last_update_{lang_}", now_utc_iso())
    except Exception:
        # silent fail (no traceback)
        return

# ============================
# SIDEBAR
# ============================
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

    # Language selector (syncs to URL so it persists)
    chosen = st.selectbox(t("choose_lang"), ["uz", "ru", "en", "tr"], index=["uz","ru","en","tr"].index(lang))
    if chosen != lang:
        st.session_state.lang = chosen
        st.query_params["lang"] = chosen
        st.rerun()

    # silent archive refresh (wow: site "lives")
    refresh_archive_if_needed(lang_=st.session_state.lang, hours=6)

    st.divider()

    page = st.radio(t("choose_section"), [
        t("monitoring"),
        t("air"),
        t("water"),
        t("soil"),
        t("climate"),
        t("disasters"),
        t("ai_core"),
        t("silent"),
        t("industrial"),
        t("action"),
        t("map"),
    ])

    st.divider()
    st.info(f"{t('today')}: {dt.date.today()}")

# ============================
# TOP LIVE BANNER (WOW)
# ============================
st.markdown(f"""
<div class="live-banner">
⚠ LIVE GLOBAL ECO ALERT SYSTEM ACTIVE • Language: {st.session_state.lang.upper()}
</div>
""", unsafe_allow_html=True)

# ============================
# PAGES (no traceback; errors become clean messages)
# ============================
if page == t("monitoring"):
    hero("📟 GLOBAL ECO MONITORING",
         {"uz":"Monitoring manbalari va jonli xaritalar.",
          "en":"Monitoring sources and live maps.",
          "ru":"Источники мониторинга и живые карты.",
          "tr":"İzleme kaynakları ve canlı haritalar."}[lang],
         "MONITORING")

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.link_button("💨 IQAIR", "https://www.iqair.com/")
    with c2: st.link_button("🚀 NASA FIRMS", "https://firms.modaps.eosdis.nasa.gov/map/")
    with c3: st.link_button("🛰️ SENTINEL", "https://apps.sentinel-hub.com/eo-browser/")
    with c4: st.link_button("🌤️ Open-Meteo", "https://open-meteo.com/")

    st.components.v1.iframe(
        "https://earth.nullschool.net/#current/wind/surface/level/orthographic=-296.22,40.06,500",
        height=600
    )

elif page == t("air"):
    hero("💨 REAL-TIME AIR QUALITY",
         {"uz":"Open-Meteo orqali real vaqtga yaqin havo sifati.",
          "en":"Near real-time air quality via Open-Meteo.",
          "ru":"Почти реальное время качества воздуха (Open-Meteo).",
          "tr":"Open-Meteo ile gerçek zamana yakın hava kalitesi."}[lang],
         "AIR")

    city = st.text_input(t("city") + ":", "Tashkent")
    if st.button(t("update")):
        try:
            geo = geocode_city(city.strip())
            if not geo:
                st.warning({"uz":"Shahar topilmadi.", "en":"City not found.", "ru":"Город не найден.", "tr":"Şehir bulunamadı."}[lang])
            else:
                aq = air_quality(geo["lat"], geo["lon"])
                cur = aq.get("current", {})

                c1, c2, c3, c4 = st.columns(4)
                with c1: st.metric("PM2.5", f"{float(cur.get('pm2_5', 0)):.1f} µg/m³")
                with c2: st.metric("PM10", f"{float(cur.get('pm10', 0)):.1f} µg/m³")
                with c3: st.metric("NO₂", f"{float(cur.get('nitrogen_dioxide', 0)):.1f} µg/m³")
                with c4: st.metric("O₃", f"{float(cur.get('ozone', 0)):.1f} µg/m³")
                st.caption(f"📍 {geo['name']}, {geo.get('country','')}")
        except Exception:
            st.error(t("api_down"))

elif page == t("water"):
    hero("💧 WATER QUALITY",
         {"uz":"Suv sifati moduli skeleti (keyin real data/API bilan).",
          "en":"Water module skeleton (later connect real data/APIs).",
          "ru":"Скелет модуля воды (позже подключим данные/API).",
          "tr":"Su modülü iskeleti (sonra gerçek veri/API)."}[lang],
         "WATER")

    st.markdown("""
    <div class="soft-card accent-water">
      <b>Roadmap</b><br>
      • COD/BOD/TDS/pH risk modeli<br>
      • Sensor/dataset ulash<br>
      • AI tavsiyalar: tozalash texnologiyasi tanlash
    </div>
    """, unsafe_allow_html=True)

elif page == t("soil"):
    hero("🌱 SOIL MONITORING",
         {"uz":"Tuproq monitoring skeleti (keyin real data/API bilan).",
          "en":"Soil module skeleton (later connect real data/APIs).",
          "ru":"Скелет почвенного мониторинга (позже данные/API).",
          "tr":"Toprak izleme iskeleti (sonra gerçek veri/API)."}[lang],
         "SOIL")

    st.markdown("""
    <div class="soft-card accent-soil">
      <b>Roadmap</b><br>
      • Namlik/sho‘rlanish indikatorlari<br>
      • Og‘ir metal risk bahosi<br>
      • GIS qatlamlar (keyin)
    </div>
    """, unsafe_allow_html=True)

elif page == t("climate"):
    hero("🌍 CLIMATE CHANGE",
         {"uz":"Iqlim trendlar va indikatorlar (skelet).",
          "en":"Climate trends and indicators (skeleton).",
          "ru":"Климатические тренды и индикаторы (скелет).",
          "tr":"İklim trendleri ve göstergeler (iskelet)."}[lang],
         "CLIMATE")

    st.markdown("""
    <div class="soft-card accent-climate">
      <b>Roadmap</b><br>
      • Temperature trend (historical)<br>
      • Heatwave/coldwave risk<br>
      • CO₂ / energy context
    </div>
    """, unsafe_allow_html=True)

elif page == t("disasters"):
    hero("⚠️ DISASTERS & HAZARDS",
         {"uz":"Ofatlar: yong‘in, toshqin, chang bo‘roni (skelet).",
          "en":"Hazards: fires, floods, dust storms (skeleton).",
          "ru":"Риски: пожары, наводнения, пыльные бури (скелет).",
          "tr":"Riskler: yangın, sel, toz fırtınası (iskelet)."}[lang],
         "HAZARDS")

    st.markdown("""
    <div class="soft-card accent-disaster">
      <b>Roadmap</b><br>
      • NASA FIRMS wildfire overlay<br>
      • Flood alerts integration<br>
      • Risk map layer
    </div>
    """, unsafe_allow_html=True)

elif page == t("ai_core"):
    hero("🧠 AI CORE",
         {"uz":"Ekologik savollarga ilmiy va amaliy javob.",
          "en":"Scientific + practical environmental answers.",
          "ru":"Научные и практические ответы по экологии.",
          "tr":"Bilimsel ve pratik çevre cevapları."}[lang],
         "AI")

    if client is None:
        st.info(t("ai_missing"))
        st.stop()

    if "chat" not in st.session_state:
        st.session_state.chat = []

    for msg in st.session_state.chat:
        st.markdown(
            f"<div class='soft-card accent-ai'><b>{'🧑' if msg['role']=='user' else '🤖'}:</b><br>{msg['content']}</div>",
            unsafe_allow_html=True
        )

    q = st.text_input("Prompt:", placeholder={
        "uz":"Masalan: Toshkentda PM2.5 oshsa nima qilish kerak?",
        "en":"Example: What to do if PM2.5 spikes in my city?",
        "ru":"Пример: что делать при росте PM2.5?",
        "tr":"Örnek: PM2.5 artarsa ne yapmalı?"
    }[lang])

    if st.button(t("send")) and q.strip():
        st.session_state.chat.append({"role": "user", "content": q.strip()})
        try:
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": f"You are an environmental analyst. Reply in language: {lang}."},
                    *st.session_state.chat
                ],
            )
            ans = completion.choices[0].message.content
            st.session_state.chat.append({"role": "assistant", "content": ans})
            st.rerun()
        except Exception:
            st.error(t("api_down"))

elif page == t("silent"):
    hero("🤫 SILENT DISASTER + ARCHIVE",
         {"uz":"Arxiv avtomatik to‘lib boradi (Cron kerak emas).",
          "en":"Archive auto-fills (no Cron needed).",
          "ru":"Архив пополняется автоматически (Cron не нужен).",
          "tr":"Arşiv otomatik dolar (Cron gerekmez)."}[lang],
         "ARCHIVE")

    q = st.text_input(t("search"))
    try:
        rows = search_posts(q, lang_=lang) if q.strip() else get_latest_posts(25, lang_=lang)
    except Exception:
        rows = []

    if not rows:
        st.info(t("archive_empty"))
    else:
        for r in rows[:12]:
            st.markdown(
                f"<div class='soft-card accent-archive'><b>{r['title']}</b><br>"
                f"<span class='small-muted'>{r['created_at']} | {r['section']} | {r['source']}</span><br>"
                f"{r['summary']}<br><span class='small-muted'>{r['url']}</span></div>",
                unsafe_allow_html=True
            )

elif page == t("industrial"):
    hero("🏭 INDUSTRIAL ECO RISK SCORING",
         {"uz":"Sanoat obyektlari uchun tezkor risk baholash (demo).",
          "en":"Fast industrial environmental risk scoring (demo).",
          "ru":"Быстрая оценка промышленного эко-риска (демо).",
          "tr":"Hızlı endüstriyel çevre risk skoru (demo)."}[lang],
         "INDUSTRY")

    a1, a2, a3 = st.columns(3)
    with a1:
        industry = st.selectbox({"uz":"Sanoat turi","en":"Industry type","ru":"Тип отрасли","tr":"Sektör türü"}[lang],
                                ["Neft/gaz", "Kimyo", "Metallurgiya", "Tekstil", "Oziq-ovqat", "Energetika", "Boshqa"])
        production = st.slider({"uz":"Quvvat (1–10)","en":"Production (1–10)","ru":"Мощность (1–10)","tr":"Kapasite (1–10)"}[lang], 1, 10, 6)
        incidents = st.slider({"uz":"Incidentlar (yiliga)","en":"Incidents/year","ru":"Инциденты/год","tr":"Yıllık olay"}[lang], 0, 20, 1)
    with a2:
        air = st.slider({"uz":"Havo emissiya riski (1–10)","en":"Air emission risk (1–10)","ru":"Риск выбросов (1–10)","tr":"Hava emisyon riski (1–10)"}[lang], 1, 10, 6)
        water = st.slider({"uz":"Oqava suv riski (1–10)","en":"Wastewater risk (1–10)","ru":"Риск стоков (1–10)","tr":"Atıksu riski (1–10)"}[lang], 1, 10, 6)
        waste = st.slider({"uz":"Chiqindi riski (1–10)","en":"Waste risk (1–10)","ru":"Риск отходов (1–10)","tr":"Atık riski (1–10)"}[lang], 1, 10, 5)
    with a3:
        compliance = st.slider({"uz":"Compliance/ISO (1–10)","en":"Compliance/ISO (1–10)","ru":"Соответствие/ISO (1–10)","tr":"Uyum/ISO (1–10)"}[lang], 1, 10, 5)
        controls = st.slider({"uz":"Filtr/ETP nazorat (1–10)","en":"Controls (1–10)","ru":"Контроль (1–10)","tr":"Kontrol (1–10)"}[lang], 1, 10, 5)
        community = st.slider({"uz":"Aholiga yaqinlik (1–10)","en":"Near communities (1–10)","ru":"Близость к населению (1–10)","tr":"Yerleşime yakınlık (1–10)"}[lang], 1, 10, 6)

    base = {"Neft/gaz": 15, "Kimyo": 18, "Metallurgiya": 16, "Tekstil": 10, "Oziq-ovqat": 8, "Energetika": 14, "Boshqa": 12}[industry]
    risk = base + production*3 + incidents*2.5 + air*4 + water*4 + waste*3 + community*2 - compliance*3.5 - controls*3.5
    risk = clamp(risk, 0, 100)

    st.metric(t("risk"), int(round(risk)))
    st.progress(risk/100)
    st.markdown(f"<div class='soft-card accent-industrial'><b>{t('rating')}:</b> {risk_level(risk)}<br>"
                f"<span class='small-muted'>Demo model. Keyin real KPI va data bilan kalibrlanadi.</span></div>",
                unsafe_allow_html=True)

elif page == t("action"):
    hero("🧩 ECO ACTION PLAN (AI)",
         {"uz":"AI sizga amaliy 7/30 kunlik reja tuzadi.",
          "en":"AI generates a practical 7/30-day plan.",
          "ru":"AI составляет практический план на 7/30 дней.",
          "tr":"AI 7/30 günlük pratik plan üretir."}[lang],
         "PLAN")

    city = st.text_input({"uz":"Hudud/Shahar","en":"City/Region","ru":"Город/Регион","tr":"Şehir/Bölge"}[lang] + ":", "Tashkent")
    focus = st.selectbox({"uz":"Asosiy muammo","en":"Main focus","ru":"Основная проблема","tr":"Ana odak"}[lang],
                         ["Havo (PM2.5)", "Suv (COD/BOD)", "Chiqindi", "Iqlim/ESG", "Aralash"])
    budget = st.selectbox({"uz":"Budjet","en":"Budget","ru":"Бюджет","tr":"Bütçe"}[lang], ["Past", "O‘rta", "Yuqori"])
    goal = st.selectbox({"uz":"Maqsad","en":"Goal","ru":"Цель","tr":"Amaç"}[lang], ["Sog‘liq", "Compliance/ISO", "ESG hisobot", "Tezkor natija", "Uzoq muddat"])
    org = st.selectbox({"uz":"Tashkilot turi","en":"Organization type","ru":"Тип организации","tr":"Kurum türü"}[lang],
                       ["Aholi/individual", "Kichik biznes", "Sanoat korxonasi", "Universitet/Lab", "Davlat"])

    if st.button(t("plan")):
        fallback = f"""
**7-day quick plan**
1) Baseline audit for: {focus}
2) Measurement: pick sensors/APIs or sampling
3) Quick wins aligned with budget={budget}
4) KPIs: PM2.5 / COD / waste diversion
5) Risk hotspots for {city}

**30-day plan**
- Week 1: audit + KPI dashboard
- Week 2: technical controls rollout
- Week 3: monitoring + SOP
- Week 4: report + next month roadmap (goal={goal})
"""
        if client is None:
            st.markdown("<div class='soft-card accent-action'><b>AI unavailable.</b><br>Fallback plan:</div>", unsafe_allow_html=True)
            st.write(fallback)
        else:
            prompt = f"""
Reply language: {lang}
City/Region: {city}
Organization: {org}
Focus: {focus}
Budget: {budget}
Goal: {goal}

Create a 7-day and a 30-day actionable plan.
Include KPIs + measurement method for each KPI.
Be concise and practical.
"""
            try:
                res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": "You are an environmental consultant AI."},
                              {"role": "user", "content": prompt}],
                )
                st.markdown("<div class='soft-card accent-action'><b>AI Plan:</b></div>", unsafe_allow_html=True)
                st.write(res.choices[0].message.content)
            except Exception:
                st.markdown("<div class='soft-card accent-action'><b>AI error.</b><br>Fallback plan:</div>", unsafe_allow_html=True)
                st.write(fallback)

elif page == t("map"):
    hero("🌍 GLOBAL RISK MAP (WOW)",
         {"uz":"Global risk vizualizatsiya: Air + Industrial + Archive signals.",
          "en":"Global visualization: Air + Industrial + Archive signals.",
          "ru":"Глобальная визуализация: воздух + промышленность + архив.",
          "tr":"Küresel görselleştirme: hava + endüstri + arşiv."}[lang],
         "MAP")

    # mini "wow" counters (non-invasive)
    st.markdown("<div class='soft-card accent-map'><b>Live pulse:</b> "
                f"<span class='small-muted'>Auto-updating archive is running • Last refresh: {meta_get('last_update_'+lang) or '—'}</span></div>",
                unsafe_allow_html=True)

    # User can add a city point
    colA, colB = st.columns([1, 2])
    with colA:
        map_city = st.text_input({"uz":"Xaritaga shahar qo‘shish","en":"Add a city to the map","ru":"Добавить город","tr":"Haritaya şehir ekle"}[lang], "Tashkent")
        add_btn = st.button({"uz":"Shaharni qo‘shish","en":"Add city","ru":"Добавить","tr":"Ekle"}[lang])
        zoom = st.slider({"uz":"Zoom","en":"Zoom","ru":"Масштаб","tr":"Yakınlaştırma"}[lang], 2, 8, 3)

    # Default sample points (can grow)
    if "map_points" not in st.session_state:
        st.session_state.map_points = [
            {"name":"Tashkent", "lat":41.3, "lon":69.2, "risk":65},
            {"name":"Baku", "lat":40.4, "lon":49.8, "risk":72},
            {"name":"Delhi", "lat":28.6, "lon":77.2, "risk":88},
            {"name":"Istanbul", "lat":41.0, "lon":28.9, "risk":55},
            {"name":"New York", "lat":40.7, "lon":-74.0, "risk":48},
        ]

    if add_btn:
        try:
            geo = geocode_city(map_city.strip())
            if geo:
                # Try air quality quickly to influence risk
                risk_guess = 50
                try:
                    aq = air_quality(geo["lat"], geo["lon"])
                    cur = aq.get("current", {})
                    pm25 = float(cur.get("pm2_5", 0) or 0)
                    # simple mapping: pm2.5 -> risk
                    risk_guess = int(clamp(pm25 * 2.0, 10, 95))
                except Exception:
                    risk_guess = 50

                st.session_state.map_points.append({
                    "name": geo["name"],
                    "lat": geo["lat"],
                    "lon": geo["lon"],
                    "risk": risk_guess
                })
                st.success({"uz":"Qo‘shildi!", "en":"Added!", "ru":"Добавлено!", "tr":"Eklendi!"}[lang])
            else:
                st.warning({"uz":"Shahar topilmadi.", "en":"City not found.", "ru":"Город не найден.", "tr":"Şehir bulunamadı."}[lang])
        except Exception:
            st.error(t("api_down"))

    # Render map
    with colB:
        m = folium.Map(location=[25, 10], zoom_start=zoom, tiles="CartoDB dark_matter")

        for p in st.session_state.map_points:
            risk = int(p["risk"])
            if risk >= 75:
                color = "#ef4444"  # red
            elif risk >= 55:
                color = "#f59e0b"  # amber
            else:
                color = "#22c55e"  # green

            folium.CircleMarker(
                location=[p["lat"], p["lon"]],
                radius=10,
                popup=f"{p['name']}<br>Risk: {risk}",
                color=color,
                fill=True,
                fill_opacity=0.75
            ).add_to(m)

        st_folium(m, height=600, use_container_width=True)

# ============================
# FOOTER
# ============================
st.markdown("""
<div style='text-align:center; border-top: 1px solid #1C1F26; padding: 18px; color:#7b8794;'>
© 2026 ECO AI WORLD | Egamberdiev Research Group
</div>
""", unsafe_allow_html=True)
