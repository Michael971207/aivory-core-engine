import pandas as pd
import pickle
import matplotlib.pyplot as plt

def explain_model_logic():
    print("\n--- AIVORY INSIGHTS: HVORDAN TENKER AI-EN? ---")
    
    # 1. Last inn hjernen
    try:
        with open("aivory_model.pkl", "rb") as f:
            model = pickle.load(f)
    except FileNotFoundError:
        print("Finner ikke modellen!")
        return

    # 2. Hent ut hva den bryr seg om (Feature Importance)
    feature_names = ["Erfaring", "Struktur", "Driv", "Samarbeid", "Skill_Match"]
    importances = model.feature_importances_

    # 3. Lag en fin tabell
    df_importance = pd.DataFrame({
        "Egenskap": feature_names,
        "Viktighet": importances
    }).sort_values(by="Viktighet", ascending=False)

    print(f"{'EGENSKAP':<15} | {'VIKTIGHET (0-100%)':<20}")
    print("-" * 40)
    
    for index, row in df_importance.iterrows():
        prosent = row['Viktighet'] * 100
        bar = "█" * int(prosent / 5) # Lager en liten grafikk
        print(f"{row['Egenskap']:<15} | {prosent:.1f}% {bar}")

    print("-" * 40)
    
    top_feature = df_importance.iloc[0]['Egenskap']
    print(f"KONKLUSJON: Denne AI-modellen ser mest etter '{top_feature.upper()}'.")
    print("Dette beviser at AI-en ikke bare gjetter, men har lært en strategi.")

if __name__ == "__main__":
    explain_model_logic()
