import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# SAHIFA SOZLAMALARI
# -----------------------------
st.set_page_config(
    page_title="Ekologik Monitoring va Tahlil",
    page_icon="🌱",
    layout="wide"
)

st.title("🌍 Ekologik Monitoring va Chuqur Tahlil Tizimi")
st.markdown(
    """
    Ushbu ilova ekologik maʼlumotlarni **muhandislik va ilmiy nuqtai nazardan**
    tahlil qiladi. Natijalar **to‘liq o‘zbek tilida** va **keng sharhlar bilan**
    beriladi.
    """
)

# -----------------------------
# DEMO MAʼLUMOTLAR
# -----------------------------
data = {
    "Yil": [2018, 2019, 2020, 2021, 2022, 2023],
    "CO2 (ppm)": [410, 412, 415, 418, 421, 425],
    "Havo ifloslanishi indeksi": [78, 82, 90, 88, 92, 97],
    "O‘rtacha harorat (°C)": [14.2, 14.4, 14.8, 15.1, 15.4, 15.8]
}

df = pd.DataFrame(data)

st.subheader("📊 Ekologik ko‘rsatkichlar jadvali")
st.dataframe(df, use_container_width=True)

# -----------------------------
# GRAFIK
# -----------------------------
st.subheader("📈 Vaqt bo‘yicha o‘zgarishlar")

fig, ax = plt.subplots()
ax.plot(df["Yil"], df["CO2 (ppm)"], marker='o', label="CO2 (ppm)")
ax.plot(df["Yil"], df["Havo ifloslanishi indeksi"], marker='s', label="Havo ifloslanishi")
ax.plot(df["Yil"], df["O‘rtacha harorat (°C)"], marker='^', label="Harorat (°C)")
ax.set_xlabel("Yil")
ax.set_ylabel("Qiymat")
ax.legend()
ax.grid(True)

st.pyplot(fig)

# -----------------------------
# CHUQUR TAHLIL (ASOSIY QISM)
# -----------------------------
st.subheader("🧠 Muhandislik va Ekologik Chuqur Tahlil")

analysis_text = f"""
### 1️⃣ Umumiy holat tahlili

2018–2023 yillar oralig‘ida ekologik ko‘rsatkichlarda **barqaror salbiy o‘sish**
kuzatilmoqda. Ayniqsa, atmosferadagi **CO2 konsentratsiyasi** {df['CO2 (ppm)'].iloc[0]} ppm dan
{df['CO2 (ppm)'].iloc[-1]} ppm gacha oshgan.

Bu esa sanoatlashuv, transport vositalarining ko‘payishi va yashil hududlarning
kamayishi bilan bevosita bog‘liq.

---

### 2️⃣ Havo ifloslanishi indeksi tahlili

Havo ifloslanishi indeksi:
- Minimal qiymat: **{df['Havo ifloslanishi indeksi'].min()}**
- Maksimal qiymat: **{df['Havo ifloslanishi indeksi'].max()}**

Bu ko‘rsatkichning oshishi:
- Aholi salomatligiga xavf
- Nafas yo‘llari kasalliklarining ko‘payishi
- Shahar ekologik barqarorligining buzilishi

kabi muammolarni keltirib chiqaradi.

---

### 3️⃣ Harorat o‘sishining ilmiy izohi

O‘rtacha harorat:
- 2018 yilda: **{df['O‘rtacha harorat (°C)'].iloc[0]} °C**
- 2023 yilda: **{df['O‘rtacha harorat (°C)'].iloc[-1]} °C**

Bu **global isish (global warming)** jarayonining mahalliy ko‘rinishidir.
CO2 miqdori ortishi issiqxona effektini kuchaytirib,
haroratning yilma-yil oshishiga sabab bo‘lmoqda.

---

### 4️⃣ Muhandislik nuqtai nazaridan xulosa

Agar mavjud trend davom etsa:
- Energiya samarador texnologiyalar joriy etilmasa
- Karbonni ushlash (Carbon Capture) tizimlari qo‘llanilmasa
- Yashil infratuzilma kengaytirilmasa

2025–2030 yillarga borib ekologik holat **kritik bosqichga** yetishi mumkin.

---

### 5️⃣ Tavsiyalar (engineering-based)

✅ Dikey bog‘lar va yashil tomlar  
✅ Karbon tutish modullari  
✅ Sunʼiy intellekt asosidagi monitoring  
✅ Sanoatda chiqindi gazlarni filtrlash  
✅ Transportni elektrlashtirish  

---

### 🟢 Yakuniy xulosa

Mazkur tahlil shuni ko‘rsatadiki, ekologik muammolar **faqat nazariy emas**,
balki **aniq raqamlar bilan isbotlangan real xavf**dir.

Agar bugun choralar ko‘rilmasa, ertaga iqtisodiy va ijtimoiy yo‘qotishlar
yanada kuchayadi.
"""

st.markdown(analysis_text)

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.markdown("🌱 **Ekologik AI Monitoring Tizimi** | Ilmiy va muhandislik tahlili")
