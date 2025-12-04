from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import pandas as pd
import sqlite3
import datetime
import os
import glob

try:
    from sentence_transformers import SentenceTransformer, util
    semantic_available = True
except: semantic_available = False

app = FastAPI(title="Aivory Corporate Brain 13.0")

# --- DATABASE ---
def init_db():
    conn = sqlite3.connect('aivory_logs.db')
    c = conn.cursor()
    try: c.execute("ALTER TABLE logs ADD COLUMN strategy_score INTEGER")
    except: pass
    conn.commit()
    conn.close()
init_db()

# --- MODELLER ---
model = None
hire_model = None
scaler = None
semantic_model = None

try:
    with open("aivory_model.pkl", "rb") as f:
        pkg = pickle.load(f)
        if isinstance(pkg, dict) and "hire_model" in pkg:
            hire_model = pkg["hire_model"]
            scaler = pkg["scaler"]
        else: model = pkg
except: pass

if semantic_available: 
    print("⏳ Laster språkmodell...")
    semantic_model = SentenceTransformer('all-MiniLM-L6-v2')

# --- KUNNSKAPS-LASTING (RAG) ---
CORPORATE_KNOWLEDGE = []
KNOWLEDGE_EMBEDDINGS = None

def load_corporate_knowledge():
    global KNOWLEDGE_EMBEDDINGS
    knowledge_texts = []
    
    # Les alle .txt filer i knowledge_base mappen
    files = glob.glob("knowledge_base/*.txt")
    print(f"📚 Fant {len(files)} dokumenter i kunnskapsbasen.")
    
    for f in files:
        with open(f, "r", encoding="utf-8") as file:
            text = file.read()
            knowledge_texts.append(text)
            print(f"   - Leste: {f}")
            
    if knowledge_texts and semantic_model:
        # Kod om hele biblioteket til vektorer
        KNOWLEDGE_EMBEDDINGS = semantic_model.encode(knowledge_texts, convert_to_tensor=True)
        return knowledge_texts
    return []

# Last kunnskap ved oppstart
if semantic_available:
    CORPORATE_KNOWLEDGE = load_corporate_knowledge()

# --- ANALYSE MOT INTERN KUNNSKAP ---
def check_strategy_fit(candidate_text):
    if KNOWLEDGE_EMBEDDINGS is None or not candidate_text: return 0, []
    
    cand_emb = semantic_model.encode(candidate_text, convert_to_tensor=True)
    
    # Sjekk likhet mot alle interne dokumenter
    hits = util.semantic_search(cand_emb, KNOWLEDGE_EMBEDDINGS, top_k=1)
    best_score = hits[0][0]['score'] * 100
    
    # Finn nøkkelord fra strategien som kandidaten traff på
    # (Forenklet match for demo)
    strategy_keywords = ["rust", "serverless", "inbound", "åpenhet", "gdpr"]
    found_keywords = [w for w in strategy_keywords if w in candidate_text.lower()]
    
    return int(best_score), found_keywords

class CandidateInput(BaseModel):
    Navn: str = "Ukjent"
    Erfaring: int = 0
    Struktur: int = 5
    Driv: int = 5
    Samarbeid: int = 5
    Skill_Match: int = 50
    Jobb_Hopping: int = 1
    Soknadstekst: str = ""
    StillingTittel: str = "Generell"
    JobbBeskrivelse: str = ""
    Lonnskrav: int = 0
    TestSvar: str = ""

@app.post("/predict_hiring")
def predict_candidate(candidate: CandidateInput):
    # 1. ML Score
    ml_score = 50.0
    input_df = pd.DataFrame([{
        "Erfaring": candidate.Erfaring, "Struktur": candidate.Struktur, "Driv": candidate.Driv,
        "Samarbeid": candidate.Samarbeid, "Skill_Match": candidate.Skill_Match, "Jobb_Hopping": candidate.Jobb_Hopping
    }])
    if hire_model and scaler:
        ml_score = hire_model.predict_proba(scaler.transform(input_df))[0][1] * 100

    # 2. Semantisk Jobb-Match
    sem_score = 0
    if semantic_model:
        e1 = semantic_model.encode(candidate.JobbBeskrivelse, convert_to_tensor=True)
        e2 = semantic_model.encode(candidate.Soknadstekst, convert_to_tensor=True)
        sem_score = float(util.pytorch_cos_sim(e1, e2)[0][0]) * 100

    # 3. KUNNSKAPS-MATCH (Nytt!)
    strat_score, strat_hits = check_strategy_fit(candidate.Soknadstekst)
    
    # Vekting: Strategi teller nå 20%
    final_score = (ml_score * 0.4) + (sem_score * 0.4) + (strat_score * 0.2)
    beslutning = "ANSETT" if final_score > 60 else "AVVIS"

    # Logg
    try:
        conn = sqlite3.connect('aivory_logs.db')
        c = conn.cursor()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute("INSERT INTO logs (tidspunkt, navn, score, beslutning, stilling, soknadstekst, strategy_score) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                  (now, candidate.Navn, round(final_score, 1), beslutning, candidate.StillingTittel, candidate.Soknadstekst, strat_score))
        conn.commit()
        conn.close()
    except: pass

    return {
        "anbefaling": beslutning,
        "total_score": round(final_score, 1),
        "analyse": {
            "ml_score": round(ml_score, 1),
            "strategi_match": strat_score
        },
        "kunnskap": {
            "treff": strat_hits,
            "melding": "Kandidaten matcher intern strategi" if strat_score > 40 else "Kandidaten kjenner ikke vår strategi"
        },
        "melding": f"Strategi-score: {strat_score}/100"
    }

@app.post("/get_challenge")
def get_challenge(d: dict): return {"sporsmal": "Hvorfor oss?", "fasit": "Strategi", "niva": "Generell"}
@app.post("/search_candidates")
def search(d: dict): return {"results": []}
