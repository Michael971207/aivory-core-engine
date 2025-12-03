# --- AIVORY MASTER CONTROL SCRIPT ---
$ErrorActionPreference = "Stop"

function Print-Step {
    param([string]$Message)
    Write-Host "`n==========================================" -ForegroundColor Cyan
    Write-Host " $Message" -ForegroundColor Cyan
    Write-Host "==========================================" -ForegroundColor Cyan
}

function Check-Success {
    if ($LastExitCode -ne 0) {
        Write-Host "`n❌ FEIL: Prosessen stoppet. Fiks feilen over og prøv igjen." -ForegroundColor Red
        exit
    }
}

# 1. Sjekk og installer biblioteker
Print-Step "STEG 1: Sjekker systemkrav (scikit-learn, pandas)..."
pip install scikit-learn pandas --quiet
Check-Success

# 2. Generer historiske data
Print-Step "STEG 2: Genererer historiske treningsdata..."
python generate_history.py
Check-Success

# 3. Tren modellen
Print-Step "STEG 3: Trener AI-modellen (Machine Learning)..."
python train_brain.py
Check-Success

# 4. Test modellen
Print-Step "STEG 4: Kjører live test på nye kandidater..."
python predict_candidate.py
Check-Success

# 5. Last opp til GitHub
Print-Step "STEG 5: Laster opp 'Hjernen' og koden til GitHub..."

$gitStatus = git status --porcelain
if ($gitStatus) {
    Write-Host "Endringer funnet. Starter opplasting..." -ForegroundColor Yellow
    
    git add .
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm"
    git commit -m "Aivory Auto-Update: $timestamp - Ny modell trent"
    
    git push
    
    if ($?) {
        Write-Host "`n✅ SUKSESS! Aivory er oppdatert og lagret i skyen." -ForegroundColor Green
    } else {
        Write-Host "`n❌ Feil ved opplasting til GitHub." -ForegroundColor Red
    }
} else {
    Write-Host "Ingen endringer å laste opp. Alt er oppdatert." -ForegroundColor Green
}

Print-Step "AIVORY SYKLUS FULLFØRT"
