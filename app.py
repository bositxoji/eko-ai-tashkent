import streamlit as st
import datetime
import os
from groq import Groq

# ==============================
# 1) GOOGLE VERIFICATION
# ==============================
GOOGLE_TAG = """<meta name="google-site-verification" content="ZkAtTf6Ut4FM76-c3qns2vqHjD4OZLKIxw_i2iw7bTY" />"""

# ==============================
# 2) PAGE CONFIG
# ==============================
st.set_page_config(
    page_title="ECO AI WORLD | Enterprise",
    page_icon="🧬",
    layout="wide"
)

# Google tag inject
st.markdown(GOOGLE_TAG, unsafe_allow_html=True)

# ==============================
# 3) SAFE API KEY LOADER
# ==============================
def get_groq_key() -> str | None:
    # 1) Server ENV (Render)
    k = os.getenv("GROQ_API_KEY")
    if k and k.strip():
        return k.strip()

    # 2) Local secrets.toml (optional)
    try:
        k2 = st.secrets.get("GROQ_API_KEY")
        if k2 and str(k2).strip():
            return str(k2).strip()
    except Exception:
        pass

    return None


GROQ_API_KEY = get_groq_key()
if not GROQ_API_KEY:
    st.error(
        "❌ GROQ_API_KEY topilmadi.\n\n"
        "✅ Render: Environment -> Add Variable -> GROQ_API_KEY\n"
        "✅ Local: .streamlit/secrets.toml ichiga GROQ_API_KEY yozing\n\n"
        "Key bo‘lmasa AI CORE ishlamaydi, qolgan bo‘limlar ishlaydi."
    )
    client = None
else:
    client = Groq(api_key=GROQ_API_KEY)

# ==============================
# 4) THEME / STYLE
# ==============================
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

