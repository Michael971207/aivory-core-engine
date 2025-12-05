import sqlite3

def build_wisdom_db():
    print("🧠 Laster inn 'Aivory Wisdom' (Etikk & Dømmekraft)...")
    
    conn = sqlite3.connect('aivory_logs.db')
    c = conn.cursor()
    
    # 1. TABELL FOR SITUASJONER (Dilemmaer)
    c.execute("DROP TABLE IF EXISTS scenarios")
    c.execute('''CREATE TABLE scenarios 
                 (id INTEGER PRIMARY KEY, kategori TEXT, scenario TEXT, best_answer TEXT, worst_answer TEXT)''')
    
    scenarios = [
        ("Konflikt", "En kollega leverer ikke sin del av prosjektet i tide, og det går ut over deg. Hva gjør du?", 
         "Jeg tar en privat prat med kollegaen for å forstå årsaken og se om jeg kan hjelpe.", 
         "Jeg klager til sjefen med en gang og sier at det ikke er min feil."),
         
        ("Etikk", "Du oppdager en feil i koden som ingen andre har sett, men som kan forsinke lansering. Hva gjør du?",
         "Jeg melder fra umiddelbart. Kvalitet og ærlighet er viktigst, selv om det blir forsinkelser.",
         "Jeg sier ingenting og håper ingen merker det før etter lansering."),
         
        ("Stress", "Du har tre hasteoppgaver samtidig og rekker ikke alle. Hva gjør du?",
         "Jeg kommuniserer tydelig til lederen min, ber om prioritering og forventningsstyrer.",
         "Jeg prøver å gjøre alt halvveis og jobber til jeg stuper uten å si ifra."),
         
        ("Kundeservice", "En kunde er rasende på telefonen for en feil vi har gjort.",
         "Jeg lytter, beklager ektefølt, og fokuserer på å løse problemet der og da.",
         "Jeg forklarer kunden at de tar feil og ber dem roe seg ned.")
    ]
    
    for kat, scen, best, worst in scenarios:
        c.execute("INSERT INTO scenarios (kategori, scenario, best_answer, worst_answer) VALUES (?, ?, ?, ?)", (kat, scen, best, worst))

    # 2. TABELL FOR RED FLAGS (Varsellamper)
    c.execute("DROP TABLE IF EXISTS red_flags")
    c.execute("CREATE TABLE red_flags (phrase TEXT, severity INTEGER, category TEXT)")
    
    flags = [
        ("hater sjefen", 10, "Holdning"),
        ("orker ikke", 8, "Motivasjon"),
        ("ikke min feil", 7, "Ansvar"),
        ("kjedelig", 5, "Motivasjon"),
        ("idioter", 10, "Sosialt"),
        ("gidder ikke", 9, "Arbeidsmoral"),
        ("bare penger", 6, "Motivasjon"),
        ("hater kunder", 10, "Service"),
        ("slappe av", 4, "Ambisiøs")
    ]
    
    for phrase, sev, cat in flags:
        c.execute("INSERT INTO red_flags VALUES (?, ?, ?)", (phrase, sev, cat))

    conn.commit()
    conn.close()
    print("✅ Visdom installert! Aivory kan nå dømme karakter og modenhet.")

if __name__ == "__main__":
    build_wisdom_db()
