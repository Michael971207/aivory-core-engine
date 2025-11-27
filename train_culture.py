import csv

# KULTUR, REMOTE ARBEID OG PERSONLIGHET
culture_insights = [
    # CASE 1: Serie-gründeren (Konkurs er erfaring)
    [
        "Startet 2 selskaper, begge gikk konkurs etter 2 år. Har lært mye om salg og produktutvikling 'the hard way'.",
        "Business Developer i scale-up. Må tåle avslag og høyt tempo.",
        0.92,
        "MATCH: I startup-verdenen er 'mislykkede' gründere gull verdt. De har enorm eierskapsfølelse, grit, og vet hva som ikke fungerer."
    ],
    
    # CASE 2: Remote-veteranen (Selvledelse)
    [
        "Har jobbet 100% remote for et selskap i San Francisco i 4 år. Vant til asynkron kommunikasjon og Slack.",
        "Remote-first stilling. Teamet sitter i 5 ulike land.",
        0.95,
        "MATCH: Kandidaten har bevist evne til selvledelse og disiplin som kreves for remote arbeid. Mye tryggere valg enn en som aldri har jobbet hjemmefra."
    ],
    
    # CASE 3: 'Jobb-hopperen' (Rødt flagg)
    [
        "6 jobber på 2 år. Slutter ofte etter prøvetiden. Skylder på 'dårlig ledelse' hver gang.",
        "Langsiktig rolle i stabilt team.",
        0.15,
        "RISIKO: Mønsteret indikerer samarbeidsproblemer eller manglende utholdenhet. Høy risiko for churn (at de slutter) uansett faglig dyktighet."
    ],
    
    # CASE 4: Konsulenten som vil 'hjem' (In-house)
    [
        "Senior Konsulent i Big 4 (PwC/Deloitte). Lei av reising og faktureringspress. Vil jobbe med ETT produkt over tid.",
        "In-house Senior Utvikler. Fokus på kvalitet og langsiktighet.",
        0.88,
        "MATCH: Klassisk og sterkt motivasjonsskifte. Konsulenter som søker seg til in-house bringer ofte med seg høy profesjonalitet og struktur fra konsulenthus."
    ],

    # CASE 5: Introvert Utvikler i Salgsmiljø (Kulturkrasj)
    [
        "Fantastisk koder, elsker å sitte med hodetelefoner i mørket. Hater møter og small-talk.",
        "Technical Sales Engineer. Må bli med selgere i kundemøter og presentere løsninger.",
        0.35,
        "MISMATCH: Faglig sterk, men personligheten krasjer med rollens krav til ekstrovert energi og kundekontakt."
    ]
]

print(f"🌍 Legger til {len(culture_insights)} dype kultur-scenarier i hjernen...")

with open("training_data.csv", "a", newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(culture_insights)

print("✅ Data lagt til! AI-en kan nå vurdere gründere og remote-arbeidere.")
