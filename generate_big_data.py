import pandas as pd
import random

def generate_industry_data(num_samples=10000):
    print(f"🏭 Starter Aivory Data Factory: Genererer {num_samples} profiler fordelt på bransjer...")
    
    data = []
    
    # Bransje-profiler (Hva kreves for å bli ansatt?)
    # Format: (Bransje, IQ-krav, Struktur, Ekstroversjon, Omgjengelighet, Lønnsnivå)
    industries = {
        "IT":     {"iq": (110, 140), "str": (5, 9), "ext": (2, 7), "agr": (4, 8), "pay": (600000, 1200000)},
        "Salg":   {"iq": (95, 120),  "str": (6, 9), "ext": (8, 10), "agr": (6, 9), "pay": (500000, 1500000)}, # Høy bonus
        "Helse":  {"iq": (100, 125), "str": (8, 10), "ext": (4, 8), "agr": (8, 10), "pay": (450000, 900000)},
        "Finans": {"iq": (105, 130), "str": (9, 10), "ext": (4, 7), "agr": (5, 8), "pay": (550000, 1100000)},
        "Bygg":   {"iq": (90, 115),  "str": (7, 10), "ext": (3, 7), "agr": (5, 8), "pay": (450000, 800000)}
    }
    
    for _ in range(num_samples):
        # 1. Velg tilfeldig bransje
        bransje = random.choice(list(industries.keys()))
        profile = industries[bransje]
        
        # 2. Generer kandidatens egenskaper
        # Vi legger til +/- tilfeldighet så ikke alle er like
        iq = random.randint(profile["iq"][0]-10, profile["iq"][1]+10)
        struktur = random.randint(1, 10)
        driv = random.randint(1, 10)
        samarbeid = random.randint(1, 10)
        ekstroversjon = random.randint(1, 10)
        
        erfaring = random.randint(0, 25)
        skill_match = random.randint(20, 100)
        jobb_hopping = random.randint(0, 5)
        
        # 3. Beregn om de passer i BRANSJEN (Fasit)
        score = 0
        
        # Bransjespesifikke krav
        if bransje == "IT":
            score += (iq * 0.4) + (skill_match * 0.4) + (driv * 2)
        elif bransje == "Salg":
            score += (ekstroversjon * 5) + (driv * 5) + (erfaring * 2)
        elif bransje == "Helse":
            score += (samarbeid * 6) + (struktur * 4) + (skill_match * 0.3)
        elif bransje == "Finans":
            score += (struktur * 8) + (iq * 0.3)
        elif bransje == "Bygg":
            score += (struktur * 5) + (erfaring * 3) + (samarbeid * 2)
            
        # Normaliser score for ansettelse
        threshold = 60 # En slags basisverdi
        hired = 1 if score > threshold + random.randint(-20, 20) else 0
        
        # 4. Beregn Retention (Hvor lenge blir de?)
        # IT-folk bytter ofte jobb (lavere retention), Helse er mer stabilt
        base_retention = 36 if bransje in ["Helse", "Bygg"] else 24
        retention = base_retention - (jobb_hopping * 6) + (erfaring * 0.5)
        flight_risk = 1 if retention < 18 else 0
        
        # 5. Beregn Markedsverdi
        base_pay = random.randint(*profile["pay"])
        markedsverdi = base_pay + (erfaring * 20000)
        
        # Mapping av bransje til ID for ML (Maskinlæring liker tall)
        b_id = ["IT", "Salg", "Helse", "Finans", "Bygg"].index(bransje)

        data.append([b_id, erfaring, struktur, driv, samarbeid, ekstroversjon, skill_match, jobb_hopping, iq, hired, flight_risk, markedsverdi])

    df = pd.DataFrame(data, columns=["Bransje_ID", "Erfaring", "Struktur", "Driv", "Samarbeid", "Ekstroversjon", "Skill_Match", "Jobb_Hopping", "IQ", "Hired", "Flight_Risk", "Markedsverdi"])
    df.to_csv("training_big_data.csv", index=False)
    print(f"✅ Generert {num_samples} linjer med bransjespesifikk logikk.")
    print("   AI-en vil nå forstå at en stille person kan være en genial utvikler, men en dårlig selger.")

if __name__ == "__main__":
    generate_industry_data()
