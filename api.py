from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import pandas as pd
import sqlite3
import datetime
import re # Bibliotek for tekstanalyse (Regular Expressions)

app = FastAPI(title="Aivory Hybrid Engine", description="ML + NLP (Tekstanalyse)")

def init_db():
    conn = sqlite3.connect('aivory_logs.db')
    c = conn.cursor()
    # Vi legger til en kolonne for 'tekst_score' i databasen
    try:
        c.execute("ALTER TABLE logs ADD COLUMN tekst_score REAL")
    except sqlite3.OperationalError:
        pass # Kolonnen finnes kanskje fra før, det går bra
    conn.commit()
    conn.close()

init_db()

# Last inn ML-modellen
model = None
scaler = None
model_type = "Ukjent"

try:
    with open("aivory_model.pkl", "rb") as f:
        package = pickle.load(f)
        if isinstance(package, dict):
            model = package["model"]
            scaler = package["scaler"]
            model_type = package["type"]
        else:
            model = package
    print(f"✅ AI-Hjernen ({model_type}) er lastet inn.")
except FileNotFoundError:
    print("❌ Fant ikke modellen.")

# --- NLP MODUL (Tekstanalyseren) ---
POWER_WORDS = [
    "ledet", "suksess", "ekspert", "ansvar", "innovasjon", "effektivisert", 
    "resultater", "motivert", "selvgående", "python", "ai", "utviklet", "team"
]

def analyze_text_quality(text):
    if not text:
        return 0
    
    text = text.lower()
    score = 0
    matches = []
    
    # 1. Sjekk lengde (for kort = dårlig, for lang = kjedelig?)
    word_count = len(text.split())
    if word_count > 20: score += 10
    if word_count > 50: score += 10
    
    # 2. Let etter Power Words
    for word in POWER_WORDS:
        if word in text:
            score += 5 # 5 poeng per gull-ord
            matches.append(word)
            
    # Max score er 100
    return min(score, 100), matches

# Input-modellen inkluderer nå 'Soknadstekst'
class CandidateInput(BaseModel):
    Navn: str
    Erfaring: int
    Struktur: int
    Driv: int
    Samarbeid: int
    Skill_Match: int
    Soknadstekst: str = "" # Valgfri tekst

@app.post("/predict_hiring")
def predict_candidate(candidate: CandidateInput):
    # 1. Kjør ML-analyse på tallene
    input_data = pd.DataFrame([{
        "Erfaring": candidate.Erfaring,
        "Struktur": candidate.Struktur,
        "Driv": candidate.Driv,
        "Samarbeid": candidate.Samarbeid,
        "Skill_Match": candidate.Skill_Match
    }])
    
    if scaler:
        final_input = scaler.transform(input_data)
    else:
        final_input = input_data

    ml_probability = model.predict_proba(final_input)[0][1] * 100 # 0-100 score
    
    # 2. Kjør NLP-analyse på teksten
    nlp_score, found_words = analyze_text_quality(candidate.Soknadstekst)
    
    # 3. HYBRID SCORE (Vekting: 70% tall, 30% tekst)
    final_score = (ml_probability * 0.7) + (nlp_score * 0.3)
    
    beslutning = "ANSETT" if final_score > 60 else "AVVIS"
    
    # 4. Logg til database
    conn = sqlite3.connect('aivory_logs.db')
    c = conn.cursor()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Vi logger litt forenklet her for å unngå SQL-feil hvis skjemaet ikke matcher perfekt
    c.execute("INSERT INTO logs (tidspunkt, navn, score, beslutning) VALUES (?, ?, ?, ?)", 
              (timestamp, candidate.Navn, round(final_score, 1), beslutning))
    conn.commit()
    conn.close()

    return {
        "anbefaling": beslutning,
        "total_score": round(final_score, 1),
        "detaljer": {
            "ml_score": round(ml_probability, 1),
            "tekst_score": nlp_score,
            "nøkkelord_funnet": found_words
        },
        "melding": f"Basert på {model_type} og tekstanalyse."
    }
