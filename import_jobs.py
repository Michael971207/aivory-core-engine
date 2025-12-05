import sqlite3
import random

def build_job_library():
    print("📚 Bygger Aivory Universal Job Database...")
    
    # En enorm liste med yrker, beskrivelser og ferdighetskrav
    # Dette simulerer et datasett du ville lastet ned fra nettet
    industries = {
        "Helse & Omsorg": [
            ("Sykepleier", "Autorisert sykepleier med erfaring fra sengepost. Du må være omsorgsfull, tåle høyt tempo og kunne bruke DIPS.", ["omsorg", "medisiner", "sykehus", "autorisasjon"]),
            ("Helsefagarbeider", "Vi søker en engasjert helsefagarbeider til hjemmetjenesten. Førerkort klasse B er et krav.", ["omsorg", "eldre", "førerkort", "hjemmetjeneste"]),
            ("Lege (Fastlege)", "Ledig hjemmel som fastlege. Du må ha norsk autorisasjon, godkjent LIS1 og gode kommunikasjonsevner.", ["medisin", "pasienter", "diagnose", "helse"]),
            ("Tannlege", "Privat klinikk søker tannlege med fokus på kvalitet og pasienttrygghet. Erfaring med protetikk er en fordel.", ["tannhelse", "odonto", "pasient", "presisjon"])
        ],
        "Bygg & Anlegg": [
            ("Tømrer", "Selvstendig tømrer søkes til rehabilitering og nybygg. Du må ha fagbrev og kunne lese tegninger.", ["snekker", "treverk", "fagbrev", "bygg"]),
            ("Rørlegger", "Servicerørlegger søkes. Varierte dager med oppdrag hos private og bedrifter. Våtromssertifikat ønskelig.", ["rør", "vvs", "våtrom", "service"]),
            ("Elektriker", "Vi trenger en elektriker gruppe L. Jobben består av installasjon i nye boliger og smarthus-løsninger.", ["strøm", "kabel", "sikring", "fagbrev"]),
            ("Kranfører", "Erfaren kranfører til stor byggeplass. G2, G3 eller G4 kranførerbevis kreves. Sikkerhet er førsteprioritet.", ["kran", "løft", "sikkerhet", "hms"]),
            ("Anleggsleder", "Leder med ansvar for fremdrift, HMS og økonomi på anleggsplassen. Ingeniørbakgrunn foretrekkes.", ["ledelse", "hms", "anlegg", "planlegging"])
        ],
        "IT & Teknologi": [
            ("Frontend Utvikler", "Ekspert på React og moderne JavaScript/TypeScript. Du har øye for design og brukervennlighet (UX).", ["javascript", "react", "css", "frontend"]),
            ("Cyber Security Ekspert", "Vi trenger noen til å sikre vår infrastruktur. Erfaring med penetrasjonstesting og nettverkssikkerhet.", ["sikkerhet", "hacking", "nettverk", "firewall"]),
            ("Data Scientist", "Kan du gjøre data om til gull? Vi søker deg som kan Python, SQL og maskinlæring.", ["python", "data", "statistikk", "ai"]),
            ("Systemadministrator", "Ansvar for drift av våre Windows og Linux servere. Du må like problemløsning og support.", ["server", "linux", "nettverk", "drift"])
        ],
        "Salg & Service": [
            ("Butikkmedarbeider", "Utadvendt og blid person til klesbutikk. Du elsker kundeservice og holder orden i butikken.", ["service", "salg", "kasse", "mote"]),
            ("Key Account Manager", "B2B-salg mot store kunder. Du bygger langsiktige relasjoner og forhandler kontrakter.", ["salg", "b2b", "forhandling", "relasjoner"]),
            ("Kundeservice", "Svare på henvendelser via telefon og chat. Du er tålmodig og løsningsorientert.", ["telefon", "chat", "service", "hjelp"])
        ],
        "Utdanning": [
            ("Lærer (Barneskole)", "Kontaktlærer for 1.-4. trinn. Du er en tydelig klasseleder med hjerte for elevene.", ["pedagogikk", "barn", "undervisning", "klasseledelse"]),
            ("Barnehageassistent", "Leken og ansvarlig voksen som liker å være ute i all slags vær.", ["barn", "lek", "omsorg", "ute"]),
            ("Rektor", "Leder for en skole i utvikling. Du har visjoner for elevenes læringsmiljø og personalets trivsel.", ["ledelse", "skole", "pedagogikk", "budsjett"])
        ]
    }
    
    conn = sqlite3.connect('aivory_logs.db')
    c = conn.cursor()
    
    # Slett gamle jobber for å få en ren start (valgfritt)
    c.execute("DELETE FROM jobs")
    
    count = 0
    for industry, jobs in industries.items():
        for title, desc, tags in jobs:
            # Vi legger til bransjen i beskrivelsen for at AI-en skal forstå kontekst
            full_desc = f"Bransje: {industry}. {desc}\nNøkkelord: {', '.join(tags)}."
            c.execute("INSERT INTO jobs (tittel, beskrivelse) VALUES (?, ?)", (title, full_desc))
            count += 1
            
    conn.commit()
    conn.close()
    print(f"✅ Ferdig! Importerte {count} stillinger fordelt på {len(industries)} bransjer.")
    print("   Aivory kan nå rekruttere alt fra Leger til Kranførere.")

if __name__ == "__main__":
    build_job_library()
