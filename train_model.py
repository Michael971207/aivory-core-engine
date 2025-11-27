import time
import json
from data_loader import load_training_data

class AIvoryTrainer:
    def __init__(self):
        self.training_data = []
        print("\n🤖 AIvory Lab v2.0 startet.")

    def load_data(self):
        self.training_data = load_training_data("training_data.csv")

    def simulate_training(self):
        if not self.training_data:
            print("⚠️ Ingen data å trene på!")
            return

        print(f"\n🧠 Trener modell på {len(self.training_data)} scenarier...")
        for entry in self.training_data:
            score_percent = int(entry['score'] * 100)
            print(f"   Studerer case: {entry['reasoning'][:40]}... (Score: {score_percent}%)")
            time.sleep(0.1) 
        print("\n✅ Ferdig! Modellen er nå oppdatert med CSV-dataene.")

    def save_dataset(self):
        filename = "aivory_dataset.jsonl"
        with open(filename, 'w', encoding='utf-8') as f:
            for entry in self.training_data:
                json.dump(entry, f)
                f.write('\n')
        print(f"💾 Behandlet data lagret til '{filename}'.")

if __name__ == "__main__":
    trainer = AIvoryTrainer()
    trainer.load_data()
    trainer.simulate_training()
    trainer.save_dataset()
