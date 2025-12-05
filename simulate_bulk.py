import requests
import random
import time

API_URL = "http://127.0.0.1:8000"

# Definer noen jobber vi simulerer søkere til
JOBS = {
    "Senior AI Utvikler": "Vi søker en ekspert på Python, Machine Learning og AI.",
    "Salgssjef": "Vi trenger en energisk leder som kan drive nysalg og booke møter.",
    "Sykepleier": "Vi søker helsepersonell med autorisasjon og erfaring fra sykehus."
}

# Hjelpefunksjon for å lage tilfeldig tekst
def generate_text(role):
    good_words = {
        "Senior AI Utvikler": ["python", "ai", "machine learning", "backend", "fullstack", "data science"],
        "Salgssjef": ["salg", "prospektering", "closing", "møter", "budsjett", "crm"],
        "Sykepleier": ["omsorg", "medisiner", "pasient", "sykehus", "autorisasjon", "vakt"]
    }
    bad_words = ["jeg vet ikke", "kanskje", "prøve", "usikker", "ingen erfaring"]
    
    # 20% sjanse for en "super-kandidat" (bruker gode ord)
    if random.random() < 0.2:
        words = good_words.get(role, [])
        return f"Jeg er en ekspert innen {', '.join(words)}. Jeg har lang erfaring og leverer resultater."
    else:
        return f"Hei, jeg søker på jobben som {role}. Jeg er {random.choice(bad_words)}."

print("🚀 Starter massesimulering av 200 søkere...")

names = ["Ola", "Kari", "Per", "Lise", "Anders", "Bjørn", "Eva", "Nora", "Jakob", "Sofie"]
last_names = ["Hansen", "Johansen", "Olsen", "Larsen", "Berg", "Nilsen", "Pedersen"]

for i in range(200):
    role = random.choice(list(JOBS.keys()))
    desc = JOBS[role]
    name = f"{random.choice(names)} {random.choice(last_names)} {i}"
    
    # Lag en tilfeldig profil
    payload = {
        "Navn": name,
        "Erfaring": random.randint(0, 20),
        "Struktur": random.randint(1, 10),
        "Driv": random.randint(1, 10),
        "Samarbeid": random.randint(1, 10),
        "Skill_Match": random.randint(30, 100),
        "Soknadstekst": generate_text(role),
        "StillingTittel": role,
        "JobbBeskrivelse": desc,
        "Jobb_Hopping": random.randint(0, 5),
        "Lonnskrav": random.randint(500000, 1500000)
    }
    
    try:
        # Send til API (Hjernen vurderer hver enkelt)
        requests.post(f"{API_URL}/predict_hiring", json=payload)
        if i % 10 == 0: print(f"   -> Behandlet {i} søkere...")
    except:
        print("❌ Feil: Serveren kjører ikke!")
        break

print("✅ Ferdig! 200 kandidater er analysert og lagret i databasen.")
