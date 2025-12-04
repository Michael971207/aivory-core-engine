$ApiUrl = "http://127.0.0.1:8000/predict_hiring"

$Kandidater = @(
    @{ Navn = "Jens (Daglig leder)"; Erfaring = 15; Struktur = 10; Driv = 10; Samarbeid = 10; Skill_Match = 90 },
    @{ Navn = "Mona (Sommerhjelp)";  Erfaring = 0;  Struktur = 6;  Driv = 8;  Samarbeid = 9;  Skill_Match = 60 },
    @{ Navn = "Espen (Hacker)";      Erfaring = 5;  Struktur = 2;  Driv = 9;  Samarbeid = 1;  Skill_Match = 99 }
)

Write-Host "--- SENDER KANDIDATER TIL DATABASE-LOGGEN ---" -ForegroundColor Cyan

foreach ($Person in $Kandidater) {
    Write-Host "Behandler $($Person.Navn)..." -NoNewline

    try {
        # Nå sender vi HELE personen inkludert Navn
        $Response = Invoke-RestMethod -Uri $ApiUrl -Method Post -Body ($Person | ConvertTo-Json) -ContentType "application/json" -ErrorAction Stop
        
        if ($Response.anbefaling -eq "ANSETT") {
            Write-Host " -> ANSETT ✅" -ForegroundColor Green
        } else {
            Write-Host " -> AVVIS ⛔" -ForegroundColor Red
        }

    } catch {
        Write-Host " FEIL! Serveren svarer ikke." -ForegroundColor Red
    }
    Start-Sleep -Seconds 1
}
Write-Host "`nAlle data er nå lagret trygt i 'aivory_logs.db'!" -ForegroundColor Yellow
