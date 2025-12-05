from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
import datetime
import json
import pickle
import pandas as pd

app = FastAPI(title="Aivory Soolv Backend")

def init_db():
    conn = sqlite3.connect('aivory_logs.db')
    c = conn.cursor()
    
    # 1. JOBBER
    c.execute('''CREATE TABLE IF NOT EXISTS jobs 
                 (id INTEGER PRIMARY KEY, tittel TEXT, beskrivelse TEXT, active INTEGER DEFAULT 1)''')
    
    # 2. BRUKERE/LOGS (Kandidater)
    # Vi samler alt i 'logs' for enkelhet i denne demoen
    cols = [
        "candidate_email TEXT", "candidate_password TEXT", 
        "company_consent INTEGER DEFAULT 0", "candidate_consent INTEGER DEFAULT 0", 
        "chat_history TEXT DEFAULT '[]'", "stilling TEXT", "soknadstekst TEXT", 
        "score REAL", "swot_analysis TEXT", "flight_risk TEXT", "status TEXT DEFAULT 'NEW'",
        "navn TEXT", "tidspunkt TEXT", "beslutning TEXT"
    ]
    
    c.execute('''CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY)''')
    for col in cols:
        try: c.execute(f"ALTER TABLE logs ADD COLUMN {col}")
        except: pass
        
    conn.commit(); conn.close()
init_db()

# --- MODELLER ---
# (Laster dummy-modeller hvis pkl mangler for stabilitet)
model = None
try:
    with open("aivory_model.pkl", "rb") as f: model = pickle.load(f)
except: pass

# --- ENDEPUNKTER ---

class CandidateInput(BaseModel):
    Navn: str; Email: str; Password: str; Soknadstekst: str; StillingTittel: str; JobbBeskrivelse: str

@app.post("/register_candidate")
def register(cand: CandidateInput):
    conn = sqlite3.connect('aivory_logs.db'); c = conn.cursor()
    
    # Sjekk duplikat
    c.execute("SELECT rowid FROM logs WHERE candidate_email = ?", (cand.Email,))
    if c.fetchone(): return {"status": "error", "msg": "Email already exists."}
    
    # Beregn Score (Simulert)
    score = 82
    if len(cand.Soknadstekst) < 20: score = 40
    
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    c.execute("""INSERT INTO logs (
        tidspunkt, navn, candidate_email, candidate_password, soknadstekst, stilling, 
        score, status, company_consent, candidate_consent, chat_history
    ) VALUES (?, ?, ?, ?, ?, ?, ?, 'NEW', 0, 0, '[]')""", 
    (now, cand.Navn, cand.Email, cand.Password, cand.Soknadstekst, cand.StillingTittel, score))
    
    conn.commit(); conn.close()
    return {"status": "success", "total_score": score}

class LoginInput(BaseModel): email: str; password: str
@app.post("/candidate_login")
def login(d: LoginInput):
    conn = sqlite3.connect('aivory_logs.db'); conn.row_factory = sqlite3.Row; c = conn.cursor()
    c.execute("SELECT * FROM logs WHERE candidate_email = ? AND candidate_password = ? ORDER BY tidspunkt DESC LIMIT 1", (d.email, d.password))
    row = c.fetchone(); conn.close()
    if row:
        return {
            "status": "success",
            "navn": row['navn'],
            "stilling": row['stilling'],
            "company_consent": bool(row['company_consent']),
            "candidate_consent": bool(row['candidate_consent']),
            "chat": json.loads(row['chat_history']) if row['chat_history'] else []
        }
    return {"status": "fail"}

# Chat & Consent
class ConsentUpdate(BaseModel): navn: str; who: str; action: bool
@app.post("/update_consent")
def uc(d: ConsentUpdate):
    conn = sqlite3.connect('aivory_logs.db'); c = conn.cursor()
    col = "company_consent" if d.who == "company" else "candidate_consent"
    c.execute(f"UPDATE logs SET {col} = 1 WHERE navn = ?", (d.navn,))
    conn.commit(); conn.close(); return {"status": "ok"}

class ChatMsg(BaseModel): navn: str; sender: str; message: str
@app.post("/send_chat")
def sc(d: ChatMsg):
    conn = sqlite3.connect('aivory_logs.db'); c = conn.cursor()
    c.execute("SELECT chat_history FROM logs WHERE navn = ?", (d.navn,)); r = c.fetchone()
    if r:
        h = json.loads(r[0]) if r[0] else []
        h.append({"sender": d.sender, "msg": d.message})
        c.execute("UPDATE logs SET chat_history = ? WHERE navn = ?", (json.dumps(h), d.navn))
        conn.commit()
    conn.close(); return {"status": "ok"}

@app.post("/get_status")
def gs(d: dict):
    conn = sqlite3.connect('aivory_logs.db'); conn.row_factory = sqlite3.Row; c = conn.cursor()
    c.execute("SELECT * FROM logs WHERE navn = ?", (d.get("navn"),)); row = c.fetchone(); conn.close()
    if row: return {"company_consent": bool(row['company_consent']), "candidate_consent": bool(row['candidate_consent']), "chat": json.loads(row['chat_history']) if row['chat_history'] else []}
    return {"error": "not found"}

# Jobber
@app.get("/get_jobs")
def gj(): conn = sqlite3.connect('aivory_logs.db'); df = pd.read_sql_query("SELECT * FROM jobs WHERE active=1", conn); conn.close(); return df.to_dict(orient="records")
@app.post("/create_job")
def cj(d: dict): conn = sqlite3.connect('aivory_logs.db'); c=conn.cursor(); c.execute("INSERT INTO jobs (tittel, beskrivelse) VALUES (?, ?)", (d['tittel'], d['beskrivelse'])); conn.commit(); conn.close(); return {"status": "ok"}
