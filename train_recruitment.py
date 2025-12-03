import pandas as pd
import time
import datetime
import os

def train_recruitment_brain():
    print("--- STARTER TRENING PÅ REKRUTTERINGSDATA ---")
    
    # 1. Last inn data
    try:
        df = pd.read_csv('recruitment_data.csv')
        print(f"Lastet inn {len(df)} kandidat-profiler for trening.")
    except FileNotFoundError:
        print("Feil: Finner ikke recruitment_data.csv")
        return

    # 2. Simulerer trening (Her ville din dype logikk vært)
    print("Analyserer ferdigheter og kultur-match...")
    time.sleep(2) # Tenkepause
    
    for index, row in df.iterrows():
        print(f"Trener på profil: {row['rolle']} - Match: {row['kultur_match']}")

    # 3. Lagre oppdatert kunnskap (Simulert ved å oppdatere en logg)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Oppdaterer en 'model_state' fil for å vise at endring har skjedd
    with open("model_status.txt", "a") as f:
        f.write(f"Rekrutteringstrening fullført: {timestamp}\n")
    
    print("--- TRENING FULLFØRT OG MODELL OPPDATERT ---")

if __name__ == "__main__":
    train_recruitment_brain()
