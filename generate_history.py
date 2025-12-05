import pandas as pd
import random

def generate_psych_data(num_samples=5000):
    print("🧠 Genererer psykometriske data (Big 5 + IQ + Kultur)...")
    
    data = []
    
    # Vi definerer arketyper for å skape realistiske mønstre
    # Format: (Rolle, IQ_range, Conscientiousness, Extraversion, Agreeableness, Culture, Hire_Prob)
    archetypes = [
        ("Star Developer", (115, 140), (7, 10), (2, 6), (4, 8), "Innovation", 0.95),
        ("Social Sales",   (100, 125), (5, 8),  (8, 10), (7, 10), "Competition", 0.90),
        ("Steady Admin",   (95, 115),  (9, 10), (3, 6),  (6, 9),  "Stability",   0.85),
        ("Toxic Genius",   (130, 150), (8, 10), (5, 9),  (1, 3),  "Innovation",  0.30), # Smart men slem
        ("Lazy Talent",    (110, 130), (1, 3),  (4, 7),  (5, 8),  "Flexibility", 0.20), # Smart men lat
        ("Culture Clash",  (100, 120), (6, 9),  (5, 8),  (5, 8),  "Stability",   0.10), # Feil kultur
        ("Average Joe",    (90, 110),  (4, 7),  (4, 7),  (4, 7),  "Stability",   0.40)
    ]
    
    culture_map = {"Innovation": 1, "Stability": 2, "Competition": 3, "Flexibility": 4}

    for _ in range(num_samples):
        # Velg en arketype
        arch = random.choice(archetypes)
        iq_r, con_r, ext_r, agr_r, cult, hire_prob = arch[1:]
        
        # Generer verdier
        iq = random.randint(*iq_r)
        
        # Big 5 (1-10)
        conscientiousness = random.randint(*con_r) # Planmessighet (Viktigst for jobb)
        extraversion = random.randint(*ext_r)      # Utadvendthet
        agreeableness = random.randint(*agr_r)     # Omgjengelighet (Viktig for team)
        openness = random.randint(3, 9)            # Åpenhet for erfaring
        neuroticism = random.randint(1, 6)         # Følelsesmessig stabilitet (Lav er bra)
        
        culture_val = culture_map[cult]
        
        # CV-data (blandet inn)
        erfaring = random.randint(0, 15)
        skill_match = random.randint(40, 100)
        
        # Logikk for ansettelse:
        # Høy IQ + Høy Conscientiousness = Gull
        # Lav Agreeableness = Risiko
        score_sum = (iq * 0.5) + (conscientiousness * 5) + (agreeableness * 3) + (skill_match * 0.5)
        
        # Simuler ansettelse
        hired = 1 if random.random() < hire_prob else 0
        
        # Simuler "Retention" (Hvor lenge blir de?)
        # Høy neuroticism eller mismatch i kultur = Slutter fort
        retention = 24
        if neuroticism > 7: retention -= 10
        if culture_val == 3: retention -= 5 # Konkurransefolk bytter ofte jobb
        retention = max(2, retention + random.randint(-5, 10))

        data.append([erfaring, skill_match, iq, conscientiousness, extraversion, agreeableness, openness, neuroticism, culture_val, hired, retention])

    df = pd.DataFrame(data, columns=["Erfaring", "Skill_Match", "IQ", "Conscientiousness", "Extraversion", "Agreeableness", "Openness", "Neuroticism", "Culture_ID", "Hired", "Retention"])
    df.to_csv("training_history.csv", index=False)
    print(f"✅ Genererte {num_samples} psykometriske profiler.")
    print("   Dataset inneholder nå IQ, Big 5 Personlighet og Kultur-verdier.")

if __name__ == "__main__":
    generate_psych_data()
