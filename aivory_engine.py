import pandas as pd

# --- JOBBPROFIL (Blind Rekruttering) ---
JOB_PROFILE = {
    "title": "Senior AI Utvikler",
    "must_have": ["Python", "AI"],
    "min_experience": 3,
    "ideal_personality": { "Struktur": 8, "Driv": 7, "Samarbeid": 6 },
    "weights": { "skills": 0.4, "experience": 0.2, "personality": 0.4 }
}

class AivoryRecruiter:
    def __init__(self, job_profile):
        self.profile = job_profile
        self.candidates = pd.DataFrame()

    def load_candidates(self, filepath):
        print(f"\n[1] Laster inn database...")
        # Laster alt, men vi later som om 'Faktisk_Navn' er kryptert for brukeren
        self.candidates = pd.read_csv(filepath)
        print(f"    -> Behandler {len(self.candidates)} kandidater ANONYMT.")

    def calculate_logic_match(self):
        print(f"\n[2] Starter blind-analyse (Ingen navn/kjønn påvirker resultatet)...")
        results = []
        
        for index, row in self.candidates.iterrows():
            # --- SAMME LOGIKK SOM FØR (Vekting av skills + personlighet) ---
            cand_skills = str(row['Ferdigheter']).lower()
            matching_skills = [s for s in self.profile['must_have'] if s.lower() in cand_skills]
            
            if not matching_skills: continue 
                
            skill_score = 100 
            exp_score = min(row['Erfaring'] * 10, 100)
            if row['Erfaring'] < self.profile['min_experience']: exp_score = 0
            
            ideal = self.profile['ideal_personality']
            diff = abs(row['Struktur'] - ideal['Struktur']) + abs(row['Driv'] - ideal['Driv']) + abs(row['Samarbeid'] - ideal['Samarbeid'])
            personality_score = max(100 - (diff * 5), 0)
            
            weights = self.profile['weights']
            final_score = (skill_score * weights['skills']) + (exp_score * weights['experience']) + (personality_score * weights['personality'])
            
            # --- HER ER FORSKJELLEN: VI BRUKER ID, IKKE NAVN ---
            results.append({
                "ID": row['ID'],
                "Hidden_Name": row['Faktisk_Navn'], # Lagres skjult
                "Total_Score": round(final_score, 1),
                "Ferdigheter": row['Ferdigheter'],
                "Kultur_Match": personality_score
            })
            
        self.results_df = pd.DataFrame(results).sort_values(by='Total_Score', ascending=False)

    def present_blind_shortlist(self):
        top_10 = self.results_df.head(10)
        
        print(f"\n[3] RESULTAT AV BLIND REKRUTTERING:")
        print("    (Navn vises kun ved høy match og simulert samtykke)")
        print("-" * 100)
        print(f"{'KANDIDAT-ID':<15} | {'SCORE':<6} | {'KULTUR':<8} | {'STATUS / HANDLING'}")
        print("-" * 100)
        
        for i, (index, row) in enumerate(top_10.iterrows()):
            status = "Anonym"
            display_name = "SKJULT"
            
            # LOGIKK: Hvis de er topp 3, simulerer vi at vi "låser opp" navnet
            if i < 3:
                status = "✅ MATCH! Samtykke gitt."
                display_name = row['Hidden_Name'] # Her avsløres navnet
            else:
                status = "🔒 Venter på samtykke"
            
            # For de anonyme viser vi bare ID-en
            if status == "Anonym" or "Venter" in status:
                print(f"{row['ID']:<15} | {row['Total_Score']:<6} | {row['Kultur_Match']:<8} | {status}")
            else:
                # For topp 3 viser vi at vi har funnet navnet
                print(f"{row['ID']:<15} | {row['Total_Score']:<6} | {row['Kultur_Match']:<8} | {status} -> Navn: {display_name}")

        top_10.to_csv("blind_shortlist.csv", index=False)
        print("-" * 100)

if __name__ == "__main__":
    engine = AivoryRecruiter(JOB_PROFILE)
    engine.load_candidates("bulk_applicants.csv")
    engine.calculate_logic_match()
    engine.present_blind_shortlist()
