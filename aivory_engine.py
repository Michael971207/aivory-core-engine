import pandas as pd

# --- DRØMMEPROFILEN FOR DENNE STILLINGEN ---
# Her definerer selskapet hva de ser etter i tillegg til kode.
JOB_PROFILE = {
    "title": "Senior AI Utvikler",
    "must_have": ["Python", "AI"],
    "min_experience": 3,
    # Ønsket personlighet (1-10)
    "ideal_personality": {
        "Struktur": 8,  # Må skrive ryddig kode
        "Driv": 7,      # Må være selvgående
        "Samarbeid": 6  # Må kunne jobbe i team, men trenger ikke være super-sosial
    },
    "weights": {
        "skills": 0.4,       # CV teller 40%
        "experience": 0.2,   # Erfaring teller 20%
        "personality": 0.4   # Personlighet teller 40% (Viktig!)
    }
}

class AivoryRecruiter:
    def __init__(self, job_profile):
        self.profile = job_profile
        self.candidates = pd.DataFrame()

    def load_candidates(self, filepath):
        print(f"\n[1] Laster inn søkere...")
        self.candidates = pd.read_csv(filepath)
        print(f"    -> Analyserer {len(self.candidates)} profiler.")

    def calculate_logic_match(self):
        """Dette er hjernen som veier faktorene mot hverandre."""
        print(f"\n[2] Starter AI-analyse med vekting: {self.profile['weights']}...")
        
        results = []
        
        for index, row in self.candidates.iterrows():
            # --- 1. HARD SKILLS SCORE (0-100) ---
            cand_skills = str(row['Ferdigheter']).lower()
            matching_skills = [s for s in self.profile['must_have'] if s.lower() in cand_skills]
            
            if not matching_skills:
                continue # Hopp over hvis de mangler basiskunnskap (Dealbreaker)
                
            skill_score = 100 # Har basic, får full pott (kan gjøres mer nyansert)
            
            # --- 2. ERFARING SCORE (0-100) ---
            # Max score ved 10 år, ellers proporsjonalt
            exp_score = min(row['Erfaring'] * 10, 100)
            if row['Erfaring'] < self.profile['min_experience']:
                exp_score = 0 # Straff for lite erfaring
            
            # --- 3. PERSONLIGHET MATCH (0-100) ---
            # Vi regner ut avviket fra idealet. Mindre avvik = Høyere score.
            ideal = self.profile['ideal_personality']
            
            # Formel: 100 minus avstanden fra idealet
            diff_struktur = abs(row['Struktur'] - ideal['Struktur'])
            diff_driv = abs(row['Driv'] - ideal['Driv'])
            diff_samarbeid = abs(row['Samarbeid'] - ideal['Samarbeid'])
            
            total_diff = diff_struktur + diff_driv + diff_samarbeid
            personality_score = max(100 - (total_diff * 5), 0) # Trekker 5 poeng per poeng avvik
            
            # --- 4. TOTAL VEKTET SCORE ---
            weights = self.profile['weights']
            final_score = (skill_score * weights['skills']) + \
                          (exp_score * weights['experience']) + \
                          (personality_score * weights['personality'])
            
            # --- 5. GENERER BEGRUNNELSE (AI Forklarer seg) ---
            reason = "God match."
            if personality_score > 90:
                reason = "PERFEKT kulturmatch og solid CV."
            elif personality_score < 50:
                reason = f"Faglig sterk, men personlighetsprofilen avviker fra teamet (Struktur: {row['Struktur']})."
            elif exp_score < 40:
                reason = "God personlighet, men mangler senior-tyngde."
            
            results.append({
                "Navn": row['Navn'],
                "Total_Score": round(final_score, 1),
                "P_Score": personality_score,
                "Ferdigheter": row['Ferdigheter'],
                "Begrunnelse": reason
            })
            
        # Sorter og lagre
        self.results_df = pd.DataFrame(results).sort_values(by='Total_Score', ascending=False)

    def present_shortlist(self):
        top_10 = self.results_df.head(10)
        print(f"\n[3] TOPP 10 KANDIDATER (Sortert etter logisk totalvurdering):")
        print("-" * 100)
        print(f"{'NAVN':<20} | {'SCORE':<6} | {'PERS.MATCH':<10} | {'AI BEGRUNNELSE'}")
        print("-" * 100)
        
        for index, row in top_10.iterrows():
            print(f"{row['Navn']:<20} | {row['Total_Score']:<6} | {row['P_Score']:<10} | {row['Begrunnelse']}")
            
        top_10.to_csv("smart_shortlist.csv", index=False)
        print("-" * 100)
        print("Liste lagret i 'smart_shortlist.csv'")

if __name__ == "__main__":
    engine = AivoryRecruiter(JOB_PROFILE)
    engine.load_candidates("bulk_applicants.csv")
    engine.calculate_logic_match()
    engine.present_shortlist()
