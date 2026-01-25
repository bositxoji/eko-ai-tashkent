import streamlit as st
from fpdf import FPDF
import base64

# 1. SAHIFA SOZLAMALARI
st.set_page_config(
    page_title="ECO-INSIGHT | Global Monitoring Center",
    page_icon="🌍",
    layout="wide"
)

# 2. PROFESSIONAL DIZAYN (CSS)
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(180deg, #050a05 0%, #000000 100%);
        color: #e0f2f1;
    }
    .service-card {
        background: rgba(0, 255, 136, 0.03);
        border: 1px solid rgba(0, 255, 136, 0.2);
        border-radius: 15px;
        padding: 20px;
        transition: 0.4s;
        height: 200px;
    }
    .service-card:hover {
        background: rgba(0, 255, 136, 0.08);
        border-color: #00ff88;
        box-shadow: 0 0 15px rgba(0, 255, 136, 0.3);
    }
    h1, h2, h3 { color: #00ff88 !important; }
    .stLinkButton > a {
        background: transparent !important;
        border: 1px solid #00ff88 !important;
        color: #00ff88 !important;
        width: 100%;
        text-align: center;
        border-radius: 8px;
    }
    .stLinkButton > a:hover {
        background: #00ff88 !important;
        color: black !important;
    }
    .pdf-box {
        background: rgba(255, 255, 255, 0.05);
        padding: 20px;
        border-radius: 10px;
        border: 1px dashed #00ff88;
    }
    </style>
    """, unsafe_allow_html=True)

# --- PDF GENERATOR FUNKSIYASI ---
def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="ECO-INSIGHT GLOBAL ANALYSIS REPORT", ln=1, align='C')
    pdf.ln(10)
    pdf.multi_cell(0, 10, txt=text)
    pdf.ln(20)
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt="Analyzed by Team Proff. Egamberdiev E.", ln=1, align='R')
    return pdf.output(dest='S').encode('latin-1')

# --- SAHIFA BOSH QISMI ---
st.title("🌐 ECO-INSIGHT: GLOBAL EKOLOGIK MONITORING")
st.markdown("**NASA, IQAIR va Grok AI ma'lumotlari asosida tahlil markazi.**")

st.divider()

# --- ASOSIY XIZMATLAR ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="service-card"><h3>💨 IQAIR</h3><p>Havo sifati monitoringi.</p></div>', unsafe_allow_html=True)
    st.link_button("Havoni tekshirish", "https://www.iqair.com")

with col2:
    st.markdown('<div class="service-card"><h3>🛰️ NASA EARTH</h3><p>Kosmosdan yer monitoringi.</p></div>', unsafe_allow_html=True)
    st.link_button("NASA tasvirlari", "https://earth.gsfc.nasa.gov")

with col3:
    st.markdown('<div class="service-card"><h3>🤖 GROK AI</h3><p>Chuqur AI tahlil xizmati.</p></div>', unsafe_allow_html=True)
    st.link_button("Grok AI ni ochish", "https://grok.com/?q=Analyze+global+eco+news")

with col4:
    st.markdown('<div class="service-card"><h3>🔥 FIRE MAP</h3><p>Global yong‘inlar monitoringi.</p></div>', unsafe_allow_html=True)
    st.link_button("Jonli xarita", "https://firms.modaps.eosdis.nasa.gov/map/")

st.divider()

# --- YANGI: PDF HISOBOT TAYYORLASH BO'LIMI ---
st.subheader("📑 Professional AI Hisobot Generator (PDF)")
st.markdown("Grok AI dan olingan tahlillarni pastga joylang va PDF shaklida yuklab oling:")

with st.container():
    st.markdown('<div class="pdf-box">', unsafe_allow_html=True)
    report_text = st.text_area("Tahlil matnini shu yerga joylang:", height=200, placeholder="Grok AI dan olingan matnni shu yerga kiritasiz...")
    
    if st.button("📄 PDF Hisobotni Tayyorlash"):
        if report_text:
            pdf_data = create_pdf(report_text)
            st.download_button(
                label="📥 PDF-ni yuklab olish",
                data=pdf_data,
                file_name="Eco_Insight_Report.pdf",
                mime="application/pdf"
            )
            st.success("Hisobot muvaffaqiyatli tayyorlandi!")
        else:
            st.warning("Iltimos, avval matnni kiriting.")
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# --- JONLI XARITA ---
st.subheader("🌍 Real vaqtdagi Global Havo Oqimlari")
st.components.v1.iframe("https://earth.nullschool.net/#current/wind/surface/level/orthographic=-296.22,40.06,500", height=500)

# --- FOOTER ---
st.markdown(f"""
    <div style="text-align: center; margin-top: 50px; padding: 30px; border-top: 1px solid rgba(0, 255, 136, 0.2);">
        <p style="color: rgba(255,255,255,0.6);">© 2026 ECO-INSIGHT Platformasi | Barcha huquqlar himoyalangan.</p>
        <p style="font-size: 1.3rem; font-weight: bold; color: #00ff88;">
            Mualliflar: <span style="color: #00d4ff;">Team Proff. Egamberdiev E.</span>
        </p>
    </div>
""", unsafe_allow_html=True)
