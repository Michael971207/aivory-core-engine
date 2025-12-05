import sqlite3

def build_question_bank():
    print("📚 Genererer Aivory Fag-Database...")
    
    conn = sqlite3.connect('aivory_logs.db')
    c = conn.cursor()
    
    # 1. Lag tabell for spørsmål
    c.execute("DROP TABLE IF EXISTS questions") # Start på nytt for å unngå duplikater
    c.execute('''CREATE TABLE questions 
                 (id INTEGER PRIMARY KEY, 
                  kategori TEXT, 
                  nokkelord TEXT, 
                  sporsmal TEXT, 
                  vanskelighetsgrad INTEGER)''')
    
    # 2. DATASETTET (Her legger vi inn fagkunnskapen)
    # Format: (Kategori, Nøkkelord som trigger spørsmålet, Spørsmålet, Vanskelighetsgrad 1-3)
    dataset = [
        # --- HELSE ---
        ("Helse", "sykepleier", "Hvordan prioriterer du pasienter i et akuttmottak (triage)?", 3),
        ("Helse", "sykepleier", "Beskriv prosedyren for sikker utdeling av medisiner.", 2),
        ("Helse", "helse", "Hvordan håndterer du taushetsplikt i møte med pårørende?", 1),
        ("Helse", "lege", "Hva er de viktigste symptomene på sepsis du ser etter?", 3),
        ("Helse", "omsorg", "Hvordan bygger du tillit til en pasient som er redd?", 1),
        
        # --- IT & UTVIKLING ---
        ("IT", "python", "Hva er forskjellen på en liste og en tuple, og når bruker du hva?", 2),
        ("IT", "python", "Hvordan håndterer du minnelekkasje i et stort script?", 3),
        ("IT", "react", "Forklar livssyklusen til en React-komponent.", 2),
        ("IT", "sikkerhet", "Hvordan beskytter du et API mot SQL Injection?", 2),
        ("IT", "utvikler", "Hva er fordelene med CI/CD i et team?", 1),
        ("IT", "ai", "Forklar forskjellen på Supervised og Unsupervised learning.", 2),
        
        # --- HÅNDVERK ---
        ("Bygg", "tømrer", "Hvordan sikrer du at en bærende konstruksjon er i vater over lange strekk?", 2),
        ("Bygg", "elektriker", "Hva er prosedyren for å sikre at strømmen er koblet fra før arbeid (FSE)?", 3),
        ("Bygg", "rørlegger", "Hvordan trykktester du et nytt røranlegg?", 2),
        ("Bygg", "hms", "Hva gjør du hvis du ser en kollega bryte sikkerhetsreglene?", 1),
        ("Bygg", "anlegg", "Hvordan sikrer du området før kranløft?", 2),
        
        # --- SALG & ØKONOMI ---
        ("Salg", "salg", "Hvordan håndterer du en kunde som sier 'vi har ikke budsjett'?", 2),
        ("Salg", "b2b", "Beskriv din prosess for å finne beslutningstakeren i en bedrift.", 3),
        ("Salg", "service", "Hvordan snur du en misfornøyd kunde til å bli fornøyd?", 1),
        ("Økonomi", "regnskap", "Hva er forskjellen på periodisering og kontantprinsippet?", 2),
        ("Økonomi", "leder", "Hvordan motiverer du et team som ligger bak budsjett?", 3),
        
        # --- GENERELLE (Soft Skills - fallback) ---
        ("Generell", "alle", "Beskriv en situasjon der du gjorde en feil. Hva lærte du?", 1),
        ("Generell", "alle", "Hvordan håndterer du stress og korte frister?", 1),
        ("Generell", "alle", "Hvorfor ønsker du akkurat denne stillingen?", 1)
    ]
    
    print(f"   -> Legger inn {len(dataset)} fagspørsmål...")
    
    for kat, tag, spm, lvl in dataset:
        c.execute("INSERT INTO questions (kategori, nokkelord, sporsmal, vanskelighetsgrad) VALUES (?, ?, ?, ?)", 
                  (kat, tag, spm, lvl))
        
    conn.commit()
    conn.close()
    print("✅ Ferdig! Aivory kan nå eksaminere kandidater i alt fra Helse til IT.")

if __name__ == "__main__":
    build_question_bank()
