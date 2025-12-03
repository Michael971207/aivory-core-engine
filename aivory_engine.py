import pandas as pd
import json
import os

# --- KONFIGURASJON OG HUKOMMELSE ---
# Vi lagrer vektingen i en fil slik at AI-en kan huske endringer fra forrige kjøring
CONFIG_FILE = "ai_memory_weights.json"

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
            print("[SYSTEM] Laster inn 'lært' kunnskap fra tidligere...")
            return json.load(f)
    return DEFAULT_PROFILE

def save_profile(profile):
    with open(CONFIG_FILE, "w") as f:
        json.dump(profile, f)
    print("[SYSTEM] AI har oppdatert sin egen algoritme basert på din feedback.")

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
        
        print(f"\n[ANALYSE] Bruker vekting: Skill={weights['skills']:.2f}, Exp={weights['experience']:.2f}, Pers={weights['personality']:.2f}")

        for index, row in self.candidates.iterrows():
            # Samme logikk som før
            cand_skills = str(row['Ferdigheter']).lower()
            matching_skills = [s for s in self.profile['must_have'] if s.lower() in cand_skills]
            
            if not matching_skills: continue 
                
            skill_score = 100 
            exp_score = min(row['Erfaring'] * 10, 100)
            if row['Erfaring'] < self.profile['min_experience']: exp_score = 0
            
            ideal = self.profile['ideal_personality']
            diff = abs(row['Struktur'] - ideal['Struktur']) + abs(row['Driv'] - ideal['Driv']) + abs(row['Samarbeid'] - ideal['Samarbeid'])
            personality_score = max(100 - (diff * 5), 0)
            
            final_score = (skill_score * weights['skills']) + \
                          (exp_score * weights['experience']) + \
                          (personality_score * weights['personality'])
            
            results.append({
                "ID": row['ID'],
                "Hidden_Name": row['Faktisk_Navn'],
                "Total_Score": round(final_score, 1),
                "Struktur": row['Struktur'],
                "Erfaring": row['Erfaring']
            })
            
        self.results_df = pd.DataFrame(results).sort_values(by='Total_Score', ascending=False)

    def generate_communications(self, top_candidate):
        """AI skriver e-post utkast automatisk"""
        print(f"\n[KOMMUNIKASJON] AI forbereder e-poster for {top_candidate['ID']}...")
        
        email_content = f"""
        EMNE: Invitasjon til intervju - {self.profile['title']}
        
        Hei kandidat {top_candidate['ID']},
        
        Vi har analysert din profil blindt, og du scoret {top_candidate['Total_Score']} poeng i vår AI-vurdering.
        Særlig din match på våre verdier (Struktur: {top_candidate['Struktur']}) imponerte oss.
        
        Siden du er rangert som nr 1, ønsker vi å låse opp identiteten din og invitere til en prat.
        
        Mvh,
        Aivory AI Recruiting Team
        """
        print("-" * 50)
        print(email_content)
        print("-" * 50)
        
        # Lagre til fil
        with open("draft_email_winner.txt", "w", encoding="utf-8") as f:
            f.write(email_content)

    def learn_from_feedback(self):
        """Dette er lærings-løkken. Du er sjefen som trener AI-en."""
        top = self.results_df.iloc[0]
        print(f"\n[LÆRING] Vinneren er {top['ID']} med {top['Total_Score']} poeng.")
        print(f"   -> Egenskaper: Erfaring={top['Erfaring']} år, Struktur={top['Struktur']}")
        
        print("\nEr du fornøyd med denne kandidaten? (Simulert input for auto-kjøring)")
        # For demo-formål: Vi simulerer at sjefen synes Erfaring er viktigere hvis vinneren har lite erfaring
        
        if top['Erfaring'] < 5:
            print("   -> SYSTEM-SIMULERING: Sjefen mener kandidaten har for lite erfaring.")
            print("   -> HANDLING: AI justerer algoritmen. Øker vektingen av 'experience'.")
            
            # Oppdater vektene
            self.profile['weights']['experience'] += 0.1
            self.profile['weights']['personality'] -= 0.1 # Må ta poeng fra noe annet
            
            save_profile(self.profile)
        else:
            print("   -> SYSTEM-SIMULERING: Sjefen er fornøyd. Ingen endring i algoritmen.")

if __name__ == "__main__":
    engine = AivoryRecruiter()
    engine.load_candidates("bulk_applicants.csv")
    engine.calculate_logic_match()
    
    # Vis resultat
    top_candidate = engine.results_df.iloc[0]
    engine.generate_communications(top_candidate)
    
    # Kjør læring
    engine.learn_from_feedback()
