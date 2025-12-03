import pandas as pd
import json
import os

CONFIG_FILE = "ai_memory_weights.json"

# --- KUNNSKAPSDATABASE FOR INTERVJUSPØRSMÅL ---
# AI velger spørsmål basert på hva kandidaten scorer lavest på
INTERVIEW_QUESTIONS = {
    "Struktur": [
        "Jeg ser at du leverer raskt, men hvordan sikrer du kvalitet i koden når fristen er kort?",
        "Beskriv en gang du mistet oversikten i et prosjekt. Hva lærte du?"
    ],
    "Driv": [
        "Hvordan motiverer du deg selv når oppgavene er kjedelige eller repetitive?",
        "Fortell om et mål du satte deg som du IKKE nådde. Hva skjedde?"
    ],
    "Samarbeid": [
        "Beskriv en konflikt du hadde med en kollega. Hvordan løste du den?",
        "Foretrekker du å jobbe alene eller i team? Hvorfor?"
    ],
    "Erfaring": [
        "Du har litt kortere fartstid enn andre søkere. Hva gjør du for å lære raskt?",
        "Hvilket teknisk problem har utfordret deg mest det siste året?"
    ]
}

DEFAULT_PROFILE = {
    "title": "Senior AI Utvikler",
    "must_have": ["Python", "AI"],
    "min_experience": 3,
    "ideal_personality": { "Struktur": 8, "Driv": 7, "Samarbeid": 6 },
    "weights": { "skills": 0.4, "experience": 0.2, "personality": 0.4 }
}

def load_profile():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return DEFAULT_PROFILE

class AivoryRecruiter:
    def __init__(self):
        self.profile = load_profile()
        self.candidates = pd.DataFrame()
        self.results_df = pd.DataFrame()

    def load_candidates(self, filepath):
        self.candidates = pd.read_csv(filepath)

    def calculate_logic_match(self):
        results = []
        weights = self.profile['weights']
        ideal = self.profile['ideal_personality']

        for index, row in self.candidates.iterrows():
            cand_skills = str(row['Ferdigheter']).lower()
            matching_skills = [s for s in self.profile['must_have'] if s.lower() in cand_skills]
            
            if not matching_skills: continue 
                
            skill_score = 100 
            exp_score = min(row['Erfaring'] * 10, 100)
            if row['Erfaring'] < self.profile['min_experience']: exp_score = 0
            
            # Personlighetsscore
            diff_struktur = abs(row['Struktur'] - ideal['Struktur'])
            diff_driv = abs(row['Driv'] - ideal['Driv'])
            diff_samarbeid = abs(row['Samarbeid'] - ideal['Samarbeid'])
            
            personality_score = max(100 - ((diff_struktur + diff_driv + diff_samarbeid) * 5), 0)
            
            final_score = (skill_score * weights['skills']) + \
                          (exp_score * weights['experience']) + \
                          (personality_score * weights['personality'])

            # --- NYTT: FINN SVAKESTE PUNKT FOR INTERVJU ---
            # Vi sjekker hva som trekker mest ned
            weaknesses = {
                "Struktur": row['Struktur'], 
                "Driv": row['Driv'], 
                "Samarbeid": row['Samarbeid'],
                "Erfaring": row['Erfaring']
            }
            # Finn den egenskapen som er lavest (forenklet logikk)
            weakest_link = min(weaknesses, key=weaknesses.get)
            
            # Hent et relevant spørsmål
            import random
            recommended_question = random.choice(INTERVIEW_QUESTIONS.get(weakest_link, ["Fortell om deg selv."]))

            results.append({
                "ID": row['ID'],
                "Hidden_Name": row['Faktisk_Navn'],
                "Total_Score": round(final_score, 1),
                "Ferdigheter": row['Ferdigheter'],
                "Svakhet": weakest_link,
                "Intervju_Tips": recommended_question
            })
            
        self.results_df = pd.DataFrame(results).sort_values(by='Total_Score', ascending=False)

    def generate_html_dashboard(self):
        """Lager en lekker HTML-rapport til kunden (Selskapet)"""
        top_10 = self.results_df.head(10)
        
        html_content = f"""
        <html>
        <head>
            <title>Aivory Report - {self.profile['title']}</title>
            <style>
                body {{ font-family: Arial, sans-serif; background-color: #f4f4f9; padding: 20px; }}
                h1 {{ color: #2c3e50; }}
                table {{ width: 100%; border-collapse: collapse; background: white; }}
                th, td {{ padding: 12px; border-bottom: 1px solid #ddd; text-align: left; }}
                th {{ background-color: #3498db; color: white; }}
                tr:hover {{ background-color: #f1f1f1; }}
                .match {{ color: green; font-weight: bold; }}
                .question {{ color: #e74c3c; font-style: italic; }}
                .locked {{ filter: blur(4px); user-select: none; }}
                .unlocked {{ font-weight: bold; }}
            </style>
        </head>
        <body>
            <h1>Aivory Analyse: {self.profile['title']}</h1>
            <p>AI har screenet databasen og funnet følgende toppkandidater.</p>
            <p><i>Kandidater markert med * er automatisk anonymisert inntil intervju.</i></p>
            
            <table>
                <tr>
                    <th>ID / Navn</th>
                    <th>Total Score</th>
                    <th>Ferdigheter</th>
                    <th>AI-Generert Intervjuspørsmål (Basert på svakhet)</th>
                </tr>
        """
        
        for i, row in top_10.iterrows():
            # Blind rekruttering logikk for visning
            navn_visning = f"🔒 {row['ID']}"
            if i < 3: # Topp 3 er "låst opp"
                navn_visning = f"✅ {row['Hidden_Name']} ({row['ID']})"
            
            html_content += f"""
                <tr>
                    <td class="unlocked">{navn_visning}</td>
                    <td class="match">{row['Total_Score']}%</td>
                    <td>{row['Ferdigheter']}</td>
                    <td>
                        <strong>Fokus: {row['Svakhet']}</strong><br>
                        <span class="question">"{row['Intervju_Tips']}"</span>
                    </td>
                </tr>
            """
            
        html_content += """
            </table>
            <p>Generert av Aivory Core Engine</p>
        </body>
        </html>
        """
        
        with open("dashboard_rapport.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        print("\n[DASHBOARD] Rapport generert: 'dashboard_rapport.html'")

if __name__ == "__main__":
    engine = AivoryRecruiter()
    engine.load_candidates("bulk_applicants.csv")
    engine.calculate_logic_match()
    engine.generate_html_dashboard()
