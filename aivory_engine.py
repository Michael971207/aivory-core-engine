import pandas as pd
import time
import random

# --- KONFIGURASJON FOR STILLINGEN (Dette endrer selskapet for hver jobb) ---
JOB_PROFILE = {
    "title": "Senior AI Utvikler",
    "must_have": ["Python", "AI"],     # MÅ ha disse for å ikke bli forkastet
    "nice_to_have": ["SQL", "Machine Learning"], # Gir bonuspoeng
    "min_experience": 3
}

class AivoryRecruiter:
    def __init__(self, job_profile):
        self.profile = job_profile
        self.candidates = []
        self.top_candidates = []

    def load_candidates(self, filepath):
        print(f"\n[1] Laster inn søkere fra {filepath}...")
        self.candidates = pd.read_csv(filepath)
        print(f"    -> Fant {len(self.candidates)} søkere i systemet.")

    def phase_1_hard_screening(self):
        """Kaster ut alle som mangler basiskunnskapene. Sparer tid."""
        print(f"\n[2] Starter grov-screening (Siler ut de uten {self.profile['must_have']})...")
        passed = []
        rejected_count = 0
        
        for index, row in self.candidates.iterrows():
            cand_skills = str(row['Ferdigheter']).lower()
            cand_exp = int(row['Erfaring'])
            
            # Sjekk 1: Har de minimumskravene?
            missing_skills = [skill for skill in self.profile['must_have'] if skill.lower() not in cand_skills]
            
            # Sjekk 2: Har de nok erfaring?
            exp_ok = cand_exp >= self.profile['min_experience']

            if not missing_skills and exp_ok:
                passed.append(row)
            else:
                rejected_count += 1
        
        self.candidates = pd.DataFrame(passed)
        print(f"    -> {rejected_count} søkere ble avvist automatisk.")
        print(f"    -> {len(self.candidates)} kandidater går videre til AI-Testing.")

    def phase_2_ai_testing_and_scoring(self):
        """Genererer tester og scorer de gjenværende kandidatene."""
        print(f"\n[3] Genererer personlige AI-tester for de {len(self.candidates)} gjenværende...")
        
        scored_candidates = []
        
        for index, row in self.candidates.iterrows():
            score = 0
            cand_skills = str(row['Ferdigheter']).lower()
            
            # --- AI LOGIKK HER ---
            # 1. Poeng for "Nice to have" ferdigheter
            for skill in self.profile['nice_to_have']:
                if skill.lower() in cand_skills:
                    score += 15
            
            # 2. Poeng for utdanning (Simulert vekting)
            if "NTNU" in row['Utdanning'] or "UiO" in row['Utdanning']:
                score += 10
            
            # 3. Erfaringsbonus
            score += (row['Erfaring'] * 2) # 2 poeng per år erfaring
            
            # 4. SIMULERT AI-TEST (Her ville vi koblet på LLM for å generere spørsmål)
            # Vi genererer et unikt spørsmål basert på profilen deres
            test_question = f"Hei {row['Navn']}, gitt din erfaring med {row['Ferdigheter']}, hvordan ville du løst et problem med skalering?"
            # Vi simulerer at de svarer og AI scorer svaret (tilfeldig 50-100 poeng for demo)
            ai_test_score = random.randint(50, 100) 
            
            total_score = score + ai_test_score
            
            # Legg til i listen med detaljer
            cand_dict = row.to_dict()
            cand_dict['AI_Test_Score'] = ai_test_score
            cand_dict['Total_Score'] = total_score
            cand_dict['Generated_Question'] = test_question
            scored_candidates.append(cand_dict)
            
        # Sorter basert på total score (Høyest først)
        self.candidates = pd.DataFrame(scored_candidates).sort_values(by='Total_Score', ascending=False)

    def phase_3_delivery(self):
        """Leverer topp 10 liste."""
        top_10 = self.candidates.head(10)
        print(f"\n[4] ANALYSE FERDIG. Her er topp 10 kandidater til din kunde:")
        print("-" * 80)
        print(f"{'NAVN':<20} | {'TOTAL SCORE':<12} | {'FERDIGHETER':<30}")
        print("-" * 80)
        
        for index, row in top_10.iterrows():
            print(f"{row['Navn']:<20} | {row['Total_Score']:<12} | {row['Ferdigheter'][:30]}...")
            
        # Lagre rapport
        top_10.to_csv("final_shortlist.csv", index=False)
        print("-" * 80)
        print("Shortlist er lagret i 'final_shortlist.csv'. Send denne til kunden.")

if __name__ == "__main__":
    # Start motoren
    engine = AivoryRecruiter(JOB_PROFILE)
    
    # Kjør pipeline
    engine.load_candidates("bulk_applicants.csv") # Laster 250 stk
    engine.phase_1_hard_screening()               # Siler vekk støy
    engine.phase_2_ai_testing_and_scoring()       # Dybdeanalyse
    engine.phase_3_delivery()                     # Resultat
