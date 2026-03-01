import streamlit as st
import datetime
import os
from groq import Groq
import requests

# =========================================================
# 1) GOOGLE SEARCH CONSOLE VERIFICATION
# =========================================================
GOOGLE_TAG = """<meta name="google-site-verification" content="ZkAtTf6Ut4FM76-c3qns2vqHjD4OZLKIxw_i2iw7bTY" />"""

# =========================================================
# 2) PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="ECO AI WORLD | Enterprise",
    page_icon="🧬",
    layout="wide"
)
st.markdown(GOOGLE_TAG, unsafe_allow_html=True)

# =========================================================
# 3) GROQ CLIENT (ENV ONLY) — NO ERROR TEXT
# =========================================================
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

# =========================================================
# 4) UI THEME
# =========================================================
st.markdown("""
<style>
.stApp { background-color: #0E1116; color: #A0A0A0; }
[data-testid="stSidebar"] { background-color: #050505 !important; border-right: 1px solid #1C1F26; }

.author-box { padding: 15px; background: rgba(28, 31, 38, 0.8); border-radius: 8px; border-left: 3px solid #FFD400; margin-bottom: 20px; }
.author-title { color: #FFD400; font-size: 11px; font-weight: bold; margin: 0; }
.author-name { color: #FFFFFF; font-size: 13px; margin-bottom: 8px; }

.main-card { background: #1C1F26; padding: 18px; border-radius: 10px; border-left: 4px solid #FF3B3B; margin-bottom: 14px; }
.soft-card { background: #141821; padding: 16px; border-radius: 10px; border: 1px solid #1C1F26; margin-bottom: 14px; }

h1, h2, h3 { color: #FFFFFF !important; font-family: 'Inter', sans-serif; }
.small-muted { color: #808080; font-size: 12px; }

.danger-text { color: #FF3B3B; font-weight: bold; animation: pulse 2s infinite; }
@keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }
</style>
""", unsafe_allow_html=True)

# =========================================================
# HELPERS
# =========================================================
def clamp(x: float, lo: float = 0, hi: float = 100) -> float:
    return max(lo, min(hi, x))

def risk_level(score: float) -> str:
    if score >= 80: return "Juda yuqori"
    if score >= 60: return "Yuqori"
    if score >= 40: return "O‘rtacha"
    if score >= 20: return "Past"
    return "Juda past"

def aqi_category(aqi: float) -> str:
    if aqi <= 50: return "Good"
    if aqi <= 100: return "Moderate"
    if aqi <= 150: return "Unhealthy (Sensitive)"
    if aqi <= 200: return "Unhealthy"
    if aqi <= 300: return "Very Unhealthy"
    return "Hazardous"

def pm25_to_us_aqi(pm25: float) -> int:
    # US EPA breakpoint method (µg/m³), simplified piecewise.
    bp = [
        (0.0, 12.0, 0, 50),
        (12.1, 35.4, 51, 100),
        (35.5, 55.4, 101, 150),
        (55.5, 150.4, 151, 200),
        (150.5, 250.4, 201, 300),
        (250.5, 350.4, 301, 400),
        (350.5, 500.4, 401, 500),
    ]
    for c_lo, c_hi, i_lo, i_hi in bp:
        if c_lo <= pm25 <= c_hi:
            aqi = (i_hi - i_lo) / (c_hi - c_lo) * (pm25 - c_lo) + i_lo
            return int(round(aqi))
    if pm25 < 0:
        return 0
    return 500

# =========================================================
# REAL-TIME AIR (OpenAQ) — key required emas
# =========================================================
@st.cache_data(ttl=300)
def openaq_latest(city: str, country: str | None = None) -> dict:
    # OpenAQ API ba'zan o'zgaradi; xato bo'lsa sahifa yiqilmaydi
    url = "https://api.openaq.org/v3/latest"
    params = {"limit": 100}
    if city:
        params["city"] = city
    if country:
        params["country"] = country

    r = requests.get(url, params=params, timeout=20)
    r.raise_for_status()
    return r.json()

