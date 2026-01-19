import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ==================================================
# SAHIFA SOZLAMASI (ENG BIRINCHI QATORLARDA BO‘LISHI SHART)
# ==================================================
st.set_page_config(
    page_title="ECO-AI Ekologik Tahlil",
    page_icon="🌍",
    layout="wide"
)

# ==================================================
# Sarlavha
# ==================================================
st.title("🌱 ECO-AI | Ekologik Monitoring va Chuqur Tahlil")
st.markdown(
    """
    Ushbu tizim ekologik ko‘rsatkichlarni **ilmiy, muhandislik va tahliliy**
    yondashuv asosida baholaydi.  
    Barcha tahlillar **to‘liq o‘zbek tilida** taqdim etiladi.
    """
)

# ==================================================
# DEMO MAʼLUMOTLAR (KEYIN CSV BILAN ALMASHTIRISH MUMKIN)
# ==================================================
data = {
    "Yil": [2018, 2019, 2020, 2021, 2022, 2023],
    "CO2 (ppm)": [410, 412, 415, 418, 421, 425],
    "Havo ifloslanishi indeksi": [78, 82, 90, 88, 92, 97],
    "O‘rtacha harorat (°C)": [14.2, 14.4, 14.8, 15.1, 15.4, 15.8]
}

df = pd.DataFrame(data)

# ==================================================
# JADVAL
# ==================================================
st.subheader("📊 Ekologik ko‘rsatkichlar jadvali")
st.dataframe(df, use_container_width=True)

# ==================================================
# GRAFIK (RENDER BILAN MOS)
# ==================================================
st.subheader("📈 Vaqt bo‘yicha ekologik o‘zgarishlar")

fig = plt.figure()
plt.plot(df["Yil"], df["CO2 (ppm)"], marker="o", label="CO2 (ppm)")
plt.plot(df["Yil"], df["Havo ifloslanishi indeksi"], marker="s", label="Havo ifloslanishi")
plt.plot(df["Yil"], df["O‘rtacha harorat (°C)"], marker="^", label="Harorat (°C)")
plt.xlabel("Yil")
plt.ylabel("Qiymat")
plt.legend()
plt.grid(True)

st.pyplot(fig)

# ==================================================
# CHUQUR TAHLIL (ASOSIY QISM)
# ==================================================
st.subheader("🧠 Chuqur ekologik va muhandislik tahlili")

analysis_text = f"""
### 1️⃣ Umumiy ekologik holat

Keltirilgan maʼlumotlarga ko‘ra, {df['Yil'].iloc[0]}–{df['Yil'].iloc[-1]} yillar oralig‘ida
ekologik ko‘rsatkichlarning deyarli barchasida **salbiy o‘sish tendensiyasi** kuzatilmoqda.

Atmosferadagi **CO2 miqdori** {df['CO2 (ppm)'].iloc[0]} ppm dan
{df['CO2 (ppm)'].iloc[-1]} ppm gacha oshgan.
Bu holat sanoat, energetika va transport sektorlaridagi yuklama ortishi bilan bog‘liq.

---

### 2️⃣ Havo ifloslanishi tahlili

Havo ifloslanishi indeksi:
- Eng past qiymat: **{df['Havo ifloslanishi indeksi'].min()}**
- Eng yuqori qiymat: **{df['Havo ifloslanishi indeksi'].max()}**

Mazkur ko‘rsatkichning o‘sishi:
- Aholi salomatligi uchun xavf
- Nafas yo‘llari kasalliklarining ko‘payishi
- Shahar ekologik barqarorligining pasayishi

kabi muammolarni yuzaga keltiradi.

---

### 3️⃣ Harorat va global isish o‘rtasidagi bog‘liqlik

O‘rtacha harorat:
- Boshlang‘ich yil: **{df['O‘rtacha harorat (°C)'].iloc[0]} °C**
- Oxirgi yil: **{df['O‘rtacha harorat (°C)'].iloc[-1]} °C**

CO2 konsentratsiyasining ortishi **issiqxona effekti**ni kuchaytirib,
haroratning bosqichma-bosqich oshishiga sabab bo‘lmoqda.

---

### 4️⃣ Muhandislik nuqtai nazaridan xavf bahosi

Agar ushbu tendensiya saqlanib qolsa:
- Energiya tizimlarida samaradorlik pasayadi
- Iqlimga moslashuv xarajatlari oshadi
- Ekotizimlar degradatsiyasi tezlashadi

Bu esa uzoq muddatda iqtisodiy va ijtimoiy barqarorlikka tahdid soladi.

---

### 5️⃣ Amaliy tavsiyalar (engineering-based)

✅ Qayta tiklanuvchi energiya manbalarini kengaytirish  
✅ Karbon tutish va saqlash (CCS) texnologiyalarini joriy etish  
✅ Yashil shahar infratuzilmasi (daraxtzorlar, yashil tomlar)  
✅ Sunʼiy intellekt asosidagi ekologik monitoring  
✅ Transport tizimini elektrlashtirish  

---

### 🟢 Yakuniy xulosa

Mazkur tahlil shuni ko‘rsatadiki, ekologik muammolar
**nazariy emas**, balki **aniq raqamlar bilan isbotlangan real xavf**dir.

Bugun amalga oshiriladigan muhandislik va boshqaruv qarorlari
kelajak avlodlar uchun barqaror muhitni taʼminlaydi.
"""

st.markdown(analysis_text)

# ==================================================
# FOOTER
# ==================================================
st.markdown("---")
st.success("Tahlil muvaffaqiyatli yakunlandi ✅")
st.caption("ECO-AI | Ekologik monitoring va ilmiy tahlil tizimi")
