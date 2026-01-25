import streamlit as st

# Sahifa sarlavhasi va dizayni
st.set_page_config(page_title="ECO-ANALYSIS PORTAL", layout="wide")

# CSS orqali tugmalarni chiroyli va katta qilish
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        height: 80px;
        font-size: 24px !important;
        font-weight: bold;
        border-radius: 15px;
        border: 2px solid #00d4ff;
        background-color: #0e1117;
        color: white;
    }
    .stButton>button:hover {
        background-color: #00d4ff;
        color: black;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🌐 Global Ekologik Tahlil Markazi")
st.write("Barcha tizimlar faol. Kerakli platformani tanlang:")

# 3 ta ustun yaratamiz
col1, col2, col3 = st.columns(3)

with col1:
    st.header("💨 Havo")
    st.write("IQAir - Global havo sifati monitoringi")
    st.link_button("IQAir saytiga o'tish", "https://www.iqair.com")

with col2:
    st.header("🚀 NASA")
    st.write("NASA Earth - Yer monitoringi va sun'iy yo'ldosh ma'lumotlari")
    st.link_button("NASA Earth saytiga o'tish", "https://earth.nasa.gov")

with col3:
    st.header("🤖 Grok AI")
    st.write("X (Twitter) Grok - Ma'lumotlarni tahlil qilish uchun")
    st.link_button("Grok AI ni ochish", "https://grok.com")

st.divider()

# Qo'shimcha tahlil bo'limi
st.subheader("📊 Ma'lumotlar tahlili qanday amalga oshiriladi?")
st.info("""
1. **IQAir** orqali hududingizdagi real vaqt rejimida havo holatini aniqlang.
2. **NASA** platformasidan global iqlim o'zgarishi xaritalarini oling.
3. To'plangan ma'lumotlarni **Grok AI** ga yuborib, chuqur tahlil va prognozlarni oling.
""")

st.success("Tizim 100% tayyor. Renderda 'Deploy' bosing.")