def extract_pollutants(openaq_json: dict) -> dict:
    out = {}
    results = openaq_json.get("results") or openaq_json.get("data") or []
    for item in results:
        measurements = item.get("measurements") or item.get("parameters") or []
        for m in measurements:
            name = (m.get("parameter") or m.get("name") or "").lower()
            value = m.get("value")
            unit = m.get("unit")
            if value is None:
                continue

            if name in ["pm2.5", "pm25", "pm_2_5"]:
                out["pm25"] = (float(value), unit)
            elif name in ["pm10", "pm_10"]:
                out["pm10"] = (float(value), unit)
            elif name == "no2":
                out["no2"] = (float(value), unit)
            elif name == "so2":
                out["so2"] = (float(value), unit)
            elif name == "o3":
                out["o3"] = (float(value), unit)
            elif name == "co":
                out["co"] = (float(value), unit)
    return out

# =========================================================
# SIDEBAR NAVIGATION
# =========================================================
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
    page = st.radio("BO'LIMNI TANLANG:", [
        "1. Monitoring Terminal (Asosiy)",
        "2. Real-Time Air Quality (API)",
        "3. Water Quality (Suv sifati)",
        "4. Industrial Eco Risk Scoring (Sanoat)",
        "5. Disasters & Hazards (Ofatlar)",
        "6. 🧠 AI CORE (Llama 3.3)",
        "7. YOUR BODY vs ENV. (Xavf)",
        "8. SILENT DISASTER (Haqiqat)"
    ])
    st.divider()
    st.info(f"Bugun: {datetime.date.today()}")

