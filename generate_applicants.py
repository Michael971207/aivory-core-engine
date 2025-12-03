import pandas as pd
import random

first_names = ["Ola", "Kari", "Ali", "Pål", "Lisa", "Erik", "Sara", "Mohamed", "Ingrid", "Lars", "Sofia", "Jakob", "Nora", "Emil", "Magnus", "Ida"]
last_names = ["Hansen", "Johansen", "Olsen", "Larsen", "Andersen", "Pedersen", "Nilsen", "Berg", "Haugen", "Hagen", "Solberg", "Vik"]
skills_pool = ["Python", "Java", "C++", "Excel", "PowerPoint", "Ledelse", "Salg", "Markedsføring", "AI", "Machine Learning", "React", "SQL", "Kundeservice", "HR", "Jira", "Azure", "AWS"]
universities = ["NTNU", "UiO", "BI", "Høyskolen Kristiania", "NHH", "Ingen utdanning", "Master i utlandet"]

def generate_bulk_data(num_applicants=250):
    data = []
    print(f"Genererer {num_applicants} kandidater med CV og PERSONLIGHETSTEST...")
    
    for _ in range(num_applicants):
        navn = f"{random.choice(first_names)} {random.choice(last_names)}"
        
        # CV Data
        num_skills = random.randint(2, 6)
        skills = ", ".join(random.sample(skills_pool, num_skills))
        erfaring = random.randint(0, 15)
        utdanning = random.choice(universities)
        
        # PERSONLIGHETSDATA (Skala 1-10)
        # Dette simulerer resultatene fra testene vi skal bygge senere
        struktur = random.randint(1, 10)  # Conscientiousness
        driv = random.randint(1, 10)      # Energy/Ambition
        samarbeid = random.randint(1, 10) # Agreeableness
        
        data.append([navn, skills, erfaring, utdanning, struktur, driv, samarbeid])
    
    df = pd.DataFrame(data, columns=["Navn", "Ferdigheter", "Erfaring", "Utdanning", "Struktur", "Driv", "Samarbeid"])
    df.to_csv("bulk_applicants.csv", index=False)
    print(f"Suksess! Database oppdatert med personlighetsprofiler.")

if __name__ == "__main__":
    generate_bulk_data(250)
