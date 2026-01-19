import streamlit as st

# Sahifa sarlavhasi
st.set_page_config(page_title="ECO-WORKSPACE", layout="centered")

st.title("🌍 Eco-Web Portal")
st.write("Tanlangan xizmatga o'tish uchun quyidagi tugmalarni bosing:")

st.divider()

# 1. IQAir bo'limi
st.subheader("1. IQAir (Havo Monitoringi)")
st.info("Bu tugma iqair.com saytini yangi oynada ochadi.")
st.link_button("💨 iqair.com saytiga o'tish", "https://www.iqair.com", use_container_width=True)

st.divider()

# 7. Gemini bo'limi
st.subheader("7. Gemini AI")
st.success("Bu tugma orqali to'g'ridan-to'g'ri menga (Gemini) o'tasiz. Hech qanday API kalit shart emas!")
st.link_button("🤖 Gemini (Muloqotni boshlash)", "https://gemini.google.com", use_container_width=True)

st.divider()
st.caption("Eslatma: Saytlar xavfsizlik nuqtai nazaridan alohida oynada ochiladi.")