# =========================================================
# PAGE 1
# =========================================================
if page == "1. Monitoring Terminal (Asosiy)":
    st.title("📟 GLOBAL ECO MONITORING")
    st.markdown("<div class='main-card'>Global monitoring manbalari va jonli xaritalar.</div>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1: st.link_button("💨 IQAIR", "https://www.iqair.com/")
    with col2: st.link_button("🚀 NASA FIRMS", "https://firms.modaps.eosdis.nasa.gov/map/")
    with col3: st.link_button("🛰️ SENTINEL", "https://apps.sentinel-hub.com/eo-browser/")
    with col4: st.link_button("🌍 OpenAQ", "https://openaq.org/")

    st.components.v1.iframe(
        "https://earth.nullschool.net/#current/wind/surface/level/orthographic=-296.22,40.06,500",
        height=600
    )

# =========================================================
# PAGE 2 — REAL TIME AIR (API)
# =========================================================
elif page == "2. Real-Time Air Quality (API)":
    st.title("💨 REAL-TIME AIR QUALITY (API)")
    st.markdown("<div class='main-card'>OpenAQ orqali real vaqtga yaqin havo sifati. PM2.5 asosida AQI hisoblanadi.</div>", unsafe_allow_html=True)

    c1, c2 = st.columns([1, 1])
    with c1:
        city = st.text_input("Shahar (inglizcha):", value="Tashkent")
        country = st.text_input("Country code (ixtiyoriy, masalan UZ):", value="UZ")
        st.caption("Agar topilmasa: city nomini boshqacha yozing yoki country ni bo‘sh qoldiring.")

    with c2:
        st.markdown("<div class='soft-card'><b>Live natija</b><div class='small-muted'>API cheklansa ham sahifa yiqilmaydi.</div></div>", unsafe_allow_html=True)

    if st.button("Yangilash"):
        try:
            data = openaq_latest(city=city.strip(), country=(country.strip() or None))
            pol = extract_pollutants(data)

            pm25 = pol.get("pm25")
            pm10 = pol.get("pm10")

            if not pm25 and not pm10:
                st.warning("Hozircha bu shahar uchun OpenAQ o‘lchov topilmadi. City nomini o‘zgartirib ko‘ring.")
            else:
                if pm25:
                    pm25_val, pm25_unit = pm25
                    aqi = pm25_to_us_aqi(pm25_val)

                    a, b, c = st.columns(3)
                    with a: st.metric("PM2.5", f"{pm25_val:.1f} {pm25_unit}")
                    with b: st.metric("AQI (PM2.5)", aqi)
                    with c: st.metric("Category", aqi_category(aqi))
                    st.progress(clamp(aqi, 0, 500) / 500)

                if pm10:
                    pm10_val, pm10_unit = pm10
                    st.write(f"**PM10:** {pm10_val:.1f} {pm10_unit}")

                extra = {k: v for k, v in pol.items() if k not in ["pm25", "pm10"]}
                if extra:
                    st.markdown("### Qo‘shimcha pollutantlar")
                    for k, (v, u) in extra.items():
                        st.write(f"• **{k.upper()}**: {v:.2f} {u}")

        except Exception as e:
            st.error(f"API xatosi: {e}")

# =========================================================
# PAGE 3 — WATER QUALITY (dashboard)
# =========================================================
elif page == "3. Water Quality (Suv sifati)":
    st.title("💧 WATER QUALITY DASHBOARD")
    st.markdown("<div class='main-card'>Suv parametrlari bo‘yicha tezkor indeks (demo), tavsiyalar bilan.</div>", unsafe_allow_html=True)

    left, right = st.columns(2)
    with left:
        ph = st.slider("pH", 0.0, 14.0, 7.2, 0.1)
        tds = st.slider("TDS (mg/L)", 0, 3000, 450, 10)
        turb = st.slider("Turbidity (NTU)", 0.0, 50.0, 2.0, 0.1)
        coliform = st.selectbox("Koliform (taxmin)", ["Yo‘q/ma’lum emas", "Past", "O‘rtacha", "Yuqori"])

    score = 0
    # pH
    score += 25 if 6.5 <= ph <= 8.5 else (15 if 6.0 <= ph <= 9.0 else 5)
    # TDS
    score += 25 if tds <= 500 else (18 if tds <= 1000 else (10 if tds <= 2000 else 5))
    # Turb
    score += 25 if turb <= 1 else (18 if turb <= 5 else (10 if turb <= 10 else 5))
    # Coliform
    score += 20 if coliform == "Yo‘q/ma’lum emas" else (15 if coliform == "Past" else (8 if coliform == "O‘rtacha" else 2))
    score = int(clamp(score))

    with right:
        st.metric("Water Quality Score (0–100)", score)
        st.write(f"Xavf bahosi: **{risk_level(100 - score)}**")
        st.progress(score / 100)

        st.markdown("### Tavsiyalar")
        tips = []
        if not (6.5 <= ph <= 8.5): tips.append("pH normadan chiqdi — neytrallash/kuzatuv.")
        if tds > 1000: tips.append("TDS yuqori — membrana/ion-almashinuv.")
        if turb > 5: tips.append("Loyqalilik yuqori — koagulyatsiya + filtrlash.")
        if coliform in ["O‘rtacha", "Yuqori"]: tips.append("Mikrobiologik xavf — UV/xlor dezinfeksiya.")
        if not tips: tips = ["Ko‘rsatkichlar yaxshi — monitoringni davom ettiring."]
        for t in tips: st.write("•", t)

# =========================================================
# PAGE 4 — INDUSTRIAL ECO RISK SCORING
# =========================================================
elif page == "4. Industrial Eco Risk Scoring (Sanoat)":
    st.title("🏭 INDUSTRIAL ECO RISK SCORING")
    st.markdown("<div class='main-card'>Sanoat obyektlari uchun ekologik risk balli: emissiya + oqava + chiqindi + compliance.</div>", unsafe_allow_html=True)

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
    risk = 0
    risk += base
    risk += production * 3.0
    risk += incidents * 2.5
    risk += air * 4.0
    risk += water * 4.0
    risk += waste * 3.0
    risk += community * 2.0
    risk -= compliance * 3.5
    risk -= controls * 3.5
    risk = clamp(risk, 0, 100)

    c1, c2, c3 = st.columns(3)
    with c1: st.metric("Industrial Eco Risk (0–100)", int(round(risk)))
    with c2: st.metric("Risk level", risk_level(risk))
    with c3: st.metric("Action", "Audit" if risk >= 60 else ("Improve monitoring" if risk >= 40 else "Maintain"))

    st.progress(risk / 100)

    st.markdown("### Tavsiyalar")
    rec = []
    if air >= 7: rec.append("Havo emissiyasi: scrubber/ESP/filtr audit + CEMS stack monitoring.")
    if water >= 7: rec.append("Oqava suv: ETP optimizatsiya (pH, koagulyatsiya, sorbent/membrana).")
    if waste >= 7: rec.append("Chiqindi: segregatsiya, xavfli chiqindi protokoli, qayta ishlash.")
    if compliance <= 4: rec.append("Compliance: ISO 14001 + ichki audit jadvali.")
    if controls <= 4: rec.append("Nazorat: servis rejasi, SOP, operator trening.")
    if incidents >= 3: rec.append("Incident: HAZOP/LOPA, emergency plan, near-miss reporting.")
    if not rec: rec = ["Monitoringni davom ettiring va KPI’ni oyma-oy yuriting."]
    for r in rec: st.write("•", r)

# =========================================================
# PAGE 5 — DISASTERS & HAZARDS
# =========================================================
elif page == "5. Disasters & Hazards (Ofatlar)":
    st.title("⚠️ DISASTERS & HAZARDS")
    st.markdown("<div class='main-card'>Xavf baholash (demo): zilzila, toshqin, yong‘in, sanoat avariyasi.</div>", unsafe_allow_html=True)

    hazard_type = st.selectbox("Xavf turi", ["Zilzila", "Toshqin", "O‘rmon yong‘ini", "Sanoat avariyasi"])
    pop_density = st.slider("Aholi zichligi (1–10)", 1, 10, 6)
    infra = st.slider("Infratuzilma tayyorgarligi (1–10)", 1, 10, 5)
    response = st.slider("Tezkor javob (1–10)", 1, 10, 5)

    base = {"Zilzila": 70, "Toshqin": 55, "O‘rmon yong‘ini": 45, "Sanoat avariyasi": 50}[hazard_type]
    hz = clamp(base + pop_density * 3 - infra * 2 - response * 2, 0, 100)

    st.metric("Hazard Score (0–100)", int(round(hz)))
    st.write(f"Baholash: **{risk_level(hz)}**")
    st.progress(hz / 100)

# =========================================================
# PAGE 6 — AI CORE (NO KEY ERROR TEXT)
# =========================================================
elif page == "6. 🧠 AI CORE (Llama 3.3)":
    st.title("🧠 AI CORE: Llama 3.3")

    if client is None:
        st.markdown(
            "<div class='soft-card'><b>AI vaqtincha o‘chiq</b>"
            "<div class='small-muted'>Serverda GROQ_API_KEY sozlangan bo‘lsa avtomatik ishlaydi.</div></div>",
            unsafe_allow_html=True
        )
        st.stop()

    if "chat" not in st.session_state:
        st.session_state.chat = []

    for msg in st.session_state.chat:
        if msg["role"] == "user":
            st.markdown(f"<div class='soft-card'><b>🧑 Siz:</b><br>{msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='soft-card' style='border-left:3px solid #FFD400;'><b>🤖 AI:</b><br>{msg['content']}</div>", unsafe_allow_html=True)

    q = st.text_input("Savol:", placeholder="Masalan: sanoat oqava suvini qanday optimallashtiramiz?")
    colA, colB = st.columns([1, 1])
    run = colA.button("Yuborish")
    clear = colB.button("Chatni tozalash")

    if clear:
        st.session_state.chat = []
        st.rerun()

    if run and q.strip():
        st.session_state.chat.append({"role": "user", "content": q.strip()})
        with st.spinner("AI tahlil qilmoqda..."):
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "Sen ekolog-analitik AI'san. Javobni ilmiy, aniq, amaliy tarzda ber."},
                    *st.session_state.chat
                ],
            )
            ans = completion.choices[0].message.content
            st.session_state.chat.append({"role": "assistant", "content": ans})
            st.rerun()

