import streamlit as st
import requests
import google.generativeai as genai
import os

# Sahifa dizayni
st.set_page_config(page_title="Neural Eco AI", page_icon="🌱")

st.markdown("""
    <style>
    .main { background-color: #050505; color: white; }
    .stMetric { background-color: #111; padding: 20px; border-radius: 15px; border: 1px solid #00f2fe; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌐 NEURAL ECO-MONITOR")

# API Kalitlari (Streamlit Secrets-ga kiritiladi yoki bu yerda qoladi)
GEMINI_KEY = st.secrets.get("GEMINI_API_KEY", "AIzaSyCl-dBQmgQTJWgA5LR0Fy5Wiq7HLxaHK2Y")
WAQI_TOKEN = "68f561578e030386d0800b656708306059b02a46"

# Ma'lumot olish
city = "Tashkent"
url = f"https://api.waqi.info/feed/{city}/?token={WAQI_TOKEN}"

try:
    r = requests.get(url).json()
    if r['status'] == 'ok':
        aqi = r['data']['aqi']
        temp = r['data']['iaqi']['t']['v']
        hum = r['data']['iaqi']['h']['v']

        col1, col2, col3 = st.columns(3)
        col1.metric("AQI Index", aqi)
        col2.metric("Temp", f"{temp}°C")
        col3.metric("Hum", f"{hum}%")

        # Gemini AI tahlili
        genai.configure(api_key=GEMINI_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        with st.spinner('AI tahlil qilmoqda...'):
            response = model.generate_content(f"Havo AQI {aqi}. 1 ta qisqa gapda maslahat ber.")
            st.info(f"🤖 AI Maslahati: {response.text}")
    else:
        st.error("API ma'lumot bera olmadi.")
except Exception as e:
    st.write("Ulanishda xatolik yuz berdi.")
