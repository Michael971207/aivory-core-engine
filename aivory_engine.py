import pandas as pd
import json
import os

# --- KLIENT-DATABASE (Våre kunder) ---
CLIENTS = [
    {
        "name": "TechNova AS",
        "industry": "IT",
        "looking_for": ["Python", "AI", "Cloud", "Java"],
        "min_exp": 2,
        "ideal_personality": {"Struktur": 7, "Driv": 8, "Samarbeid": 6}
    },
    {
        "name": "Nordic Bank",
        "industry": "Finans",
        "looking_for": ["Excel", "Økonomi", "Analyse", "Regnskap"],
        "min_exp": 5,
        "ideal_personality": {"Struktur": 10, "Driv": 5, "Samarbeid": 5}
    },
    {
        "name": "Creative Minds",
        "industry": "Design",
        "looking_for": ["Figma", "Photoshop", "Design", "SoMe"],
        "min_exp": 1,
        "ideal_personality": {"Struktur": 4, "Driv": 8, "Samarbeid": 9}
    }
]

class AivoryMatchmaker:
    def __init__(self):
        self.candidates = pd.DataFrame()
        self.matches = [] # Her lagrer vi hvem som passer hvor

    def load_candidates(self, filepath):
        self.candidates = pd.read_csv(filepath)
        print(f"[SYSTEM] Lastet {len(self.candidates)} kandidater. Starter matching mot {len(CLIENTS)} klienter...")

    def run_multi_client_matching(self):
        """Sjekker hver kandidat mot alle klienter"""
        
        for index, row in self.candidates.iterrows():
            cand_skills = str(row['Ferdigheter']).lower()
            
            best_score = 0
            best_client = None
            
            # Sjekk mot hver kunde
            for client in CLIENTS:
                # 1. Ferdighetssjekk
                client_skills = [s.lower() for s in client['looking_for']]
                matches = [s for s in client_skills if s in cand_skills]
                
                if not matches:
                    continue # Ingen match her
                
                match_percent = len(matches) / len(client_skills)
                skill_points = match_percent * 50 # Max 50 poeng for skills
                
                # 2. Erfaringssjekk
                exp_points = 0
                if row['Erfaring'] >= client['min_exp']:
                    exp_points = 20
                
                # 3. Personlighetssjekk (Kulturmatch)
                ideal = client['ideal_personality']
                diff = abs(row['Struktur'] - ideal['Struktur']) + \
                       abs(row['Driv'] - ideal['Driv']) + \
                       abs(row['Samarbeid'] - ideal['Samarbeid'])
                cult_points = max(30 - diff, 0) # Max 30 poeng for kultur
                
                total_score = skill_points + exp_points + cult_points
                
                # Vi lagrer bare hvis det er en GOD match (> 60 poeng)
                if total_score > 60 and total_score > best_score:
                    best_score = total_score
                    best_client = client['name']

            # Hvis kandidaten passet hos noen, legg dem i listen
            if best_client:
                self.matches.append({
                    "Kandidat_ID": row['ID'],
                    "Navn": row['Faktisk_Navn'], # Ville vært skjult i ekte prod
                    "Matchet_Med": best_client,
                    "Score": round(best_score, 1),
                    "Ferdigheter": row['Ferdigheter']
                })

    def generate_master_dashboard(self):
        """Lager en HTML-oversikt for hele Aivory-systemet"""
        df = pd.DataFrame(self.matches)
        
        if df.empty:
            print("Ingen matcher funnet.")
            return

        # Sorter etter selskap og score
        df = df.sort_values(by=['Matchet_Med', 'Score'], ascending=[True, False])
        
        html = """
        <html>
        <head>
            <title>Aivory Global Dashboard</title>
            <style>
                body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #222; color: #fff; padding: 20px; }
                .card { background: #333; margin-bottom: 20px; padding: 15px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
                h1 { text-align: center; color: #00d2ff; }
                h2 { border-bottom: 2px solid #555; padding-bottom: 10px; color: #ffd700; }
                table { width: 100%; border-collapse: collapse; margin-top: 10px; }
                th, td { padding: 10px; text-align: left; border-bottom: 1px solid #444; }
                th { color: #aaa; }
                .score { font-weight: bold; color: #00ff9d; }
            </style>
        </head>
        <body>
            <h1>AIVORY MULTI-CLIENT DASHBOARD</h1>
            <p style="text-align:center;">Sanntidsoversikt over plasseringer</p>
        """
        
        # Lag en seksjon per kunde
        for client in CLIENTS:
            client_name = client['name']
            matches = df[df['Matchet_Med'] == client_name].head(5) # Topp 5 per kunde
            
            html += f"<div class='card'><h2>🏢 {client_name} ({client['industry']})</h2>"
            
            if matches.empty:
                html += "<p>Ingen kvalifiserte kandidater funnet i dag.</p>"
            else:
                html += "<table><tr><th>ID</th><th>Score</th><th>Ferdigheter</th></tr>"
                for _, row in matches.iterrows():
                    html += f"<tr><td>{row['Kandidat_ID']}</td><td class='score'>{row['Score']}</td><td>{row['Ferdigheter']}</td></tr>"
                html += "</table>"
            
            html += "</div>"

        html += "</body></html>"
        
        with open("global_dashboard.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("\n[DASHBOARD] 'global_dashboard.html' er generert! Åpne den for å se oversikten.")

if __name__ == "__main__":
    engine = AivoryMatchmaker()
    engine.load_candidates("bulk_applicants.csv")
    engine.run_multi_client_matching()
    engine.generate_master_dashboard()