# =========================================================
# PAGE 7
# =========================================================
elif page == "7. YOUR BODY vs ENV. (Xavf)":
    st.title("🫀 YOUR BODY vs ENVIRONMENT")
    st.markdown("<div class='main-card'>Shaxsiy risk baholash (demo).</div>", unsafe_allow_html=True)

    age = st.slider("Yosh", 1, 100, 25)
    aqi = st.slider("AQI (taxminiy)", 0, 400, 120)
    smoker = st.selectbox("Chekish", ["Yo‘q", "Ha"])

    load = 10 + age * 0.3 + aqi * 0.15 + (15 if smoker == "Ha" else 0)
    load = clamp(load, 0, 100)

    st.metric("Ecological Body Load (0–100)", int(round(load)))
    st.write(f"Baholash: **{risk_level(load)}**")
    st.progress(load / 100)

# =========================================================
# PAGE 8
# =========================================================
elif page == "8. SILENT DISASTER (Haqiqat)":
    st.title("🤫 THE SILENT DISASTER")
    st.image("https://images.unsplash.com/photo-1500382017468-9049fed747ef", use_container_width=True)
    st.markdown('<p class="danger-text">OGOHLANTIRISH: Hamma narsa ko\'ringanidan ko\'ra dahshatliroq.</p>', unsafe_allow_html=True)

# =========================================================
# FOOTER
# =========================================================
st.markdown("""
<div style='text-align: center; border-top: 1px solid #1C1F26; padding: 18px;'>
© 2026 ECO AI WORLD | Egamberdiev Research Group
</div>
""", unsafe_allow_html=True)