hr { border: none; border-top: 1px solid #1C1F26; }
</style>
""", unsafe_allow_html=True)

# ==============================
# 5) HELPERS
# ==============================
def risk_level(score: int) -> str:
    if score >= 80:
        return "Juda yuqori"
    if score >= 60:
        return "Yuqori"
    if score >= 40:
        return "O‘rtacha"
    if score >= 20:
        return "Past"
    return "Juda past"


def clamp(x: int, lo: int = 0, hi: int = 100) -> int:
    return max(lo, min(hi, x))

# ==============================
# 6) SIDEBAR NAV
# ==============================
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

# ==============================
# 7) PAGES
# ==============================
if page == "1. Monitoring Terminal (Asosiy)":
    st.title("📟 GLOBAL ECO MONITORING")
    st.markdown("<div class='main-card'>Global monitoring manbalari va jonli xaritalar.</div>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1: st.link_button("💨 IQAIR", "https://www.iqair.com/")
    with col2: st.link_button("🚀 NASA FIRMS", "https://firms.modaps.eosdis.nasa.gov/map/")
    with col3: st.link_button("🧠 Groq (Models)", "https://console.groq.com/")
    with col4: st.link_button("🛰️ SENTINEL", "https://apps.sentinel-hub.com/eo-browser/")

    st.markdown("<div class='soft-card'><b>Earth Wind Map</b><div class='small-muted'>Shamol, oqimlar va atmosfera dinamikasi</div></div>", unsafe_allow_html=True)
    st.components.v1.iframe(
        "https://earth.nullschool.net/#current/wind/surface/level/orthographic=-296.22,40.06,500",
        height=600
    )

elif page == "2. Water Quality (Suv sifati)":
    st.title("💧 WATER QUALITY DASHBOARD")
    st.markdown("<div class='main-card'>Suv parametrlari bo‘yicha tezkor baholash va indeks hisoblash.</div>", unsafe_allow_html=True)

    left, right = st.columns([1, 1])

    with left:
        st.markdown("<div class='soft-card'><b>Parametrlarni kiriting</b></div>", unsafe_allow_html=True)
        ph = st.slider("pH", 0.0, 14.0, 7.2, 0.1)
        tds = st.slider("TDS (mg/L)", 0, 3000, 450, 10)
        turb = st.slider("Turbidity NTU", 0.0, 50.0, 2.0, 0.1)
        temp = st.slider("Harorat (°C)", 0.0, 40.0, 18.0, 0.5)
        coliform = st.selectbox("Koliform (taxminiy holat)", ["Yo‘q/ma’lum emas", "Past", "O‘rtacha", "Yuqori"])

    # Simple heuristic score (demo dashboard)
    score = 0
    # pH ideal ~6.5-8.5
    if 6.5 <= ph <= 8.5: score += 25
    elif 6.0 <= ph <= 9.0: score += 15
    else: score += 5

    # TDS
    if tds <= 500: score += 25
    elif tds <= 1000: score += 18
    elif tds <= 2000: score += 10
    else: score += 5

    # turbidity
    if turb <= 1: score += 25
    elif turb <= 5: score += 18
    elif turb <= 10: score += 10
    else: score += 5

    # coliform penalty
    if coliform == "Yo‘q/ma’lum emas": score += 20
    elif coliform == "Past": score += 15
    elif coliform == "O‘rtacha": score += 8
    else: score += 2

    score = clamp(score)

    with right:
        st.markdown("<div class='soft-card'><b>Natija</b></div>", unsafe_allow_html=True)
        st.metric("Water Quality Score (0–100)", score)
        st.write(f"Baholash: **{risk_level(100 - score)} xavf**")
        st.progress(score / 100)

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("**Tavsiyalar (qisqa):**")
        tips = []
        if not (6.5 <= ph <= 8.5):
            tips.append("pH normadan chiqdi — neytrallash/korreksiya kerak.")
        if tds > 1000:
            tips.append("TDS yuqori — membrana/ion-almashinuv tavsiya.")
        if turb > 5:
            tips.append("Loyqalilik yuqori — koagulyatsiya + filtrlash.")
        if coliform in ["O‘rtacha", "Yuqori"]:
            tips.append("Mikrobiologik xavf ehtimoli — dezinfeksiya (UV/xlor) kerak.")
        if not tips:
            tips = ["Ko‘rsatkichlar yaxshi — monitoringni davom ettiring."]
        for t in tips:
            st.write("•", t)

        st.markdown("<div class='small-muted'>Eslatma: bu dashboard tezkor (heuristic) baholash. Laboratoriya tahlili bilan tasdiqlang.</div>", unsafe_allow_html=True)

elif page == "3. Soil Monitoring (Tuproq)":
    st.title("🌱 SOIL MONITORING DASHBOARD")
    st.markdown("<div class='main-card'>Tuproq parametrlari bo‘yicha indeks va agro-eko tavsiyalar.</div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        soil_ph = st.slider("Tuproq pH", 3.0, 10.0, 6.8, 0.1)
        moisture = st.slider("Namlik (%)", 0, 100, 35, 1)
    with c2:
        ec = st.slider("EC (dS/m) – sho‘rlanish", 0.0, 10.0, 1.2, 0.1)
        om = st.slider("Organik modda (%)", 0.0, 15.0, 2.5, 0.1)
    with c3:
        nitrate = st.slider("Nitrat (mg/kg)", 0, 300, 45, 1)
        heavy = st.selectbox("Og‘ir metall risk (taxmin)", ["Past", "O‘rtacha", "Yuqori"])

    # Simple soil health score (demo)
    s = 0
    if 6.0 <= soil_ph <= 7.5: s += 25
    elif 5.5 <= soil_ph <= 8.0: s += 18
    else: s += 10

    if 20 <= moisture <= 60: s += 20
    else: s += 12

    if ec <= 2: s += 20
    elif ec <= 4: s += 12
    else: s += 6

    if om >= 3: s += 20
    elif om >= 1.5: s += 14
    else: s += 8

    if nitrate <= 50: s += 15
    elif nitrate <= 120: s += 10
    else: s += 6

    if heavy == "Past": s += 10
    elif heavy == "O‘rtacha": s += 5
    else: s += 1

    s = clamp(s)

    st.metric("Soil Health Score (0–100)", s)
    st.progress(s / 100)

    st.markdown("### Tavsiyalar")
    rec = []
    if soil_ph < 6.0:
        rec.append("pH past — ohaklash (CaCO₃) haqida o‘ylang.")
    if soil_ph > 7.8:
        rec.append("pH yuqori — organik modda, gipss (sho‘rlanish bo‘lsa) ko‘rib chiqing.")
    if ec > 4:
        rec.append("Sho‘rlanish yuqori — yuvish sug‘orishi + drenaj rejasi.")
    if om < 2:
        rec.append("Organik modda past — kompost/biochar/organik o‘g‘it.")
    if heavy == "Yuqori":
        rec.append("Og‘ir metall riski — fitoremediatsiya yoki sorbent (biochar/zeolit) ishlatish.")
    if not rec:
        rec = ["Ko‘rsatkichlar yaxshi — mavsumiy monitoring davom ettiring."]

    for r in rec:
        st.write("•", r)

elif page == "4. Climate Change (Iqlim)":
    st.title("🌍 CLIMATE CHANGE DASHBOARD")
    st.markdown("<div class='main-card'>Iqlim xavfi bo‘yicha ssenariy va ta’sir indikatorlari (interaktiv).</div>", unsafe_allow_html=True)

    st.markdown("<div class='soft-card'><b>Hudud ssenariysi</b><div class='small-muted'>Bu bo‘lim real API emas, interaktiv model-senariy.</div></div>", unsafe_allow_html=True)
    region = st.selectbox("Hudud", ["Toshkent", "Samarqand", "Farg‘ona", "Buxoro", "Qoraqalpog‘iston", "Boshqa"])
    warming = st.slider("Harorat oshishi ssenariysi (°C)", 0.0, 4.0, 1.5, 0.1)
    rainfall = st.slider("Yog‘in o‘zgarishi (%)", -40, 40, -5, 1)
    heatwaves = st.slider("Issiq to‘lqinlar chastotasi (1–10)", 1, 10, 6)

    # Heuristic climate risk
    cr = 20
    cr += int(warming * 15)
    cr += int(abs(rainfall) * 0.5)
    cr += int(heatwaves * 4)
    cr = clamp(cr)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Climate Risk Index", cr)
    with c2:
        st.metric("Issiq stress", clamp(int(warming * 25 + heatwaves * 5)))
    with c3:
        st.metric("Suv stress", clamp(int(((-rainfall) if rainfall < 0 else 0) * 1.2 + warming * 10)))

    st.progress(cr / 100)
    st.write(f"**{region}** uchun umumiy baholash: **{risk_level(cr)}**")

    st.markdown("### Adaptatsiya tavsiyalari")
    adv = []
    if warming >= 2:
        adv.append("Shahar issiq oroli: ko‘kalamzor, soyali yo‘laklar, cool-roof.")
    if rainfall < -10:
        adv.append("Suv tejamkor irrigatsiya, qayta foydalanish, yomg‘ir suvi yig‘ish.")
    if heatwaves >= 7:
        adv.append("Issiq to‘lqin protokoli: ogohlantirish, dam olish nuqtalari, tibbiy tavsiya.")
    if not adv:
        adv.append("Monitoring + energiya samaradorligi + yashil infratuzilma.")

    for a in adv:
        st.write("•", a)

elif page == "5. Disasters & Hazards (Ofatlar)":
    st.title("⚠️ DISASTERS & HAZARDS")
    st.markdown("<div class='main-card'>Xavf baholash: zilzila, toshqin, yong‘in, sanoat xavfi (interaktiv).</div>", unsafe_allow_html=True)

    a1, a2 = st.columns([1, 1])

    with a1:
        hazard_type = st.selectbox("Xavf turi", ["Zilzila", "Toshqin", "O‘rmon yong‘ini", "Sanoat avariyasi"])
        pop_density = st.slider("Aholi zichligi (1–10)", 1, 10, 6)
        infra = st.slider("Infratuzilma tayyorgarligi (1–10)", 1, 10, 5)
        response = st.slider("Tezkor javob (1–10)", 1, 10, 5)

    base = {"Zilzila": 70, "Toshqin": 55, "O‘rmon yong‘ini": 45, "Sanoat avariyasi": 50}[hazard_type]
    hz = base + pop_density * 3 - infra * 2 - response * 2
    hz = clamp(int(hz))

    with a2:
        st.metric("Hazard Score (0–100)", hz)
        st.write(f"Baholash: **{risk_level(hz)}**")
        st.progress(hz / 100)

        st.markdown("### Tezkor checklist")
        checklist = []
        if hazard_type == "Zilzila":
            checklist = ["Evakuatsiya yo‘laklari", "Gaz/elektr o‘chirish rejasi", "Zaxira suv va aptechka", "Binoni tekshirtirish"]
        elif hazard_type == "Toshqin":
            checklist = ["Drenaj va ariqchalarni tozalash", "Muhim hujjatlar suvdan himoya", "Yuqori joyga chiqish rejasi", "Elektr xavfsizligi"]
        elif hazard_type == "O‘rmon yong‘ini":
            checklist = ["Yonuvchi chiqindini tozalash", "Aloqa/ogohlantirish", "Evakuatsiya", "Niqob/suv zaxirasi"]
        else:
            checklist = ["Kimyoviy xavf protokoli", "PPE", "Avariya aloqa zanjiri", "Hudud izolatsiyasi"]

        for c in checklist:
            st.write("•", c)

    st.markdown("<div class='small-muted'>Eslatma: real-time ofat monitoring uchun (USGS/NOAA/NASA FIRMS) API yoki iframe ishlatish mumkin.</div>", unsafe_allow_html=True)

elif page == "6. 🧠 AI CORE (Llama 3.3)":
    st.title("🧠 AI CORE: Llama 3.3 Intelligence")
    st.markdown("<div class='main-card'>Savolingizga ilmiy va aniq javob oling.</div>", unsafe_allow_html=True)

    if client is None:
        st.warning("AI CORE ishlashi uchun GROQ_API_KEY kerak. Render Environment ga qo‘ying.")
        st.stop()

    # chat history
    if "chat" not in st.session_state:
        st.session_state.chat = []

    with st.container():
        for msg in st.session_state.chat:
            role = msg["role"]
            content = msg["content"]
            if role == "user":
                st.markdown(f"<div class='soft-card'><b>🧑 Siz:</b><br>{content}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='soft-card' style='border-left:3px solid #FFD400;'><b>🤖 AI:</b><br>{content}</div>", unsafe_allow_html=True)

    user_query = st.text_input("Ekologik muammo haqida so'rang:", placeholder="Masalan: neftli oqova suvni arzon tozalash yo‘li?")

    colA, colB = st.columns([1, 1])
    with colA:
        run = st.button("Tahlilni boshlash")
    with colB:
        clear = st.button("Chatni tozalash")

    if clear:
        st.session_state.chat = []
        st.rerun()

    if run:
        q = user_query.strip()
        if not q:
            st.warning("Savol yozing.")
        else:
            st.session_state.chat.append({"role": "user", "content": q})
            with st.spinner("AI tahlil qilmoqda..."):
                try:
                    completion = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {
                                "role": "system",
                                "content": (
                                    "Sen ekolog-analitik AI'san. "
                                    "Javobni: (1) qisqa xulosa, (2) ilmiy izoh, (3) amaliy tavsiya, (4) xavf va cheklovlar "
                                    "tuzilmasida ber. Keraksiz gap yozma."
                                )
                            },
                            *st.session_state.chat
                        ],
                    )
                    ans = completion.choices[0].message.content
                    st.session_state.chat.append({"role": "assistant", "content": ans})
                    st.rerun()
                except Exception as e:
                    st.error(f"Xatolik: {e}")

elif page == "7. YOUR BODY vs ENV. (Xavf)":
    st.title("🫀 YOUR BODY vs ENVIRONMENT")
    st.markdown("<div class='main-card'>Shaxsiy risk baholash (demo model) – sog‘liq uchun ekologik yuklama.</div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        age = st.slider("Yosh", 1, 100, 25)
        smoker = st.selectbox("Chekish", ["Yo‘q", "Ha"])
    with c2:
        aqi = st.slider("Hudud AQI (taxminiy)", 0, 400, 120)
        indoor = st.slider("Uy ichida shamollatish (1–10)", 1, 10, 5)
    with c3:
        work = st.selectbox("Ish muhiti", ["Ofis", "Zavod/sanoat", "Ko‘cha/transport", "Laboratoriya"])
        mask = st.selectbox("Niqob odati", ["Yo‘q", "Ba’zan", "Doim"])

    # heuristic body load
    load = 10
    load += int(age * 0.3)
    load += int(aqi * 0.15)
    if smoker == "Ha":
        load += 15
    if work == "Zavod/sanoat":
        load += 12
    elif work == "Ko‘cha/transport":
        load += 10
    elif work == "Laboratoriya":
        load += 6

    load -= int(indoor * 1.5)
    if mask == "Ba’zan":
        load -= 6
    elif mask == "Doim":
        load -= 12

    load = clamp(int(load))

    st.metric("Ecological Body Load (0–100)", load)
    st.write(f"Baholash: **{risk_level(load)}**")
    st.progress(load / 100)

    st.markdown("### Shaxsiy tavsiyalar")
    adv = []
    if aqi > 150:
        adv.append("AQI yuqori: ko‘chada faol sportni kamaytiring, ichki havo filtri (HEPA) ko‘rib chiqing.")
    if smoker == "Ha":
        adv.append("Chekish riskni keskin oshiradi — kamaytirish/ tashlash eng kuchli ta’sir beradi.")
    if indoor <= 4:
        adv.append("Shamollatish past — reja bilan shamollatish yoki filtratsiya.")
    if mask == "Yo‘q" and aqi > 120:
        adv.append("Changli kunlarda niqob (N95/FFP2) foydali bo‘lishi mumkin.")
    if not adv:
        adv.append("Holat yomon emas — profilaktika va monitoringni davom ettiring.")

    for a in adv:
        st.write("•", a)

elif page == "8. SILENT DISASTER (Haqiqat)":
    st.title("🤫 THE SILENT DISASTER")
    st.image("https://images.unsplash.com/photo-1500382017468-9049fed747ef", use_container_width=True)
    st.markdown('<p class="danger-text">OGOHLANTIRISH: Hamma narsa ko\'ringanidan ko\'ra dahshatliroq.</p>', unsafe_allow_html=True)

    st.markdown("<div class='soft-card'><b>Haqiqat bloklari</b><div class='small-muted'>Bu bo‘limni siz xohlagancha kengaytiramiz: dalil, grafik, havola, monitoring.</div></div>", unsafe_allow_html=True)

    st.write("• Ko‘rinmas ifloslanish: PM2.5, VOC, og‘ir metall, mikroplastik.")
    st.write("• Ekotizimga ta’sir: tuproq degradatsiyasi, suv resurslari kamayishi.")
    st.write("• Inson salomatligi: nafas yo‘llari, yurak-qon tomir, stress yuklamasi.")

# ==============================
# 8) FOOTER
# ==============================
st.markdown("""
<div style='text-align: center; border-top: 1px solid #1C1F26; padding: 18px;'>
© 2026 ECO AI WORLD | Egamberdiev Research Group
</div>
""", unsafe_allow_html=True)
