import json
import random
import time

class AIvoryTrainer:
    def __init__(self):
        self.training_data = []
        print("\n🤖 AIvory Lab startet. Laster inn unik logikk...")

    def add_unique_insight(self, cv_text, job_desc, match_score, reasoning):
        data_point = {
            "cv_snippet": cv_text,
            "job_snippet": job_desc,
            "score": match_score,
            "reasoning": reasoning
        }
        self.training_data.append(data_point)
        # Vi printer bare de første 50 tegnene for å holde loggen ren
        print(f"   ➕ Lærte nytt konsept: {reasoning[:60]}...")

    def simulate_training(self):
        print(f"\n🧠 Trener på {len(self.training_data)} datapunkter...")
        # Simulert prosess bar
        for i in range(1, 4):
            time.sleep(0.5)
            print(f"   ... Epoch {i}: Justerer synapser ({i*33}%)")
        print("✅ Ferdig! Modellen er nå 'fine-tuned' på din kunnskap.")

    def save_dataset(self):
        filename = "aivory_dataset.jsonl"
        with open(filename, 'w', encoding='utf-8') as f:
            for entry in self.training_data:
                json.dump(entry, f)
                f.write('\n')
        print(f"\n💾 Kunnskap lagret i '{filename}'.")

if __name__ == "__main__":
    trainer = AIvoryTrainer()

    # --- EKSEMPEL 1: Hovmesteren (Soft Skills) ---
    trainer.add_unique_insight(
        cv_text="Hovmester, 10 år. Høyt tempo, klagehåndtering, team-koordinering.",
        job_desc="Junior Prosjektleder. Stressmestring og mange baller i luften.",
        match_score=0.85,
        reasoning="MATCH: Stressmestring fra restaurantbransjen er direkte overførbart til prosjektledelse."
    )

    # --- EKSEMPEL 2: Solo-utvikleren (Kulturkrasj) ---
    trainer.add_unique_insight(
        cv_text="Senior utvikler, 20 år. Jobbet alene på eget system i 15 år.",
        job_desc="Team-lead i startup. Krever parprogrammering og smidig metodikk.",
        match_score=0.40,
        reasoning="MISMATCH: Kandidaten er vant til å jobbe alene (silo), mens jobben krever ekstremt samarbeid."
    )

    # --- EKSEMPEL 3: 'Jobb-hopperen' (Læringsvillig) ---
    # En vanlig AI ville sett negativt på korte arbeidsforhold. Vi ser potensialet.
    trainer.add_unique_insight(
        cv_text="3 jobber på 4 år. Har lært React, Vue og Svelte på kort tid i ulike byråer.",
        job_desc="Konsulent. Må kunne sette seg inn i ny tech raskt ute hos kunde.",
        match_score=0.90,
        reasoning="MATCH: Mange jobbytter indikerer her høy tilpasningsdyktighet og læringsvilje, perfekt for konsulenter."
    )

    # --- EKSEMPEL 4: Den Overkvalifiserte (Kjedsomhet) ---
    # En vanlig AI ville tenkt "Mye erfaring = Bra". Vi ser risikoen for at de slutter.
    trainer.add_unique_insight(
        cv_text="CTO med 15 års erfaring, ledet avdeling på 50 pers.",
        job_desc="Enkel frontend-koding av landingssider.",
        match_score=0.30,
        reasoning="RISIKO: Kandidaten er grovt overkvalifisert og vil sannsynligvis kjede seg og slutte raskt."
    )

    trainer.simulate_training()
    trainer.save_dataset()
