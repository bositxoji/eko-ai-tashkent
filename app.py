import streamlit as st
from streamlit_option_menu import option_menu
import google.generativeai as genai
from streamlit_folium import st_folium
import folium

# 1. Sahifa sozlamasi
st.set_page_config(page_title="ECO-WEB WORKSPACE", layout="wide")

# 2. Asosiy Menyu (Siz aytgan 7 ta punkt)
with st.sidebar:
    selected = option_menu(
        menu_title="ASOSIY MENYU",
        options=[
            "1. IQAir (Havo)", 
            "2. GEMStat (Suv)", 
            "3. SoilGrids (Tuproq)", 
            "4. USGS (Zilzila)", 
            "5. IPCC (Iqlim)", 
            "6. Google Earth (Map)", 
            "7. Gemini AI (Chat)"
        ],
        icons=["wind", "droplet", "layers", "activity", "thermometer", "globe", "robot"],
        default_index=0,
    )

# 3. Har bir menyu bosilganda nima chiqishi
st.header(f"📌 Bo'lim: {selected}")

# --- 1. IQAIR ---
if selected == "1. IQAir (Havo)":
    st.write("IQAir platformasi Google Earth bilan integratsiya qilinmoqda...")
    # Asl saytni oyna ichida ochish
    st.components.v1.iframe("https://www.iqair.com/air-quality-map", height=700, scrolling=True)

# --- 2. GEMSTAT ---
elif selected == "2. GEMStat (Suv)":
    st.write("GEMStat suv monitoringi ma'lumotlari:")
    st.info("GEMStat bazasi yuklanmoqda. Hozircha rasmiy portal oynasi:")
    st.components.v1.iframe("https://gemstat.org/", height=700, scrolling=True)

# --- 3. SOILGRIDS ---
elif selected == "3. SoilGrids (Tuproq)":
    st.write("Tuproq tarkibi va unumdorligi xaritasi:")
    st.components.v1.iframe("https://soilgrids.org/", height=700, scrolling=True)

# --- 4. USGS ---
elif selected == "4. USGS (Zilzila)":
    st.write("USGS Zilzila markazi ma'lumotlari:")
    st.components.v1.iframe("https://earthquake.usgs.gov/", height=700, scrolling=True)

# --- 5. IPCC ---
elif selected == "5. IPCC (Iqlim)":
    st.write("IPCC Iqlim o'zgarishi hisobotlari:")
    st.components.v1.iframe("https://www.ipcc.ch/", height=700, scrolling=True)

# --- 6. GOOGLE EARTH (Kalibratsiya markazi) ---
elif selected == "6. Google Earth (Map)":
    st.write("Barcha ma'lumotlarni yagona Xaritada ko'rish (Google Earth Mode):")
    
    # Xarita yaratish
    m = folium.Map(location=[41.2995, 69.2401], zoom_start=4)
    folium.TileLayer(
        tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
        attr='Google',
        name='Google Satellite',
        overlay=True
    ).add_to(m)
    
    st_folium(m, width=1400, height=700)

# --- 7. GEMINI AI (Foydalanuvchi kirishi) ---
elif selected == "7. Gemini AI (Chat)":
    st.subheader("🤖 Gemini Sun'iy Intellekti bilan ishlash")
    
    # API Kalit so'rash (Foydalanuvchi o'zi kiritadi)
    api_key = st.text_input("Gemini ishga tushirish uchun API kalitni kiriting:", type="password")
    
    if api_key:
        genai.configure(api_key=api_key)
        prompt = st.chat_input("Savol bering...")
        
        if prompt:
            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(prompt)
            st.write(response.text)
    else:
        st.warning("Iltimos, ishlash uchun API kalitni kiriting.")
