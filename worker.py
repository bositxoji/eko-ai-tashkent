import os
import sqlite3
import datetime
import requests
from groq import Groq

DB_PATH = "storage.db"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

def db():
    conn = sqlite3.connect(DB_PATH)
    return conn

def init_db():
    conn = db()
    conn.execute("""
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TEXT NOT NULL,
        section TEXT NOT NULL,
        title TEXT NOT NULL,
        summary TEXT NOT NULL,
        source TEXT NOT NULL,
        url TEXT NOT NULL,
        lang TEXT NOT NULL
    );
    """)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        year INTEGER NOT NULL,
        month INTEGER NOT NULL,
        lang TEXT NOT NULL,
        content TEXT NOT NULL,
        created_at TEXT NOT NULL,
        UNIQUE(year, month, lang)
    );
    """)
    conn.commit()
    conn.close()

def exists_url(url: str, lang: str) -> bool:
    conn = db()
    r = conn.execute("SELECT 1 FROM posts WHERE url=? AND lang=? LIMIT 1", (url, lang)).fetchone()
    conn.close()
    return r is not None

def save_post(section, title, summary, source, url, lang):
    conn = db()
    conn.execute(
        "INSERT INTO posts(created_at, section, title, summary, source, url, lang) VALUES (?,?,?,?,?,?,?)",
        (datetime.datetime.utcnow().isoformat(), section, title, summary, source, url, lang)
    )
    conn.commit()
    conn.close()

def fetch_rss(url):
    r = requests.get(url, timeout=25)
    r.raise_for_status()
    return r.text

def simple_extract(xml_text, limit=8):
    # minimal RSS parsing
    items = []
    parts = xml_text.split("<item>")
    for p in parts[1:limit+1]:
        title = ""
        link = ""
        if "<title>" in p and "</title>" in p:
            title = p.split("<title>")[1].split("</title>")[0].strip()
        if "<link>" in p and "</link>" in p:
            link = p.split("<link>")[1].split("</link>")[0].strip()
        if title and link:
            items.append((title, link))
    return items

def ai_pack(title: str, url: str, lang: str):
    # fallback
    if client is None:
        return ("Climate", f"{title}. Batafsil: {url}")

    prompt = f"""
Til: {lang}
Sarlavha: {title}
Manba: {url}

2-3 gaplik ekologik summary yoz.
Bo‘limni tanla: Air / Water / Climate / Disasters / Industry.
Natija faqat shu formatda:
SECTION: ...
SUMMARY: ...
"""
    try:
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
        )
        text = res.choices[0].message.content.strip()
        sec = "Climate"
        summ = text[:260]
        if "SECTION:" in text:
            sec = text.split("SECTION:")[1].splitlines()[0].strip() or "Climate"
        if "SUMMARY:" in text:
            summ = text.split("SUMMARY:")[1].strip()
        return (sec, summ)
    except Exception:
        return ("Climate", f"{title}. Batafsil: {url}")

def run():
    init_db()

    sources = [
        ("UN News - Climate", "https://news.un.org/feed/subscribe/en/news/topic/climate-change/feed/rss.xml"),
        ("NASA Earth Observatory", "https://earthobservatory.nasa.gov/feeds/earth-observatory.rss"),
        ("World Bank - Environment", "https://www.worldbank.org/en/topic/environment/rss"),
    ]

    langs = ["uz", "ru", "en", "tr"]

    for source_name, rss in sources:
        try:
            xml = fetch_rss(rss)
            items = simple_extract(xml, limit=6)
        except Exception:
            continue

        for title, url in items:
            for lang in langs:
                if exists_url(url, lang):
                    continue
                section, summary = ai_pack(title, url, lang)
                save_post(section, title, summary, source_name, url, lang)

if __name__ == "__main__":
    run()
