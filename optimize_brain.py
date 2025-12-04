import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.preprocessing import StandardScaler

# --- MODELLENE VI SKAL TESTE ---
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neural_network import MLPClassifier

def run_ai_lab():
    print("\n🔬 VELKOMMEN TIL AIVORY AI LAB 🔬")
    print("Vi arrangerer en turnering for å finne den optimale hjernen.")
    print("-" * 50)

    # 1. Last inn og forbered data
    try:
        df = pd.read_csv("training_history.csv")
    except FileNotFoundError:
        print("Mangler data! Kjør generate_history.py først.")
        return

    X = df[["Erfaring", "Struktur", "Driv", "Samarbeid", "Skill_Match"]]
    y = df["Hired"]

    # VIKTIG: Nevrale nettverk krever at dataene er "skalert" (tall mellom 0 og 1)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Del i trening og test
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    # 2. Definer konkurrentene
    models = {
        "Random Forest 🌲": RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42),
        "Gradient Boost 🚀": GradientBoostingClassifier(learning_rate=0.1, n_estimators=100, random_state=42),
        "Nevralt Nettverk 🧠": MLPClassifier(hidden_layer_sizes=(50, 25), max_iter=1000, random_state=42)
    }

    best_model = None
    best_score = 0
    best_name = ""

    # 3. Start turneringen
    for name, model in models.items():
        print(f"\nTrener {name}...")
        model.fit(X_train, y_train)
        
        preds = model.predict(X_test)
        acc = accuracy_score(y_test, preds)
        prec = precision_score(y_test, preds)
        
        print(f"   -> Nøyaktighet: {acc*100:.2f}%")
        print(f"   -> Presisjon:   {prec*100:.2f}%") # Hvor ofte har den rett når den sier JA?

        # Vi velger vinneren basert på nøyaktighet
        if acc > best_score:
            best_score = acc
            best_model = model
            best_name = name

    # 4. Kår en vinner
    print("\n" + "="*50)
    print(f"🏆 VINNEREN ER: {best_name}")
    print(f"   Med score: {best_score*100:.2f}%")
    print("="*50)

    # 5. Lagre vinneren (Inkludert skaleringen, den må vi huske!)
    # Vi pakker både modellen og skaleringen sammen i en liste
    package = {
        "model": best_model,
        "scaler": scaler,
        "type": best_name
    }

    with open("aivory_model.pkl", "wb") as f:
        pickle.dump(package, f)
    
    print(f"✅ Vinner-modellen er lagret og klar til bruk i API-et.")

if __name__ == "__main__":
    run_ai_lab()
