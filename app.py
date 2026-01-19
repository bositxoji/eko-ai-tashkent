import streamlit as st
import pandas as pd
import requests
import google.generativeai as genai
from streamlit_folium import st_folium
import folium

# --- 1. SAHIFA SOZLAMALARI ---
st.set_page_config(
    page_title="Global Eco-Portal",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. STYLE (DIZAYN) ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    h1 { color: #00d2ff; }
    .stButton>button { width: 100%; border-radius: 5px; background: #1f2937; color: white; border: 1px solid #374151; }
    .stButton>button:hover { border-color: #00d2ff; color: #00d2ff; }
    .metric-card { background: #1f2937; padding: 15px; border-radius: 10px; border-left: 5px solid #00d2ff; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_stdio=True)

# --- 3. SIDEBAR MENYU (NAVIGATSIYA) ---
with st.sidebar:
    st.title("🌐 GLOBAL NAVIGATSIYA")
    st.write("Xalqaro platformalar integratsiyasi")
    
    menu = st.radio(
        "Bo'limni tanlang:",
        [
            "🏠 Bosh Sahifa",
            "1. 💨 IQAir (Havo Sifati)",
            "2. 💧 GEMStat (Suv Sifati)",
            "3. 🌱 SoilGrids (Tuproq)",
            "4. 🌋 USGS (Zilzilalar)",
            "5. 📉 IPCC (Iqlim O'zgarishi)",
            "6. 🗺️ Google Earth (Map)",
            "7. 🤖 Gemini AI (Assistant)"
        ]
    )
    st.divider()
    st.info("Status: Tizim Online ✅")

# --- 4. ASOSIY MANTIQ ---

# === BOSH SAHIFA ===
if menu == "🏠 Bosh Sahifa":
    st.title("🌍 Yagona Ekologik Portal")
    st.markdown("""
    ### Xush kelibsiz!
    Ushbu portal dunyodagi eng yirik **7 ta ekologik va ilmiy platformani** o'zida jamlagan.
    
    **Mavjud imkoniyatlar:**
    * Real vaqtda havo va suv monitoringi.
    * NASA va USGS ma'lumotlari asosida xaritalar.
    * **Google Earth** vizualizatsiyasi.
    * **Gemini AI** orqali aqlli tahlil.
    
    ⬅️ *Ishni boshlash uchun chap tomondagi menyudan birini tanlang.*
    """)

# === 1. IQAir (Havo) ===
elif "IQAir" in menu:
    st.header("💨 IQAir: Global Havo Sifati Monitoringi")
    st.markdown("Real vaqt rejimida hududlardagi havo ifloslanish darajasi (AQI).")
    
    # Iframe orqali IQAir vidjetini qo'shish (Imitatsiya)
    st.info("IQAir Global xaritasi yuklanmoqda...")
    st.components.v1.iframe("https://www.iqair.com/air-quality-map", height=600, scrolling=True)

# === 2. GEMStat (Suv) ===
elif "GEMStat" in menu:
    st.header("💧 GEMStat: Global Suv Sifati")
    st.write("BMT va GEMS/Water dasturi doirasidagi suv resurslari tahlili.")
    st.warning("⚠️ GEMStat to'g'ridan-to'g'ri integratsiyani cheklaydi. Quyidagi tugma orqali rasmiy portalga o'tishingiz mumkin.")
    st.link_button("GEMStat Portaliga O'tish", "https://gemstat.org/")

# === 3. SoilGrids (Tuproq) ===
elif "SoilGrids" in menu:
    st.header("🌱 SoilGrids: Tuproq Tarkibi Xaritasi")
    st.write("ISRIC — World Soil Information ma'lumotlari.")
    st.components.v1.iframe("https://soilgrids.org/", height=600, scrolling=True)

# === 4. USGS (Zilzilalar - API Integratsiyasi) ===
elif "USGS" in menu:
    st.header("🌋 USGS: Real Vaqtda Zilzilalar")
    
    # USGS API dan jonli ma'lumot olish
    try:
        url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_day.geojson"
        response = requests.get(url).json()
        quakes = []
        for feature in response['features']:
            coords = feature['geometry']['coordinates']
            props = feature['properties']
            quakes.append({
                "Joy": props['place'],
                "Magnituda": props['mag'],
                "lat": coords[1],
                "lon": coords[0]
            })
        
        df_quakes = pd.DataFrame(quakes)
        col1, col2 = st.columns([3, 1])
        with col1:
            st.map(df_quakes, latitude='lat', longitude='lon', size='Magnituda')
        with col2:
            st.write("So'nggi 24 soatdagi zilzilalar:")
            st.dataframe(df_quakes[['Joy', 'Magnituda']], height=400)
            
    except Exception as e:
        st.error(f"Ma'lumot olishda xatolik: {e}")

# === 5. IPCC (Iqlim) ===
elif "IPCC" in menu:
    st.header("📉 IPCC: Iqlim O'zgarishi Bo'yicha Hisobotlar")
    st.write("Intergovernmental Panel on Climate Change (IPCC) rasmiy ma'lumotlari.")
    st.components.v1.iframe("https://www.ipcc.ch/", height=600, scrolling=True)

# === 6. Google Earth (Vizualizatsiya) ===
elif "Google Earth" in menu:
    st.header("🗺️ Google Earth (Satellite View)")
    st.write("Sun'iy yo'ldosh orqali yer yuzini kuzatish.")
    
    # Folium yordamida Google Satellite xaritasini yaratish
    m = folium.Map(location=[41.2995, 69.2401], zoom_start=5) # Default: Tashkent
    folium.TileLayer(
        tiles = 'https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
        attr = 'Google',
        name = 'Google Satellite',
        overlay = True,
        control = True
    ).add_to(m)
    
    st_folium(m, width=1200, height=600)

# === 7. Gemini AI (Chat) ===
elif "Gemini" in menu:
    st.header("🤖 Gemini AI: Ekologik Maslahatchi")
    
    # API Kalitni kiritish (Xavfsizlik uchun)
    api_key = st.text_input("Google Gemini API Kalitingizni kiriting:", type="password")
    
    if api_key:
        genai.configure(api_key=api_key)
        
        # Chat tarixi
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Tarixni chiqarish
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Yangi savol
        if prompt := st.chat_input("Savol bering (Masalan: O'zbekistonda suv muammosi)..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            try:
                model = genai.GenerativeModel("gemini-pro")
                response = model.generate_content(prompt)
                
                with st.chat_message("assistant"):
                    st.markdown(response.text)
                
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Xatolik yuz berdi: {e}")
    else:
        st.warning("Iltimos, ishlash uchun API kalitni kiriting. (Agar yo'q bo'lsa, Google AI Studio'dan oling)")
        st.markdown("[API Kalit olish uchun havola](https://aistudio.google.com/app/apikey)")

# --- FOOTER ---
st.markdown("---")
st.caption("© 2026 Global Eco-Portal | Barcha huquqlar himoyalangan.")
