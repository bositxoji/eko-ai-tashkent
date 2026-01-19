import streamlit as st

# Sahifa sozlamalari
st.set_page_config(page_title="ECO-WEB WORKSPACE", layout="wide")

# Dizaynni chiroyli qilish (Kattaroq tugmalar)
st.markdown("""
    <style>
    div.stButton > button {
        width: 100%;
        height: 60px;
        font-size: 20px;
        margin-bottom: 10px;
        text-align: left;
        padding-left: 20px;
    }
    </style>
    """, unsafe_allow_stdio=True)

st.title("🌍 Global Eco-Portal Navigatsiyasi")
st.write("Kerakli platformani tanlang. Tugmani bossangiz, sayt yangi oynada ochiladi:")

# Menyu qismini 2 ta ustunga bo'lamiz
col1, col2 = st.columns(2)

with col1:
    # 1. IQAir
    if st.button("💨 1. iqair.com saytiga o'tish"):
        st.write("IQAir ochilmoqda...")
        st.markdown('<meta http-equiv="refresh" content="0;URL=\'https://www.iqair.com\'">', unsafe_allow_stdio=True)
        st.link_button("Agar ochilmasa bu erni bosing", "https://www.iqair.com")

    # 2. GEMStat
    if st.button("💧 2. gemstat.org saytiga o'tish"):
        st.link_button("Saytni ochish", "https://gemstat.org")

    # 3. SoilGrids
    if st.button("🌱 3. soilgrids.org saytiga o'tish"):
        st.link_button("Saytni ochish", "https://soilgrids.org")

with col2:
    # 4. USGS
    if st.button("🌋 4. earthquake.usgs.gov saytiga o'tish"):
        st.link_button("Saytni ochish", "https://earthquake.usgs.gov")

    # 5. IPCC
    if st.button("📉 5. ipcc.ch saytiga o'tish"):
        st.link_button("Saytni ochish", "https://www.ipcc.ch")

    # 6. Google Earth
    if st.button("🗺️ 6. Google Earth (Kalibratsiya)"):
        st.link_button("Xaritani ochish", "https://earth.google.com/web/")

st.divider()

# 7. Gemini (Siz aytgandek, to'g'ridan-to'g'ri menga o'tish)
st.subheader("🤖 Sun'iy Intellekt")
if st.button("✨ 7. GEMINI (Muloqotni boshlash)"):
    st.markdown('<meta http-equiv="refresh" content="0;URL=\'https://gemini.google.com\'">', unsafe_allow_stdio=True)
    st.link_button("Gemini AI ga kirish", "https://gemini.google.com")

st.info("Eslatma: Tugmani bosganingizda brauzer yangi oyna ochishga ruxsat so'rashi mumkin.")
