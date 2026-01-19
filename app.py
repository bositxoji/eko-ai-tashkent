import streamlit as st

# Sahifa sozlamalari
st.set_page_config(page_title="ECO-WORKSPACE", layout="centered")

# Sarlavha
st.title("🌍 Eco-Web Navigatsiya")
st.write("Tanlangan xizmatga o'tish uchun tugmani bosing:")

st.markdown("---")

# 1. IQAir tugmasi
st.subheader("1. Havo monitoringi")
if st.button("💨 iqair.com saytiga o'tish", use_container_width=True):
    # Bu kod brauzerda yangi oyna ochib yuboradi
    st.markdown('<a href="https://www.iqair.com" target="_blank">Saytga o\'tish uchun bu erni bosing (Yangi oyna)</a>', unsafe_allow_stdio=True)
    st.link_button("IQAir ni ochish", "https://www.iqair.com")

st.markdown("---")

# 7. Gemini tugmasi
st.subheader("7. Sun'iy intellekt")
if st.button("🤖 Gemini (Men bilan gaplashish)", use_container_width=True):
    # To'g'ridan-to'g'ri Gemini rasmiy saytiga o'tkazish
    st.markdown('<a href="https://gemini.google.com" target="_blank">Gemini saytiga o\'tish uchun bu erni bosing (Yangi oyna)</a>', unsafe_allow_stdio=True)
    st.link_button("Gemini AI ga kirish", "https://gemini.google.com")

st.markdown("---")
st.info("Eslatma: Tugmani bosganingizda paydo bo'ladigan ko'k havolani (link) bossangiz, saytlar alohida oynada ochiladi.")
