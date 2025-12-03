import pandas as pd
import pickle

def predict_new_candidates():
    print("\n--- AIVORY LIVE PREDICTION ---")
    try:
        with open("aivory_model.pkl", "rb") as f:
            model = pickle.load(f)
    except FileNotFoundError:
        print("Finner ikke hjernen!")
        return

    new_candidates = [
        {"Navn": "Kandidat A (Junior)", "Erfaring": 1, "Struktur": 4, "Driv": 9, "Samarbeid": 8, "Skill_Match": 40},
        {"Navn": "Kandidat B (Senior)", "Erfaring": 8, "Struktur": 9, "Driv": 7, "Samarbeid": 6, "Skill_Match": 90},
        {"Navn": "Kandidat C (Kaos)",   "Erfaring": 5, "Struktur": 2, "Driv": 5, "Samarbeid": 2, "Skill_Match": 80},
    ]
    
    df_new = pd.DataFrame(new_candidates)
    features = df_new[["Erfaring", "Struktur", "Driv", "Samarbeid", "Skill_Match"]]

    predictions = model.predict(features)
    probabilities = model.predict_proba(features)

    print(f"{'NAVN':<20} | {'ANSETT?':<10} | {'SIKKERHET':<10}")
    print("-" * 45)
    
    for i, candidate in df_new.iterrows():
        ansett = "JA" if predictions[i] == 1 else "NEI"
        prosent = probabilities[i][1] * 100 
        print(f"{candidate['Navn']:<20} | {ansett:<10} | {prosent:.1f}%")

if __name__ == "__main__":
    predict_new_candidates()
