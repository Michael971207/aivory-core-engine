import csv
import random

# Vi lager noen lister med "byggeklosser" for å generere data
roles = ["Frontend Utvikler", "Salgssjef", "Lagerarbeider", "Kundeservice", "CTO", "Prosjektleder"]
skills = ["Python", "React", "Salg", "Truckførerbevis", "Ledelse", "Excel", "Maling", "Sveising"]
experiences = ["Nyutdannet", "2 års erfaring", "10 års erfaring", "Senior", "Lærling"]

print("🏭 Starter masseproduksjon av treningsdata...")

new_data = []

for i in range(50): # Vi lager 50 nye eksempler
    role = random.choice(roles)
    skill = random.choice(skills)
    exp = random.choice(experiences)
    
    # Vi lager en tilfeldig CV og Jobb
    cv = f"{role} med {exp}. Kan {skill}."
    job = f"Søker etter {role} som kan {skill}."
    
    # Enkel logikk: Hvis ferdigheten matcher, er det en god match (forenklet for demo)
    score = 0.9 if skill in job else 0.2
    reasoning = f"AUTO-GENERERT: Sjekket om {skill} var relevant for {role}."

    new_data.append([cv, job, score, reasoning])

# Legg til i CSV-filen
with open("training_data.csv", "a", newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(new_data)

print(f"✅ Ferdig! La til 50 nye eksempler i 'training_data.csv'.")
print("👉 Kjør './publish_brain.sh' for å trene modellen på disse nye dataene.")
