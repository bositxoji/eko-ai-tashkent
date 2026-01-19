import os
from flask import Flask, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>GLOBAL ECO PLATFORM</title>
<meta name="viewport" content="width=device-width, initial-scale=1">

<style>
body {
    margin: 0;
    font-family: Arial, sans-serif;
    background: #0b0e14;
    color: #ffffff;
}

header {
    background: #101522;
    padding: 15px 25px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.menu-btn {
    background: #00d2ff;
    border: none;
    padding: 10px 18px;
    border-radius: 8px;
    font-weight: bold;
    cursor: pointer;
}

.sidebar {
    position: fixed;
    top: 0;
    left: -260px;
    width: 260px;
    height: 100%;
    background: #141a2a;
    padding-top: 60px;
    transition: 0.3s;
}

.sidebar a {
    display: block;
    padding: 15px 25px;
    color: #ffffff;
    text-decoration: none;
    border-bottom: 1px solid #222;
}

.sidebar a:hover {
    background: #00d2ff;
    color: #000;
}

.main {
    padding: 30px;
}

iframe {
    width: 100%;
    height: 75vh;
    border: none;
    border-radius: 12px;
    background: #000;
}
</style>

<script>
function toggleMenu() {
    let menu = document.getElementById("sidebar");
    menu.style.left = (menu.style.left === "0px") ? "-260px" : "0px";
}

function loadSite(url) {
    document.getElementById("contentFrame").src = url;
}
</script>
</head>

<body>

<header>
    <h2>🌍 GLOBAL ECO PLATFORM</h2>
    <button class="menu-btn" onclick="toggleMenu()">☰ MENU</button>
</header>

<div id="sidebar" class="sidebar">
    <a href="#" onclick="loadSite('https://www.iqair.com')">1️⃣ IQAir</a>
    <a href="#" onclick="loadSite('https://www.unep.org')">2️⃣ UNEP</a>
    <a href="#" onclick="loadSite('https://climate.nasa.gov')">3️⃣ NASA</a>
    <a href="#" onclick="loadSite('https://earth.google.com/web')">4️⃣ Google Earth</a>
    <a href="https://gemini.google.com" target="_blank">5️⃣ Gemini (external)</a>
</div>

<div class="main">
    <p style="opacity:0.7;">
        Ekologik monitoring va global manbalar bilan integratsiyalashgan platforma.
    </p>

    <iframe id="contentFrame"
        src="https://www.iqair.com">
    </iframe>
</div>

</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
