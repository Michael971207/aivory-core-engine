import csv

# REALISTISKE SCENARIER FOR NYUTDANNEDE
junior_insights = [
    [
        "Nyutdannet Bachelor Markedsføring. Ingen relevant erfaring, men har jobbet 4 år deltid på McDonald's ved siden av studiene.",
        "Junior Sales Associate. Krever høy arbeidskapasitet og kundekontakt.",
        0.90,
        "MATCH: 4 år på McDonald's viser ekstrem arbeidsmoral, evne til å håndtere stress og møte opp til tiden. Dette er bedre enn en relevant sommerjobb hvor man bare kokte kaffe."
    ],
    [
        "Master i Historie, Master i Statsvitenskap, Bachelor i Filosofi. 29 år gammel, aldri hatt en betalt jobb.",
        "Konsulent i byrå. Krever kommersiell forståelse og faktureringsgrad.",
        0.30,
        "RISIKO: Kandidaten er akademisk sterk, men mangler 'business mindset'. Risiko for at overgangen til en kommersiell hverdag blir for brutal."
    ],
    [
        "Ingen høyere utdanning. Har bygget og driftet sin egen Minecraft-server med 500 brukere. Kan Python og Linux ut og inn.",
        "Junior Systemadministrator / DevOps. Trenger noen som kan fikse servere når de brenner.",
        0.95,
        "MATCH: Praktisk erfaring med å drifte en live server med ekte brukere trumfer ofte en teoretisk bachelorgrad for denne typen stilling."
    ],
    [
        "Nyutdannet Økonomi. C-snitt (gjennomsnittlig) karakterer. Men har vært leder for Studentforeningen og arrangert UKA-festivalen.",
        "Management Trainee. Ser etter fremtidige ledere.",
        0.88,
        "MATCH: Karakterene er middels, men ledererfaringen fra studentforeningen viser initiativ, ansvar og sosiale antenner som er avgjørende for en lederrolle."
    ],
    [
        "A i alle fag på Master i Datateknologi. Har aldri kodet noe utenom obligatoriske innleveringer. Ingen GitHub-profil.",
        "Fullstack Utvikler i startup. Må kunne bygge ting raskt fra dag én.",
        0.40,
        "MISMATCH: Kandidaten er teoretisk briljant, men mangler 'hacker-mentaliteten' og lidenskapen for å bygge ting som en startup trenger."
    ]
]

print(f"🎓 Legger til {len(junior_insights)} realistiske junior-caset i hjernen...")

with open("training_data.csv", "a", newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(junior_insights)

print("✅ Data lagt til! AI-en forstår nå verdien av McDonald's og studentverv.")
