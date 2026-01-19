import os
import json
import numpy as np
import faiss
from flask import Flask, request, jsonify, render_template_string
from sentence_transformers import SentenceTransformer

# ===============================
# 1. APP INIT
# ===============================
app = Flask(__name__)

# ===============================
# 2. LOAD AI MODEL (SEMANTIC BRAIN)
# ===============================
model = SentenceTransformer("all-MiniLM-L6-v2")

# ===============================
# 3. BIG ECO KNOWLEDGE BASE
# (You can expand this to 10k+ docs)
# ===============================
ECO_DATA = [
    {
        "title": "Water Scarcity",
        "content": "Over 2 billion people lack access to safe drinking water. Climate change and overuse are major drivers. NASA GRACE satellites confirm groundwater depletion."
    },
    {
        "title": "Air Pollution",
        "content": "PM2.5 pollution causes over 7 million premature deaths annually. Transport and industry are the main contributors according to WHO and NASA data."
    },
    {
        "title": "Climate Change",
        "content": "Global temperature has increased by 1.1°C since pre-industrial levels. IPCC warns this will intensify floods, droughts, and heatwaves."
    },
    {
        "title": "Renewable Energy",
        "content": "By 2030, renewable energy must supply over 50% of global electricity to meet climate targets according to IEA and UNEP."
    },
    {
        "title": "Plastic Waste",
        "content": "Every year 8–10 million tons of plastic enter oceans, causing irreversible ecosystem damage according to UNEP and WWF."
    }
]

# ===============================
# 4. VECTORIZE KNOWLEDGE BASE
# ===============================
documents = [item["content"] for item in ECO_DATA]
doc_vectors = model.encode(documents)

dimension = doc_vectors.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(doc_vectors))

# ===============================
# 5. AI REASONING ENGINE
# ===============================
def eco_ai_engine(user_query):
    query_vector = model.encode([user_query])
    D, I = index.search(np.array(query_vector), k=3)

    related_docs = []
    for idx in I[0]:
        related_docs.append(ECO_DATA[idx])

    # Generate human-like analysis
    analysis = ""
    for doc in related_docs:
        analysis += f"<p><b>{doc['title']}:</b> {doc['content']}</p>"

    return f"""
    <div class="expert-report">
        <h3 style="color:#00d2ff;">🌍 GLOBAL ECO-AI ANALYSIS</h3>
        <p><i>User Query:</i> {user_query}</p>
        <hr style="border:1px dashed #333;">
        {analysis}
        <div style="margin-top:15px; padding:10px; background:rgba(0,210,255,0.08); border-radius:6px;">
            <b>Conclusion:</b> This issue is interconnected with global sustainability systems.
            Integrated policy, technology, and AI-based monitoring are required.
        </div>
    </div>
    """

# ===============================
# 6. ROUTES
# ===============================
@app.route("/")
def index():
    return render_template_string("""
<!DOCTYPE html>
<html lang="uz">
<head>
<meta charset="UTF-8">
<title>GLOBAL ECO-AI</title>
<style>
body { background:#0b0e14; color:#e9ecef; font-family:Inter,sans-serif; }
.container { max-width:1100px; margin:40px auto; }
.chat { background:#1a1f26; border-radius:16px; padding:25px; }
#output { min-height:400px; }
input { width:75%; padding:15px; border-radius:10px; border:1px solid #333; background:#0b0e14; color:white; }
button { padding:15px 25px; background:#00d2ff; border:none; border-radius:10px; font-weight:bold; }
</style>
</head>
<body>
<div class="container">
    <h1>🌐 GLOBAL <span style="color:#00d2ff;">ECO-AI</span></h1>
    <div class="chat">
        <div id="output">
            <p style="opacity:.6;">Ekologik savol bering. AI ma’noni tushunadi.</p>
        </div>
        <br>
        <input id="q" placeholder="Masalan: zavod havoga qanday ta’sir qiladi?">
        <button onclick="ask()">TAHLIL</button>
    </div>
</div>

<script>
function ask(){
    let q=document.getElementById("q").value;
    fetch("/ask",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({query:q})
    })
    .then(r=>r.json())
    .then(d=>{
        document.getElementById("output").innerHTML += d.response;
    });
}
</script>
</body>
</html>
""")

@app.route("/ask", methods=["POST"])
def ask():
    query = request.json.get("query","")
    response = eco_ai_engine(query)
    return jsonify({"response": response})

# ===============================
# 7. RUN
# ===============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
