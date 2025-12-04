from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pickle
import pandas as pd
import sqlite3
import datetime
# Vi pakker importen i en try/except for å fange installasjonsfeil
try:
    from sentence_transformers import SentenceTransformer, util
    semantic_available = True
except ImportError:
    semantic_available = False
    print("⚠️ ADVARSEL: Sentence-transformers mangler. Kjører uten tekstforståelse.")

app = FastAPI(title="Aivory Robust Engine")

# --- DATABASE ---
def init_db():
    conn = sqlite3.connect('aivory_logs.db')
    c = conn.cursor()
    try:
        c.execute("ALTER TABLE logs ADD COLUMN semantisk_match REAL")
    except sqlite3.OperationalError:
        pass
    conn.commit()
    conn.close()
init_db()

# --- MODELLER ---
model = None
scaler = None
semantic_model = None

# Last ML
try:
    with open("aivory_model.pkl", "rb") as f:
        package = pickle.load(f)
        if isinstance(package, dict):
            model = package["model"]
            scaler = package["scaler"]
        else:
            model = package
    print("✅ ML-Hjerne lastet.")
except Exception as e:
    print(f"❌ Kunne ikke laste ML-modell: {e}")

# Last NLP
if semantic_available:
    try:
        print("⏳ Laster språkmodell (Vent litt)...")
        semantic_model = SentenceTransformer('all-MiniLM-L6-v2')
        print("✅ Språkmodell lastet.")
    except Exception as e:
        print(f"❌ Feil med språkmodell: {e}")

class CandidateInput(BaseModel):
    Navn: str
    Erfaring: int
    Struktur: int
    Driv: int
    Samarbeid: int
    Skill_Match: int
    Soknadstekst: str = ""

@app.post("/predict_hiring")
def predict_candidate(candidate: CandidateInput):
    # SIKKERHETSSJEKK: Har vi en hjerne?
    if model is None:
        raise HTTPException(status_code=500, detail="Serverfeil: ML-modellen er ikke lastet inn. Kjør train_brain.py!")

    # 1. ML Analyse
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

    ml_probability = model.predict_proba(final_input)[0][1] * 100

    # 2. Semantisk Analyse
    semantic_score = 0
    if semantic_model and candidate.Soknadstekst:
        # Enkel fasit for demo
        JOB_DESC = "Python AI Machine Learning ansvar selvstendig lede prosjekter team"
        emb1 = semantic_model.encode(JOB_DESC, convert_to_tensor=True)
        emb2 = semantic_model.encode(candidate.Soknadstekst, convert_to_tensor=True)
        # Beregn likhet
        sim = util.pytorch_cos_sim(emb1, emb2)
        semantic_score = float(sim[0][0]) * 100
        if len(candidate.Soknadstekst.split()) < 5: semantic_score *= 0.5
    
    # 3. Total
    final_score = (ml_probability * 0.6) + (semantic_score * 0.4)
    beslutning = "ANSETT" if final_score > 60 else "AVVIS"

    # 4. Logg
    try:
        conn = sqlite3.connect('aivory_logs.db')
        c = conn.cursor()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute("INSERT INTO logs (tidspunkt, navn, score, beslutning) VALUES (?, ?, ?, ?)", 
                  (now, candidate.Navn, round(final_score, 1), beslutning))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Logg-feil: {e}")

    return {
        "anbefaling": beslutning,
        "total_score": round(final_score, 1),
        "analyse": {"semantisk_match": round(semantic_score, 1)},
        "melding": "Hybrid analyse fullført."
    }
