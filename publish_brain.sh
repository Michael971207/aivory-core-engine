#!/bin/bash

# 1. Kjør treningen først
python train_model.py

# 2. Last opp resultatet til GitHub
echo "--------------------------------------"
echo "☁️  Laster opp ny hjernemasse til GitHub..."
git add training_data.csv aivory_dataset.jsonl
git commit -m "Brain Update: $(date "+%Y-%m-%d %H:%M")"
git push origin main

echo "✅ Ferdig! Din unike AI er lagret trygt i skyen."
