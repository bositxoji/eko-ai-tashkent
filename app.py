from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Tashkent Air Live</title>
        <style>
            body { background: #000; color: #00f2fe; font-family: sans-serif; text-align: center; padding-top: 100px; }
            .box { border: 2px solid #00f2fe; display: inline-block; padding: 50px; border-radius: 20px; box-shadow: 0 0 20px #00f2fe; }
            h1 { font-size: 80px; margin: 0; }
        </style>
    </head>
    <body>
        <div class="box">
            <h2>TASHKENT AQI</h2>
            <h1 id="aqi">YUKLANMOQDA...</h1>
            <p id="msg">Ma'lumot qidirilmoqda...</p>
        </div>

        <script>
            async function getData() {
                try {
                    // API so'rovi to'g'ridan-to'g'ri ochiq ulanish orqali
                    const r = await fetch('https://api.waqi.info/feed/tashkent/?token=68f561578e030386d0800b656708306059b02a46');
                    const d = await r.json();
                    if(d.status === 'ok') {
                        document.getElementById('aqi').innerText = d.data.aqi;
                        document.getElementById('msg').innerText = "Hozirgi holat yangilandi";
                    } else {
                        document.getElementById('msg').innerText = "API javob bermadi";
                    }
                } catch(e) {
                    document.getElementById('msg').innerText = "Ulanishda xatolik!";
                }
            }
            getData();
        </script>
    </body>
    </html>
    """)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
