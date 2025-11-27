import csv

# Her definerer vi EKTE innsikt - ting en vanlig søkemotor ikke skjønner.
expert_data = [
    # CASE 1: Gameren (Utradisjonell ledelse)
    [
        "22 år, ingen formell ledererfaring. Har ledet en 'Guild' med 40 personer i World of Warcraft i 3 år. Organisert raids, håndtert konflikter og oppmøte.",
        "Junior Team Lead for kundeservice. Trenger noen som kan holde hodet kaldt og organisere skiftplaner.",
        0.85,
        "MATCH: Ledelse i komplekse spill krever reell organisering, konflikthåndtering og stressmestring som er direkte overførbart til personalledelse."
    ],
    
    # CASE 2: Den Selvlærte (Portfolio over Papir)
    [
        "Droppet ut av VGS. Har kodet siden 12-årsalderen. Har 5 apper på App Store og bidrar til Open Source prosjekter ukentlig.",
        "Senior Utvikler. Krav: Mastergrad i informatikk.",
        0.95,
        "MATCH: Her må vi ignorere utdanningskravet. Kandidatens praktiske resultater og lidenskap trumfer formell utdanning i dette tilfellet."
    ],

    # CASE 3: Corporate til Kaos (Risiko)
    [
        "Senior Rådgiver i DNB/Statoil i 15 år. Vant til faste rutiner, store støtteapparat og langsomme prosesser.",
        "Daglig leder i et reklamebyrå med 4 ansatte. Høyt tempo, ingen struktur, man må gjøre alt selv.",
        0.30,
        "RISIKO: Selv om kandidaten er dyktig, er kultur-forskjellen for stor. Risiko for at vedkommende blir paralysert av mangelen på struktur."
    ],

    # CASE 4: Hull i CV-en (Kan være positivt)
    [
        "Hullete CV. Har reist jorden rundt i 2 år. Startet egen mislykket café. Skrevet en bok.",
        "Innovasjonsleder. Må tenke nytt og tørre å feile.",
        0.80,
        "MATCH: En 'rotete' bakgrunn indikerer her livserfaring, risikovilje og kreativitet, som er perfekt for innovasjon."
    ]
]

print(f"💎 Legger til {len(expert_data)} ekspert-innsikter i hjernen...")

# Vi bruker 'a' for append (legg til på slutten)
with open("training_data.csv", "a", newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(expert_data)

print("✅ Data lagt til! AI-en vet nå om gaming-ledelse og autodidakter.")
