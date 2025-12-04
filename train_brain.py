import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor # To typer skog!
from sklearn.preprocessing import StandardScaler

def train_dual_brain():
    print("🧠 Trener Aivory Dual-Core Engine...")
    
    df = pd.read_csv("training_history.csv")
    
    # Input data (X)
    X = df[["Erfaring", "Struktur", "Driv", "Samarbeid", "Skill_Match", "Jobb_Hopping"]]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # --- HJERNE 1: ANSETTELSE (Ja/Nei) ---
    y_hire = df["Hired"]
    hire_model = RandomForestClassifier(n_estimators=100, random_state=42)
    hire_model.fit(X_scaled, y_hire)
    print("✅ Ansettelses-hjerne trent.")
    
    # --- HJERNE 2: LOJALITET (Antall Måneder) ---
    # Vi trener kun på de som faktisk ble ansatt (gir mest mening)
    hired_df = df[df["Hired"] == 1]
    X_ret = hired_df[["Erfaring", "Struktur", "Driv", "Samarbeid", "Skill_Match", "Jobb_Hopping"]]
    y_ret = hired_df["Retention_Months"]
    
    # Skaler på nytt for denne gruppen
    X_ret_scaled = scaler.transform(X_ret)
    
    retention_model = RandomForestRegressor(n_estimators=100, random_state=42)
    retention_model.fit(X_ret_scaled, y_ret)
    print("✅ Lojalitets-hjerne trent.")
    
    # Pakk alt i én fil
    package = {
        "hire_model": hire_model,
        "retention_model": retention_model,
        "scaler": scaler,
        "version": "Dual-Core 11.0"
    }

    with open("aivory_model.pkl", "wb") as f:
        pickle.dump(package, f)
    
    print("💾 Lagret som 'aivory_model.pkl'")

if __name__ == "__main__":
    train_dual_brain()
