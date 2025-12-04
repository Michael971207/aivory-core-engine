import pandas as pd
import random

def generate_smart_data(num_samples=3000):
    data = []
    print(f"Genererer {num_samples} avanserte profiler med lojalitets-data...")
    
    # Arketyper: (Navn, Erfaring, Struktur, Driv, Samarbeid, Skill, JobbHopping, Ansettelse_Sannsynlighet)
    # JobbHopping = Antall jobber de har hatt siste 5 år (0-5)
    archetypes = [
        ("Loyal Senior",    (8, 20), (7, 10), (4, 7),  (6, 10), (70, 100), (0, 1), 0.90),
        ("Job Hopper",      (2, 6),  (3, 7),  (8, 10), (5, 9),  (80, 100), (3, 5), 0.70), # Flink men flyktig
        ("Junior Stable",   (0, 3),  (6, 9),  (5, 8),  (6, 9),  (40, 70),  (0, 1), 0.60),
        ("Toxic Expert",    (5, 15), (8, 10), (8, 10), (1, 3),  (90, 100), (2, 4), 0.20),
        ("Average Joe",     (3, 8),  (4, 7),  (4, 7),  (4, 7),  (40, 70),  (1, 3), 0.40)
    ]
    
    for _ in range(num_samples):
        type_data = random.choice(archetypes)
        exp_r, str_r, dri_r, sam_r, skill_r, hop_r, hire_prob = type_data[1:]
        
        erfaring = random.randint(*exp_r)
        struktur = random.randint(*str_r)
        driv = random.randint(*dri_r)
        samarbeid = random.randint(*sam_r)
        skill_match = random.randint(*skill_r)
        jobb_hops = random.randint(*hop_r) # Ny faktor!
        
        # 1. Mål: Ble de ansatt? (Klassifisering)
        hired = 1 if random.random() < hire_prob else 0
        
        # 2. Mål: Hvor lenge ble de? (Regresjon - Antall måneder)
        # Formel: Struktur hjelper, JobbHopping skader, Driv kan gjøre dem rastløse
        base_months = 24
        retention = base_months + (struktur * 2) - (jobb_hops * 8) - (driv * 0.5) + (erfaring * 0.5)
        retention = max(3, retention + random.randint(-5, 5)) # Minst 3 mnd, litt tilfeldighet
        
        data.append([erfaring, struktur, driv, samarbeid, skill_match, jobb_hops, hired, int(retention)])

    df = pd.DataFrame(data, columns=["Erfaring", "Struktur", "Driv", "Samarbeid", "Skill_Match", "Jobb_Hopping", "Hired", "Retention_Months"])
    df.to_csv("training_history.csv", index=False)
    print("✅ Data generert: Inkluderer nå 'Jobb Hopping' og forventet tid i selskapet.")

if __name__ == "__main__":
    generate_smart_data()
