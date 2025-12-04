# --- AIVORY MASTER CONTROL SCRIPT (V3) ---
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

# 1. Sjekk systemkrav (La til fastapi og uvicorn)
Print-Step "STEG 1: Sjekker systemkrav..."
pip install scikit-learn pandas matplotlib fastapi uvicorn --quiet
Check-Success

# 2. Generer data
Print-Step "STEG 2: Genererer data..."
python generate_history.py
Check-Success

# 3. Tren modellen
Print-Step "STEG 3: Trener AI-modellen..."
python train_brain.py
Check-Success

# 4. Forklar modellen
Print-Step "STEG 4: Analyserer logikk..."
python explain_brain.py
Check-Success

# 5. Ferdig
Print-Step "KLAR! For å starte serveren, kjør: uvicorn api:app --reload"
