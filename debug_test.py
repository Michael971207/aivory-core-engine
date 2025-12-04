import requests
import json

# URL til din lokale server
url = "http://127.0.0.1:8000/predict_hiring"

# Test-kandidater
candidates = [
    {
        "Navn": "Kandidat A (Papegøye)",
        "Erfaring": 5, "Struktur": 5, "Driv": 5, "Samarbeid": 5, "Skill_Match": 80,
        "Soknadstekst": "Python. Machine Learning. AI. Koding. Data."
    },
    {
        "Navn": "Kandidat B (Ekspert)",
        "Erfaring": 5, "Struktur": 5, "Driv": 5, "Samarbeid": 5, "Skill_Match": 80,
        "Soknadstekst": "Jeg har bygget avanserte nevrale nettverk og trives med å løse komplekse problemer i backend. Jeg tar eierskap til leveransene mine."
    }
]

print(f"--- TESTER KOBLING MOT {url} ---")

for cand in candidates:
    print(f"\nSender: {cand['Navn']}...")
    try:
        # Sender request til API-et
        response = requests.post(url, json=cand)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ SUKSESS!")
            print(f"   Anbefaling: {data['anbefaling']}")
            print(f"   Total Score: {data['total_score']}%")
            # Sjekk om analysen finnes før vi printer
            if 'analyse' in data:
                print(f"   -> Mening-Match: {data['analyse'].get('semantisk_match', 0)}%")
        else:
            print(f"❌ FEIL (Kode {response.status_code}):")
            print(response.text) # Her får vi se nøyaktig hva serveren klager på!
            
    except Exception as e:
        print(f"❌ KRITISK FEIL: {e}")
        print("   Kjører serveren i det andre vinduet?")

print("\n--- TEST FERDIG ---")
