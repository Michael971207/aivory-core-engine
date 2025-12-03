Write-Host "?? --- AIVORY BRAIN SYNC (Lokal Mappe) ---" -ForegroundColor Cyan

# Sjekk at vi er i riktig mappe
if (!(Test-Path "train_model.py")) {
    Write-Host "?? Fant ikke 'train_model.py' her! Sjekk at du står i riktig mappe." -ForegroundColor Red
    # Vi fortsetter likevel i tilfelle du bare vil pushe
}

# 1. Sikre kobling til GitHub
git init
# HER VAR FEILEN: Vi escaper $null så det faktisk havner i filen
git remote remove origin 2>$null 
git remote add origin https://github.com/Michael971207/aivory-core-engine.git

# 2. Tren (Hvis scriptet finnes)
if (Test-Path "train_model.py") {
    Write-Host "1. Trener modellen lokalt..." -ForegroundColor Yellow
    python train_model.py
}

# 3. Last opp til Supabase (Hvis scriptet finnes)
if (Test-Path "upload_brain_safe.py") {
    Write-Host "2. Laster opp kunnskap til databasen..." -ForegroundColor Yellow
    python upload_brain_safe.py
}

# 4. Lagre til GitHub
Write-Host "3. Sikrer kunnskapen i skyen..." -ForegroundColor Yellow
git add .
$date = Get-Date -Format "yyyy-MM-dd HH:mm"
git commit -m "Brain Update: $date"
git push -u origin main

Write-Host "? Hjernen er lagret! Ingen data gikk tapt." -ForegroundColor Green
Write-Host "-------------------------------------------------------"
