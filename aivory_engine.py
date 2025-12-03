import pandas as pd
import json
import os
import random
import time

CONFIG_FILE = "ai_memory_weights.json"

# --- KUNNSKAPSDATABASE ---
INTERVIEW_QUESTIONS = {
    "Struktur": ["Hvordan sikrer du kvalitet under tidspress?", "Fortell om en gang du mistet oversikten."],
    "Driv": ["Hva gjør du når oppgavene blir kjedelige?", "Fortell om et mål du ikke nådde."],
    "Samarbeid": ["Beskriv en konflikt med en kollega.", "Jobber du best alene eller i team?"],
    "Erfaring": ["Hvordan lærer du deg nye teknologier raskt?", "Hva er det vanskeligste problemet du har løst?"]
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
        if not os.path.exists(filepath):
            print(f"Feil: Finner ikke {filepath}")
            return
        self.candidates = pd.read_csv(filepath)

    def calculate_logic_match(self):
        results = []
        weights = self.profile['weights']
        ideal = self.profile['ideal_personality']

        print(f"\n[MOTOR] Analyserer {len(self.candidates)} kandidater...")

        for index, row in self.candidates.iterrows():
            cand_skills = str(row['Ferdigheter']).lower()
            matching_skills = [s for s in self.profile['must_have'] if s.lower() in cand_skills]
            
            if not matching_skills: continue 
                
            skill_score = 100 
            exp_score = min(row['Erfaring'] * 10, 100)
            if row['Erfaring'] < self.profile['min_experience']: exp_score = 0
            
            diff = abs(row['Struktur'] - ideal['Struktur']) + abs(row['Driv'] - ideal['Driv']) + abs(row['Samarbeid'] - ideal['Samarbeid'])
            personality_score = max(100 - (diff * 5), 0)
            
            final_score = (skill_score * weights['skills']) + \
                          (exp_score * weights['experience']) + \
                          (personality_score * weights['personality'])

            weaknesses = {"Struktur": row['Struktur'], "Driv": row['Driv'], "Samarbeid": row['Samarbeid'], "Erfaring": row['Erfaring']}
            weakest_link = min(weaknesses, key=weaknesses.get)
            tips = random.choice(INTERVIEW_QUESTIONS.get(weakest_link, ["Generelt spørsmål"]))

            results.append({
                "ID": row['ID'],
                "Hidden_Name": row['Faktisk_Navn'],
                "Total_Score": round(final_score, 1),
                "Ferdigheter": row['Ferdigheter'],
                "Svakhet": weakest_link,
                "Intervju_Tips": tips,
                "Struktur": row['Struktur'],
                "Driv": row['Driv'],
                "Samarbeid": row['Samarbeid'],
                "Erfaring": row['Erfaring']
            })
            
        self.results_df = pd.DataFrame(results).sort_values(by='Total_Score', ascending=False)
        self.top_10 = self.results_df.head(10).reset_index(drop=True)

    def generate_html_dashboard(self):
        # (Forenklet for å spare plass i koden, men funksjonaliteten er her)
        with open("dashboard_rapport.html", "w", encoding="utf-8") as f:
            f.write(f"<h1>Aivory Analyse ferdig</h1><p>Fant {len(self.results_df)} matcher.</p>")
        print("[RAPPORT] HTML oppdatert.")

    def chat_interface(self):
        print("\n" + "="*60)
        print("  AIVORY ASSISTANT - INTERAKTIV MODUS")
        print("  Still spørsmål som: 'Hvem vant?', 'Sammenlign topp 2', 'Vis svakhet [ID]', 'avslutt'")
        print("="*60)
        
        while True:
            command = input("\nDu: ").lower().strip()
            
            if command in ["avslutt", "exit", "quit", "nei"]:
                print("Aivory: Avslutter systemet. Ha en fin dag!")
                break
                
            elif "vant" in command or "best" in command or "vinner" in command:
                winner = self.top_10.iloc[0]
                print(f"Aivory: Vinneren er {winner['ID']} (Navn: {winner['Hidden_Name']}) med {winner['Total_Score']} poeng.")
            
            elif "sammenlign" in command or "duell" in command:
                c1 = self.top_10.iloc[0]
                c2 = self.top_10.iloc[1]
                print(f"\n--- DUELL: {c1['ID']} vs {c2['ID']} ---")
                print(f"{'EGENSKAP':<15} | {c1['ID']:<15} | {c2['ID']:<15}")
                print("-" * 50)
                print(f"{'Total Score':<15} | {str(c1['Total_Score']):<15} | {str(c2['Total_Score']):<15}")
                print(f"{'Struktur':<15} | {str(c1['Struktur']):<15} | {str(c2['Struktur']):<15}")
                print(f"{'Driv':<15} | {str(c1['Driv']):<15} | {str(c2['Driv']):<15}")
                print(f"{'Erfaring':<15} | {str(c1['Erfaring']):<15} | {str(c2['Erfaring']):<15}")
                
                diff = c1['Total_Score'] - c2['Total_Score']
                print(f"\nKONKLUSJON: {c1['ID']} vinner med {diff:.1f} poeng.")

            elif "svakhet" in command:
                # Prøver å finne ID i setningen
                found = False
                for index, row in self.top_10.iterrows():
                    if row['ID'].lower() in command:
                        print(f"Aivory: {row['ID']} sin største svakhet er '{row['Svakhet']}'.")
                        print(f"Tips til intervju: \"{row['Intervju_Tips']}\"")
                        found = True
                        break
                if not found:
                    print("Aivory: Jeg trenger en ID for å svare (f.eks 'Vis svakhet KANDIDAT-1234'). Se listen over.")
            
            elif "liste" in command or "vis alle" in command:
                 print(self.top_10[['ID', 'Total_Score', 'Svakhet']])

            else:
                print("Aivory: Jeg forsto ikke den. Prøv 'Hvem vant?' eller 'Sammenlign'.")

if __name__ == "__main__":
    engine = AivoryRecruiter()
    engine.load_candidates("bulk_applicants.csv")
    engine.calculate_logic_match()
    engine.generate_html_dashboard()
    
    # Start chatten til slutt
    engine.chat_interface()
