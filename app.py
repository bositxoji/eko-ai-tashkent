import streamlit as st
import datetime
import pandas as pd
from groq import Groq

# 1. API SOZLAMASI
client = Groq(api_key="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")

# 2. SAHIFA SOZLAMALARI
st.set_page_config(page_title="ECO AI WORLD | 2nd Floor", page_icon="🏗️", layout="wide")

# 3. "SILENT THREAT" DIZAYN KONSEPSIYASI (2-qavat elementlari bilan)
st.markdown("""
    <style>
    .stApp { background-color: #0E1116; color: #A0A0A0; }
    [data-testid="stSidebar"] { background-color: #050505 !important; border-right: 1px solid #1C1F26; }
    
    /* Mualliflar bo'limi - Menyu osti */
    .author-box {
        padding: 12px;
        background: #1C1F26;
        border-radius: 4px;
        border: 1px solid #FFD400;
        margin-top: 10px;
        font-family: 'Inter', sans-serif;
    }
    .author-title { color: #FFD400; font-size: 11px; font-weight: bold; margin: 0; }
    .author-name { color: #FFFFFF; font-size: 13px; margin-bottom: 5px; }

    h1 { color: #FFFFFF !important; text-shadow: 0 0 10px rgba(0,255,136,0.2); }
    h2 { color: #FFD400 !important; }
    .main-card { background: #1C1F26; padding: 20px; border-radius: 4px; border-left: 4px solid #FF3B3B; margin-bottom: 20px; }
    .stButton>button { background-color: #1C1F26; color: #FFD400; border: 1px solid #FFD400; width: 100%; }
    .stButton>button:hover { background-color: #FFD400; color: #000; }
    </style>
    """, unsafe_allow_html=True)

# --- NAVIGATSIYA (2-qavat qo'shildi) ---
with st.sidebar:
    st.markdown("<h1>💠 ECO WORLD</h1>", unsafe_allow_html=True)
    
    # MUALLIFLAR TARKIBI
    st.markdown("""
    <div class="author-box">
        <p class="author-title">ILMIY RAHBAR:</p>
        <p class="author-name">E. EGAMBERDIEV</p>
        <p class="author-title">MUALLIF:</p>
        <p class="author-name">A. ATAXOJAYEV</p>
        <p class="author-title">TEAM:</p>
        <p class="author-name">Egamberdiev</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    page = st.radio("QAVATLAR / FLOORS:", [
        "1-QAVAT: Monitoring Terminal", 
        "1-QAVAT: AI Eco-Judgment",
        "1-QAVAT: Body vs Environment",
        "1-QAVAT: The Silent Mode",
        "2-QAVAT: Eco-Time Machine ⏳",
        "2-QAVAT: Survival Guide 🛡️",
        "2-QAVAT: Carbon Tax Calc 💸"
    ])
    st.success("Tizim barqaror ishlamoqda.")

# =================================================================
# 1-QAVAT FUNKSIYALARI (O'zgarmas saqlangan)
# =================================================================
if "1-QAVAT" in page:
    if "Monitoring" in page:
        st.markdown("<h1>ECO TERMINAL (Poydevor)</h1>", unsafe_allow_html=True)
        st.components.v1.iframe("https://earth.nullschool.net/#current/wind/surface/level/orthographic=-296.22,40.06,500", height=600)
    
    elif "Judgment" in page:
        st.markdown("<h1>AI ECO-JUDGMENT</h1>", unsafe_allow_html=True)
        query = st.text_input("Hukm uchun savol bering:")
        if st.button("ANALIZ"):
            completion = client.chat.completions.create(
                messages=[{"role": "system", "content": "Sen shafqatsiz ekologsan."}, {"role": "user", "content": query}],
                model="llama-3.3-70b-versatile"
            )
            st.markdown(f"<div style='background:black; padding:20px;'>{completion.choices[0].message.content}</div>", unsafe_allow_html=True)

# =================================================================
# 2-QAVAT: ECO-TIME MACHINE (YANGI)
# =================================================================
elif page == "2-QAVAT: Eco-Time Machine ⏳":
    st.markdown("<h1>ECO-TIME MACHINE</h1>", unsafe_allow_html=True)
    st.markdown("<h2>Kelajakni hozir ko'ring</h2>", unsafe_allow_html=True)
    
    
    
    target_year = st.select_slider("Yilni tanlang:", options=[2030, 2050, 2075, 2100])
    
    if st.button(f"{target_year}-yilga sayohat"):
        with st.spinner("AI vaqt chizig'ini hisoblamoqda..."):
            completion = client.chat.completions.create(
                messages=[{"role": "system", "content": "Sen vaqt mashinasisan. Tanlangan yildagi ekologik holatni dahshatli va real tasvirlab ber."}, 
                          {"role": "user", "content": f"{target_year}-yilda O'zbekiston va dunyo ekologiyasi qanday?"}],
                model="llama-3.3-70b-versatile"
            )
            st.markdown(f"<div class='main-card'><h3>STSENARIY: {target_year}</h3>{completion.choices[0].message.content}</div>", unsafe_allow_html=True)

# =================================================================
# 2-QAVAT: SURVIVAL GUIDE (YANGI)
# =================================================================
elif page == "2-QAVAT: Survival Guide 🛡️":
    st.markdown("<h1>SURVIVAL GUIDE AI</h1>", unsafe_allow_html=True)
    st.markdown("<h2>Ekologik ofatda omon qolish qoidalari</h2>", unsafe_allow_html=True)
    
    
    
    scenario = st.selectbox("Ofat turini tanlang:", ["Suv toshqini", "Havo zaharlanishi", "Ekstremal issiqlik", "Oziq-ovqat tanqisligi"])
    
    if st.button("Yo'riqnomani olish"):
        completion = client.chat.completions.create(
            messages=[{"role": "system", "content": "Sen ekstremal vaziyatlarda omon qolish bo'yicha mutaxassis AI'san."}, 
                      {"role": "user", "content": f"{scenario} paytida qanday tirik qolish mumkin?"}],
            model="llama-3.3-70b-versatile"
        )
        st.markdown(f"<div class='main-card'><h3>QO'LLANMA:</h3>{completion.choices[0].message.content}</div>", unsafe_allow_html=True)

# =================================================================
# 2-QAVAT: CARBON TAX CALC (YANGI)
# =================================================================
elif page == "2-QAVAT: Carbon Tax Calc 💸":
    st.markdown("<h1>CARBON TAX CALCULATOR</h1>", unsafe_allow_html=True)
    st.markdown("<h2>Tabiatga yetkazgan zararingizni pulda hisoblang</h2>", unsafe_allow_html=True)
    
    

    km = st.number_input("Kunlik mashina haydash (km):", 0, 500, 20)
    meat = st.checkbox("Bugun go'sht iste'mol qildingizmi?")
    
    if st.button("Hisoblash"):
        tax = (km * 0.2) + (15 if meat else 0)
        st.markdown(f"""
        <div class="main-card">
            <h3>KUNLIK JURM: ${tax}</h3>
            <p>Siz bugun tabiatdan shuncha qiymatdagi resursni tekinga o'g'irladingiz.</p>
        </div>
        """, unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("<div style='text-align: center; border-top: 1px solid #1C1F26; padding: 20px;'>ECO AI WORLD | Team Egamberdiev</div>", unsafe_allow_html=True)
