import pandas as pd
import random

first_names = ["Ola", "Kari", "Ali", "Pål", "Lisa", "Erik", "Sara", "Mohamed", "Ingrid", "Lars", "Sofia", "Jakob"]
last_names = ["Hansen", "Johansen", "Olsen", "Larsen", "Andersen", "Pedersen", "Nilsen", "Berg"]

# Vi utvider ferdighets-poolen til å dekke flere bransjer
tech_skills = ["Python", "AI", "Java", "React", "Cloud", "SQL"]
finance_skills = ["Excel", "Regnskap", "Økonomi", "Analyse", "Matematikk"]
creative_skills = ["Photoshop", "Figma", "Design", "Video", "SoMe"]
all_skills = tech_skills + finance_skills + creative_skills

def generate_bulk_data(num_applicants=500):
    data = []
    print(f"Genererer {num_applicants} varierte kandidater (Tech, Finans, Kreativ)...")
    
    for i in range(num_applicants):
        real_name = f"{random.choice(first_names)} {random.choice(last_names)}"
        kandidat_id = f"CAND-{random.randint(10000, 99999)}"
        
        # Vi lager en "profiltype" for å sikre at ferdighetene henger litt sammen
        profile_type = random.choice(["tech", "finance", "creative", "mixed"])
        
        if profile_type == "tech":
            base_skills = random.sample(tech_skills, k=3)
        elif profile_type == "finance":
            base_skills = random.sample(finance_skills, k=3)
        elif profile_type == "creative":
            base_skills = random.sample(creative_skills, k=3)
        else:
            base_skills = random.sample(all_skills, k=4) # En generalist
            
        skills_str = ", ".join(base_skills)
        erfaring = random.randint(0, 20)
        
        # Personlighet
        struktur = random.randint(1, 10)
        driv = random.randint(1, 10)
        samarbeid = random.randint(1, 10)
        
        data.append([kandidat_id, real_name, skills_str, erfaring, struktur, driv, samarbeid])
    
    df = pd.DataFrame(data, columns=["ID", "Faktisk_Navn", "Ferdigheter", "Erfaring", "Struktur", "Driv", "Samarbeid"])
    df.to_csv("bulk_applicants.csv", index=False)
    print(f"Suksess! 500 kandidater klare i basen.")

if __name__ == "__main__":
    generate_bulk_data(500)
