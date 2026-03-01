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

def fetch_rss(url):
    # minimal RSS read (simple)
    r = requests.get(url, timeout=20)
    r.raise_for_status()
    return r.text

def simple_extract_titles(xml_text, limit=5):
    # quick extraction without extra libs
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

def summarize(title, url, lang="uz"):
    # If AI not available -> fallback summary
    if client is None:
        return f"{title} — batafsil: {url}"

    prompt = f"""
Til: {lang}.
Manba: {url}
Sarlavha: {title}

Vazifa:
1) 2-3 gaplik aniq ekologik summary yoz.
2) Qaysi bo‘limga mosligini ayt: Air / Water / Climate / Disasters / Industry.
3) 3 ta kalit so‘z ber.
Format:
SUMMARY: ...
SECTION: ...
TAGS: ...
"""
    try:
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role":"user","content":prompt}]
        )
        return res.choices[0].message.content
    except Exception:
        return f"{title} — batafsil: {url}"

def parse_section(ai_text: str):
    # default
    section = "Climate"
    if "SECTION:" in ai_text:
        sec = ai_text.split("SECTION:")[1].splitlines()[0].strip()
        if sec:
            section = sec
    return section

def parse_summary(ai_text: str):
    if "SUMMARY:" in ai_text:
        s = ai_text.split("SUMMARY:")[1].split("SECTION:")[0].strip()
        if s:
            return s
    # fallback: first 300 chars
    return ai_text.strip()[:300]

def exists_url(url: str) -> bool:
    conn = db()
    r = conn.execute("SELECT 1 FROM posts WHERE url=? LIMIT 1", (url,)).fetchone()
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

def generate_monthly_report(year: int, month: int, lang: str):
    conn = db()
    start = datetime.datetime(year, month, 1)
    if month == 12:
        end = datetime.datetime(year+1, 1, 1)
    else:
        end = datetime.datetime(year, month+1, 1)

    rows = conn.execute(
        "SELECT section, title, summary FROM posts WHERE created_at>=? AND created_at<? AND lang=? ORDER BY created_at ASC",
        (start.isoformat(), end.isoformat(), lang)
    ).fetchall()

    if not rows:
        conn.close()
        return

    # group by section
    sections = {}
    for sec, title, summary in rows:
        sections.setdefault(sec, []).append((title, summary))

    text_blob = ""
    for sec, items in sections.items():
        text_blob += f"\n## {sec}\n"
        for t, s in items[:20]:
            text_blob += f"- {t}: {s}\n"

    if client is None:
        report = f"{year}-{month} report (lang={lang})\n" + text_blob
    else:
        prompt = f"""
Til: {lang}
Quyidagi arxiv asosida oylik HISOBOT yoz.
Bo‘limlar kesimida: asosiy trendlar, muammolar, tavsiyalar.
Qisqa statistikalar ham qo‘sh: har bo‘limda nechta yangilik chiqqanini ayt.
Arxiv:
{text_blob}
"""
        try:
            res = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role":"user","content":prompt}]
            )
            report = res.choices[0].message.content
        except Exception:
            report = f"{year}-{month} report (lang={lang})\n" + text_blob

    conn.execute(
        "INSERT OR REPLACE INTO reports(year, month, lang, content, created_at) VALUES (?,?,?,?,?)",
        (year, month, lang, report, datetime.datetime.utcnow().isoformat())
    )
    conn.commit()
    conn.close()

def run():
    init_db()

    # RSS sources (ekologiya uchun)
    sources = [
        ("UN News - Climate", "https://news.un.org/feed/subscribe/en/news/topic/climate-change/feed/rss.xml"),
        ("NASA Earth Observatory", "https://earthobservatory.nasa.gov/feeds/earth-observatory.rss"),
        ("World Bank - Environment", "https://www.worldbank.org/en/topic/environment/rss"),
    ]

    langs = ["uz", "ru", "en", "tr"]

    for source_name, rss in sources:
        xml = fetch_rss(rss)
        items = simple_extract_titles(xml, limit=5)

        for title, url in items:
            if exists_url(url):
                continue

            # 4 tilda saqlaymiz
            for lang in langs:
                ai = summarize(title, url, lang=lang)
                section = parse_section(ai)
                summary = parse_summary(ai)
                save_post(section, title, summary, source_name, url, lang)

    # oylik report: har oyning 1-kuni (UTC) ishlasa yaratadi
    now = datetime.datetime.utcnow()
    if now.day == 1:
        # o‘tgan oy
        y = now.year
        m = now.month - 1
        if m == 0:
            m = 12
            y -= 1
        for lang in langs:
            generate_monthly_report(y, m, lang)

if __name__ == "__main__":
    run()
