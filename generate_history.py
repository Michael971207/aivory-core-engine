import pandas as pd
import random

def generate_training_data(num_samples=1000):
    data = []
    print(f"Genererer {num_samples} historiske saker for trening...")

    for _ in range(num_samples):
        erfaring = random.randint(0, 15)
        struktur = random.randint(1, 10)
        driv = random.randint(1, 10)
        samarbeid = random.randint(1, 10)
        skill_match = random.randint(20, 100)

        # Fasit-logikk (Hvem ble ansatt?)
        score = (erfaring * 3) + (struktur * 4) + (skill_match * 0.5)
        threshold = 60 + random.randint(-10, 10) 
        hired = 1 if score > threshold else 0

        data.append([erfaring, struktur, driv, samarbeid, skill_match, hired])

    df = pd.DataFrame(data, columns=["Erfaring", "Struktur", "Driv", "Samarbeid", "Skill_Match", "Hired"])
    df.to_csv("training_history.csv", index=False)
    print("Suksess! Historiske data lagret i 'training_history.csv'.")

if __name__ == "__main__":
    generate_training_data()
