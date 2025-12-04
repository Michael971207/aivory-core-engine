$ApiUrl = "http://127.0.0.1:8000/predict_hiring"

$Kandidater = @(
    @{ 
        Navn = "Kandidat A (Papegøyen)"; 
        Erfaring = 5; Struktur = 5; Driv = 5; Samarbeid = 5; Skill_Match = 80;
        Soknadstekst = "Python. Machine Learning. AI. Koding. Data." 
    },
    @{ 
        Navn = "Kandidat B (Den Ekte Utvikleren)"; 
        Erfaring = 5; Struktur = 5; Driv = 5; Samarbeid = 5; Skill_Match = 80;
        Soknadstekst = "Jeg har bygget avanserte nevrale nettverk og trives med å løse komplekse problemer i backend. Jeg tar eierskap til leveransene mine." 
    }
)

Write-Host "--- SEMANTISK AI TEST (FORSTÅELSE) ---" -ForegroundColor Cyan

foreach ($Person in $Kandidater) {
    Write-Host "`nAnalyserer $($Person.Navn)..." -NoNewline
    
    try {
        $jsonPayload = $Person | ConvertTo-Json -Depth 10
        $Response = Invoke-RestMethod -Uri $ApiUrl -Method Post -Body $jsonPayload -ContentType "application/json" -ErrorAction Stop
        
        Write-Host " [OK]" -ForegroundColor Green
        Write-Host "   Total Score: $($Response.total_score)%" -ForegroundColor Yellow
        Write-Host "   -> Mening-Match: $($Response.analyse.semantisk_match)%" -ForegroundColor Cyan
        
        if ($Response.anbefaling -eq "ANSETT") {
            Write-Host "   KONKLUSJON: ANSETT ✅" -ForegroundColor Green
        } else {
            Write-Host "   KONKLUSJON: AVVIS ⛔" -ForegroundColor Red
        }

    } catch {
        Write-Host " [FEIL]" -ForegroundColor Red
        if ($_.Exception.Response) {
             $Reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
             Write-Host "   SERVER SA: $($Reader.ReadToEnd())" -ForegroundColor Red
        }
    }
}
