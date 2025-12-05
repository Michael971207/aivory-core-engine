import sqlite3

def build_soft_skill_db():
    print("🧠 Bygger database for Myke Ferdigheter (Soft Skills)...")
    
    conn = sqlite3.connect('aivory_logs.db')
    c = conn.cursor()
    
    # 1. Tabell
    c.execute("DROP TABLE IF EXISTS soft_skills")
    c.execute('''CREATE TABLE soft_skills 
                 (bransje TEXT, egenskap TEXT, vekting INTEGER)''')
    
    # 2. DATASETT (Hva kreves mentalt?)
    skills = [
        # IT & Tech (Trenger hoder som tåler frustrasjon)
        ("IT", "Problemløsning", 10),
        ("IT", "Nysgjerrighet", 9),
        ("IT", "Autonomi", 8),
        ("IT", "Analytisk", 9),
        
        # Salg (Trenger folk som tåler avvisning)
        ("Salg", "Utholdenhet", 10),
        ("Salg", "Overtalelse", 9),
        ("Salg", "Selvsikkerhet", 8),
        ("Salg", "Relasjonsbygging", 9),
        
        # Helse (Trenger folk som bryr seg)
        ("Helse", "Empati", 10),
        ("Helse", "Tålmodighet", 9),
        ("Helse", "Stressmestring", 10),
        ("Helse", "Samarbeid", 8),
        
        # Ledelse
        ("Leder", "Beslutningsevne", 10),
        ("Leder", "Integritet", 9),
        ("Leder", "Strategisk", 9),
        
        # Service / Butikk
        ("Service", "Positivitet", 10),
        ("Service", "Fleksibilitet", 8),
        ("Service", "Punktlighet", 9)
    ]
    
    print(f"   -> Importerer {len(skills)} psykologiske koblinger...")
    
    for bransje, egenskap, vekt in skills:
        c.execute("INSERT INTO soft_skills VALUES (?, ?, ?)", (bransje, egenskap, vekt))
        
    conn.commit()
    conn.close()
    print("✅ Soft Skill Database er aktiv!")

if __name__ == "__main__":
    build_soft_skill_db()
