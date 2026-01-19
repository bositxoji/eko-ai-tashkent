import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# PAGE CONFIG (HAR DOIM ENG TEPADA)
# -----------------------------
st.set_page_config(
    page_title="Ekologik Monitoring",
    page_icon="🌱",
    layout="wide"
)

st.title("🌍 Ekologik Monitoring va Chuqur Tahlil")

st.write(
    "Bu ilova ekologik ko‘rsatkichlarni muhandislik va ilmiy asosda tahlil qiladi."
)

# -----------------------------
# MAʼLUMOTLAR
# -----------------------------
df = pd.DataFrame({
    "Yil": [2018, 2019, 2020, 2021, 2022, 2023],
    "CO2 (ppm)": [410, 412, 415, 418, 421, 425],
    "Ifloslanish indeksi": [78, 82, 90, 88, 92, 97],
    "Harorat (°C)": [14.2, 14.4, 14.8, 15.1, 15.4, 15.8]
})

st.subheader("📊 Jadval")
st.dataframe(df)

# -----------------------------
# GRAFIK (RENDER SAFE)
# -----------------------------
st.subheader("📈 Grafik tahlil")

fig = plt.figure()
plt.plot(df["Yil"], df["CO2 (ppm)"], label="CO2")
plt.plot(df["Yil"], df["Ifloslanish indeksi"], label="Ifloslanish")
plt.plot(df["Yil"], df["Harorat (°C)"], label="Harorat")
plt.xlabel("Yil")
plt.ylabel("Qiymat")
plt.legend()
plt.grid(True)

st.pyplot(fig)

# -----------------------------
# CHUQUR TAHLIL
# -----------------------------
st.subheader("🧠 Ekologik tahlil")

st.markdown("""
### Umumiy xulosa

So‘nggi 6 yil ichida:

- Atmosferadagi **CO2 miqdori izchil oshgan**
- Havo ifloslanishi **sog‘liq uchun xavfli darajaga yaqinlashgan**
- Harorat o‘sishi **global isish jarayonini tasdiqlaydi**

### Muhandislik nuqtai nazari

Agar ushbu trend saqlanib qolsa:
- Karbon tutish tizimlari joriy etilishi shart
- Yashil infratuzilma kengaytirilishi kerak
- AI asosida real vaqt monitoring zarur

### Yakun

Bu raqamlar ekologik muammo **real va o‘lchab bo‘ladigan xavf** ekanini ko‘rsatadi.
""")

st.success("Tahlil muvaffaqiyatli bajarildi ✅")
