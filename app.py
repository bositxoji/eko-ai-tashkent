import os
import numpy as np
from flask import Flask, request, jsonify, render_template_string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# ===============================
# ECO KNOWLEDGE BASE
# ===============================
ECO_DATA = [
    {
        "title": "Water Scarcity",
        "content": "Over 2 billion people lack access to safe drinking water. Climate change and overuse are major drivers."
    },
    {
        "title": "Air Pollution",
        "content": "PM2.5 pollution causes over 7 million premature deaths annually. Transport and industry are main sources."
    },
    {
        "title": "Climate Change",
        "content": "Global temperature increased by 1.1°C. Climate change intensifies floods and droughts."
    },
    {
        "title": "Renewable Energy",
        "content": "Renewable energy must supply 50% of electricity by 2030 to meet climate targets."
    },
    {
        "title": "Plastic Waste",
        "content": "8–10 million tons of plastic enter oceans every year causing ecosystem damage."
    }
]

documents = [d["content"] for d in ECO_DATA]

# ===============================
# LIGHTWEIGHT SEMANTIC ENGINE
# ===============================
vectorizer = TfidfVectorizer(stop_words="english")
doc_vectors = vectorizer.fit_transform(documents)

def eco_ai_engine(query):
    query_vec = vectorizer.transform([query])
    similarities = cosine_similarity(query_vec, doc_vectors)[0]
    top_indices = similarities.argsort()[-3:][::-1]

    analysis = ""
    for i in top_indices:
        analysis += f"<p><b>{ECO_DATA[i]['title']}:</b> {ECO_DATA[i]['content']}</p>"

    return f"""
    <div>
        <h3 style="color:#00d2ff;">🌍 ECO-AI ANALYSIS</h3>
        <p><i>Query:</i> {query}</p>
        <hr>
        {analysis}
        <p style="background:#112;padding:10px;">
        <b>Conclusion:</b> This issue is connected to global ecological sustainability.
        </p>
    </div>
    """

# ===============================
# ROUTES
# ===============================
@app.route("/")
def index():
    return render_template_string("""
    <html>
    <body style="background:#0b0e14;color:white;font-family:Arial">
    <h1>GLOBAL ECO-AI</h1>
    <input id="q" placeholder="Savol yozing">
    <button onclick="ask()">Tahlil</button>
    <div id="out"></div>
    <script>
    function ask(){
        fetch("/ask",{method:"POST",headers:{"Content-Type":"application/json"},
        body:JSON.stringify({query:document.getElementById("q").value})})
        .then(r=>r.json()).then(d=>out.innerHTML+=d.response)
    }
    </script>
    </body>
    </html>
    """)

@app.route("/ask", methods=["POST"])
def ask():
    q = request.json.get("query","")
    return jsonify({"response": eco_ai_engine(q)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
