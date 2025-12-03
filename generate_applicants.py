import pandas as pd
import random

first_names = ["Ola", "Kari", "Ali", "Pål", "Lisa", "Erik", "Sara", "Mohamed", "Ingrid", "Lars", "Sofia", "Jakob", "Nora", "Emil", "Magnus", "Ida"]
last_names = ["Hansen", "Johansen", "Olsen", "Larsen", "Andersen", "Pedersen", "Nilsen", "Berg", "Haugen", "Hagen", "Solberg", "Vik"]
skills_pool = ["Python", "Java", "C++", "Excel", "PowerPoint", "Ledelse", "Salg", "Markedsføring", "AI", "Machine Learning", "React", "SQL", "Kundeservice", "HR", "Jira", "Azure", "AWS"]
universities = ["NTNU", "UiO", "BI", "Høyskolen Kristiania", "NHH", "Ingen utdanning", "Master i utlandet"]

def generate_bulk_data(num_applicants=250):
    data = []
    print(f"Genererer {num_applicants} ANONYME kandidatprofiler...")
    
    for i in range(num_applicants):
        # Vi genererer navn, men disse skal skjules i prosessen
        real_name = f"{random.choice(first_names)} {random.choice(last_names)}"
        
        # Generer en unik ID (Dette er det eneste selskapet får se)
        kandidat_id = f"KANDIDAT-{random.randint(1000, 9999)}"
        
        # CV Data
        num_skills = random.randint(2, 6)
        skills = ", ".join(random.sample(skills_pool, num_skills))
        erfaring = random.randint(0, 15)
        utdanning = random.choice(universities)
        
        # PERSONLIGHETSDATA (1-10)
        struktur = random.randint(1, 10)
        driv = random.randint(1, 10)
        samarbeid = random.randint(1, 10)
        
        data.append([kandidat_id, real_name, skills, erfaring, utdanning, struktur, driv, samarbeid])
    
    df = pd.DataFrame(data, columns=["ID", "Faktisk_Navn", "Ferdigheter", "Erfaring", "Utdanning", "Struktur", "Driv", "Samarbeid"])
    df.to_csv("bulk_applicants.csv", index=False)
    print(f"Suksess! Database opprettet. Navn ligger lagret, men skal skjules.")

if __name__ == "__main__":
    generate_bulk_data(250)
