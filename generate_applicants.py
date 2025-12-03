import pandas as pd
import random

# Vi bruker forhåndsdefinerte lister så vi slipper eksterne bibliotek
first_names = ["Ola", "Kari", "Ali", "Pål", "Lisa", "Erik", "Sara", "Mohamed", "Ingrid", "Lars", "Sofia", "Jakob", "Nora", "Emil"]
last_names = ["Hansen", "Johansen", "Olsen", "Larsen", "Andersen", "Pedersen", "Nilsen", "Berg", "Haugen", "Hagen"]
skills_pool = ["Python", "Java", "C++", "Excel", "PowerPoint", "Ledelse", "Salg", "Markedsføring", "AI", "Machine Learning", "React", "SQL", "Kundeservice", "HR", "Jira"]
universities = ["NTNU", "UiO", "BI", "Høyskolen Kristiania", "NHH", "Ingen utdanning", "Master i utlandet"]

def generate_bulk_data(num_applicants=250):
    data = []
    print(f"Genererer {num_applicants} søkere til databasen (Uten eksterne bibliotek)...")
    
    for _ in range(num_applicants):
        # 1. Lag navn
        navn = f"{random.choice(first_names)} {random.choice(last_names)}"
        
        # 2. Generer ferdigheter (tilfeldig 2 til 6 ferdigheter)
        num_skills = random.randint(2, 6)
        skills = ", ".join(random.sample(skills_pool, num_skills))
        
        # 3. Erfaring (0 til 15 år)
        erfaring = random.randint(0, 15)
        
        # 4. Utdanning
        utdanning = random.choice(universities)
        
        data.append([navn, skills, erfaring, utdanning])
    
    # Lagre filen
    df = pd.DataFrame(data, columns=["Navn", "Ferdigheter", "Erfaring", "Utdanning"])
    df.to_csv("bulk_applicants.csv", index=False)
    print(f"Suksess! 'bulk_applicants.csv' er opprettet med {len(df)} kandidater.")

if __name__ == "__main__":
    generate_bulk_data(250)
