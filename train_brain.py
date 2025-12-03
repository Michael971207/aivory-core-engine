import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def train_model():
    print("--- STARTER TRENING AV AI-MODELL ---")
    try:
        df = pd.read_csv("training_history.csv")
    except FileNotFoundError:
        print("Mangler data!")
        return

    X = df[["Erfaring", "Struktur", "Driv", "Samarbeid", "Skill_Match"]]
    y = df["Hired"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    print(f"Modell trent ferdig! Nøyaktighet: {accuracy * 100:.2f}%")

    with open("aivory_model.pkl", "wb") as f:
        pickle.dump(model, f)
    
    print("Hjernen er lagret som 'aivory_model.pkl'.")

if __name__ == "__main__":
    train_model()
