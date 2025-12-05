import sqlite3

def build_knowledge_graph():
    print("🧠 Bygger Aivory Knowledge Graph (Assosiasjons-database)...")
    
    conn = sqlite3.connect('aivory_logs.db')
    c = conn.cursor()
    
    # 1. Lag tabell for koblinger
    c.execute("DROP TABLE IF EXISTS knowledge_graph")
    c.execute('''CREATE TABLE knowledge_graph 
                 (trigger_word TEXT, implied_skill TEXT, confidence REAL)''')
    
    # 2. DATASETT (Trigger -> Hva det egentlig betyr)
    # Dette simulerer et "Real World" dataset vi kunne lastet ned
    associations = [
        # --- IT & TECH ---
        ("fullstack", "backend utvikling", 0.9),
        ("fullstack", "frontend utvikling", 0.9),
        ("fullstack", "database", 0.8),
        ("react", "javascript", 1.0),
        ("react", "frontend", 1.0),
        ("django", "python", 1.0),
        ("laravel", "php", 1.0),
        ("aws", "cloud computing", 0.9),
        ("aws", "devops", 0.7),
        ("scrum master", "agile metoder", 1.0),
        ("scrum master", "fasilitering", 0.8),
        
        # --- HELSE ---
        ("ambulanse", "akuttmedisin", 0.9),
        ("ambulanse", "stressmestring", 0.8),
        ("ambulanse", "førerkort 160", 1.0),
        ("sykepleier", "medikamenthåndtering", 1.0),
        ("sykepleier", "omsorg", 0.9),
        ("sykepleier", "journalføring", 0.8),
        ("lege", "diagnostikk", 1.0),
        ("lege", "ansvar", 0.9),
        
        # --- ERFARINGER (Det som ofte står i CV, men ikke er "fag") ---
        ("forsvaret", "disiplin", 0.9),
        ("forsvaret", "ledelse", 0.6),
        ("førstegangstjeneste", "samarbeid", 0.8),
        ("butikkmedarbeider", "kundeservice", 1.0),
        ("butikkmedarbeider", "salg", 0.7),
        ("butikkmedarbeider", "kasseoppgjør", 0.9),
        ("servitør", "multitasking", 0.9),
        ("servitør", "stressmestring", 0.8),
        ("servitør", "serviceinnstilling", 1.0),
        ("fotballtrener", "ledelse", 0.7),
        ("fotballtrener", "pedagogikk", 0.6),
        
        # --- ØKONOMI & SALG ---
        ("revisor", "nøyaktighet", 1.0),
        ("revisor", "excel", 0.9),
        ("revisor", "lovverk", 0.8),
        ("kaldt salg", "utholdenhet", 0.9),
        ("kaldt salg", "prospektering", 1.0),
        ("b2b", "relasjonsbygging", 0.8)
    ]
    
    print(f"   -> Importerer {len(associations)} nevrale koblinger...")
    
    for trigger, skill, conf in associations:
        c.execute("INSERT INTO knowledge_graph VALUES (?, ?, ?)", (trigger, skill, conf))
        
    conn.commit()
    conn.close()
    print("✅ Hjernen er oppdatert! Den kan nå 'lese mellom linjene'.")

if __name__ == "__main__":
    build_knowledge_graph()
