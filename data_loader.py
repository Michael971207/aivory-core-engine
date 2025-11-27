import csv
import os

def load_training_data(filename="training_data.csv"):
    if not os.path.exists(filename):
        print(f"⚠️ Fant ikke filen: {filename}")
        return []

    dataset = []
    print(f"📂 Leser data fra {filename}...")
    
    with open(filename, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                data_point = {
                    "cv_snippet": row["cv_text"],
                    "job_snippet": row["job_desc"],
                    "score": float(row["score"]),
                    "reasoning": row["reasoning"]
                }
                dataset.append(data_point)
            except ValueError:
                print(f"   ❌ Hoppet over ugyldig rad: {row}")

    print(f"   ✅ Lastet inn {len(dataset)} unike innsikter.")
    return dataset
