import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import StandardScaler

def train_pro_models():
    print("🧠 Trener Aivory Pro Models (Multi-Industry)...")
    
    df = pd.read_csv("training_big_data.csv")
    
    # Input features (Alt AI-en vet om kandidaten)
    X = df[["Bransje_ID", "Erfaring", "Struktur", "Driv", "Samarbeid", "Ekstroversjon", "Skill_Match", "Jobb_Hopping", "IQ"]]
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # 1. HJERNE FOR ANSETTELSE (Classifier)
    print("   -> Trener Ansettelses-logikk...")
    hire_model = RandomForestClassifier(n_estimators=150, random_state=42)
    hire_model.fit(X_scaled, df["Hired"])
    
    # 2. HJERNE FOR RISIKO (Classifier)
    print("   -> Trener Risiko-analyse...")
    risk_model = RandomForestClassifier(n_estimators=100, random_state=42)
    risk_model.fit(X_scaled, df["Flight_Risk"])
    
    # 3. HJERNE FOR LØNN (Regressor)
    print("   -> Trener Lønns-kalkulator...")
    salary_model = RandomForestRegressor(n_estimators=100, random_state=42)
    salary_model.fit(X_scaled, df["Markedsverdi"])
    
    # Pakk alt
    # Vi prøver å bevare Knowledge Graph fra forrige versjon hvis den finnes
    existing_graph = {}
    try:
        with open("aivory_model.pkl", "rb") as f:
            old = pickle.load(f)
            if isinstance(old, dict): existing_graph = old.get("skill_graph", {})
    except: pass
    
    package = {
        "hire_model": hire_model,
        "risk_model": risk_model,
        "salary_model": salary_model,
        "scaler": scaler,
        "skill_graph": existing_graph,
        "version": "Pro-Industry-v1"
    }

    with open("aivory_model.pkl", "wb") as f:
        pickle.dump(package, f)
    
    print("💾 Aivory er nå en bransje-ekspert!")

if __name__ == "__main__":
    train_pro_models()
