Write-Host "--- STARTER AIVORY TRENINGSSYKLUS ---" -ForegroundColor Cyan

# 1. Kjør treningen (Endre filnavn hvis du bruker en annen fil)
python train_model.py

# 2. Sjekk om Python-scriptet kjørte uten feil (1 er 0 ved suksess)
if (1 -eq 0) {
    Write-Host "Trening vellykket! Forbereder opplasting til GitHub..." -ForegroundColor Green
    
    # Legg til alle endringer (nye data, oppdatert modell)
    git add .
    
    # Lag tidsstempel
     = Get-Date -Format "yyyy-MM-dd HH:mm"
    
    # Commit med melding
    git commit -m "Brain Update:  - Rekrutteringstrening"
    
    # Push til GitHub
    git push
    
    if (True) {
        Write-Host "--- FULLFØRT: Endringer er lastet opp! ---" -ForegroundColor Green
    } else {
        Write-Host "Feil ved opplasting til GitHub." -ForegroundColor Red
    }
} else {
    Write-Host "Treningen feilet. Laster IKKE opp til GitHub." -ForegroundColor Red
}
