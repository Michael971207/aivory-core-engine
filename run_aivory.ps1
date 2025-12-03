# --- AIVORY MASTER CONTROL SCRIPT (V2) ---
$ErrorActionPreference = "Stop"

function Print-Step {
    param([string]$Message)
    Write-Host "`n==========================================" -ForegroundColor Cyan
    Write-Host " $Message" -ForegroundColor Cyan
    Write-Host "==========================================" -ForegroundColor Cyan
}

function Check-Success {
    if ($LastExitCode -ne 0) {
        Write-Host "`n❌ FEIL: Prosessen stoppet." -ForegroundColor Red
        exit
    }
}

# 1. Sjekk systemkrav
Print-Step "STEG 1: Sjekker systemkrav..."
pip install scikit-learn pandas matplotlib --quiet
Check-Success

# 2. Generer historiske data
Print-Step "STEG 2: Genererer historiske treningsdata..."
python generate_history.py
Check-Success

# 3. Tren modellen
Print-Step "STEG 3: Trener AI-modellen..."
python train_brain.py
Check-Success

# 4. FORKLAR modellen (Nytt steg!)
Print-Step "STEG 4: Analyserer AI-ens logikk (Explainable AI)..."
python explain_brain.py
Check-Success

# 5. Test modellen
Print-Step "STEG 5: Kjører live test på nye kandidater..."
python predict_candidate.py
Check-Success

# 6. Last opp til GitHub
Print-Step "STEG 6: Laster opp til GitHub..."
$gitStatus = git status --porcelain
if ($gitStatus) {
    git add .
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm"
    git commit -m "Aivory Update: $timestamp - La til Explainable AI"
    git push
    if ($?) { Write-Host "✅ Lagret i skyen!" -ForegroundColor Green }
} else {
    Write-Host "Alt er oppdatert." -ForegroundColor Green
}

Print-Step "SYKLUS FULLFØRT"
