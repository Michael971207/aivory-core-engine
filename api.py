from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import pandas as pd
import sqlite3
import datetime

app = FastAPI(title="Aivory AI Engine", description="API med Database-logging")

# --- DATABASE OPPSETT ---
def init_db():
    conn = sqlite3.connect('aivory_logs.db')
    c = conn.cursor()
    # Lag tabellen hvis den ikke finnes fra før
    c.execute('''CREATE TABLE IF NOT EXISTS logs
                 (tidspunkt TEXT, navn TEXT, erfaring INTEGER, struktur INTEGER, 
                  driv INTEGER, samarbeid INTEGER, score REAL, beslutning TEXT)''')
    conn.commit()
    conn.close()

init_db() # Kjør oppsettet når serveren starter

# Last inn hjernen
try:
    with open("aivory_model.pkl", "rb") as f:
        model = pickle.load(f)
    print("✅ AI-Hjernen er lastet inn.")
except FileNotFoundError:
    print("❌ Fant ikke modellen.")

class CandidateInput(BaseModel):
    Navn: str = "Ukjent" # Vi legger til navn i API-et nå for loggingens skyld
    Erfaring: int
    Struktur: int
    Driv: int
    Samarbeid: int
    Skill_Match: int

@app.post("/predict_hiring")
def predict_candidate(candidate: CandidateInput):
    # 1. Forbered data til modellen (Fjern navn, modellen skjønner ikke tekst)
    input_data = {
        "Erfaring": candidate.Erfaring,
        "Struktur": candidate.Struktur,
        "Driv": candidate.Driv,
        "Samarbeid": candidate.Samarbeid,
        "Skill_Match": candidate.Skill_Match
    }
    df = pd.DataFrame([input_data])
    
    # 2. Spør AI
    probability = model.predict_proba(df)[0][1] # Sannsynlighet
    beslutning = "ANSETT" if probability > 0.6 else "AVVIS"
    
    # 3. LAGRE I DATABASE (Hukommelsen)
    conn = sqlite3.connect('aivory_logs.db')
    c = conn.cursor()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    c.execute("INSERT INTO logs VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
              (timestamp, candidate.Navn, candidate.Erfaring, candidate.Struktur, 
               candidate.Driv, candidate.Samarbeid, round(probability*100, 1), beslutning))
    
    conn.commit()
    conn.close()
    
    print(f"💾 Logget: {candidate.Navn} -> {beslutning}")

    return {
        "anbefaling": beslutning,
        "score": round(probability * 100, 1),
        "melding": "Loggført i databasen."
    }

@app.get("/")
def home():
    return {"status": "Aivory Database Server Online 🟢"}
