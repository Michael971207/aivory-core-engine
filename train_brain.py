import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import StandardScaler

def train_psych_brain():
    print("🧠 Trener Aivory Deep Psychometric Engine...")
    
    df = pd.read_csv("training_history.csv")
    
    # Input features (Nå mye rikere!)
    features = ["Erfaring", "Skill_Match", "IQ", "Conscientiousness", "Extraversion", "Agreeableness", "Openness", "Neuroticism", "Culture_ID"]
    X = df[features]
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # 1. HJERNE FOR ANSETTELSE
    y_hire = df["Hired"]
    hire_model = RandomForestClassifier(n_estimators=100, random_state=42)
    hire_model.fit(X_scaled, y_hire)
    print(f"✅ Ansettelses-modell trent. (Vekter IQ og Personlighet)")
    
    # 2. HJERNE FOR RETENTION (Lojalitet)
    y_ret = df["Retention"]
    ret_model = RandomForestRegressor(n_estimators=100, random_state=42)
    ret_model.fit(X_scaled, y_ret)
    print(f"✅ Lojalitets-modell trent.")
    
    # Behold eksisterende Knowledge Graph hvis den finnes
    existing_pkg = {}
    try:
        with open("aivory_model.pkl", "rb") as f:
            old = pickle.load(f)
            if isinstance(old, dict): existing_pkg = old
    except: pass
    
    # Oppdater pakken
    package = {
        "hire_model": hire_model,
        "retention_model": ret_model,
        "scaler": scaler,
        "skill_graph": existing_pkg.get("skill_graph", {}), # Behold kunnskap
        "version": "Psych-v1"
    }

    with open("aivory_model.pkl", "wb") as f:
        pickle.dump(package, f)
    
    print("💾 Aivory er nå oppgradert med psykologisk innsikt.")

if __name__ == "__main__":
    train_psych_brain()
