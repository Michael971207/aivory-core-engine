$ApiUrl = "http://127.0.0.1:8000/predict_hiring"

# Vi bruker engelsk i teksten for sikkerhets skyld for å unngå æ/ø/å-krøll i første omgang
$Kandidater = @(
    @{ 
        Navn = "Kandidat A"; 
        Erfaring = 3; Struktur = 5; Driv = 5; Samarbeid = 5; Skill_Match = 50;
        Soknadstekst = "Hei, jeg vil ha jobb." 
    },
    @{ 
        Navn = "Kandidat B"; 
        Erfaring = 3; Struktur = 5; Driv = 5; Samarbeid = 5; Skill_Match = 50;
        Soknadstekst = "Jeg har ledet prosjekter og er en ekspert pa Python og AI." 
    }
)

Write-Host "--- AIVORY FEILSØKING ---" -ForegroundColor Cyan

foreach ($Person in $Kandidater) {
    Write-Host "`nSender $($Person.Navn)..." -NoNewline
    
    try {
        # ConvertTo-Json -Depth 10 sikrer at strukturen blir riktig
        $jsonPayload = $Person | ConvertTo-Json -Depth 10
        
        $Response = Invoke-RestMethod -Uri $ApiUrl -Method Post -Body $jsonPayload -ContentType "application/json" -ErrorAction Stop
        
        Write-Host " [OK]" -ForegroundColor Green
        Write-Host "   Score: $($Response.total_score)%" -ForegroundColor Yellow
        Write-Host "   Melding: $($Response.melding)" -ForegroundColor Gray

    } catch {
        Write-Host " [FEIL]" -ForegroundColor Red
        
        # HER ER MAGIEN: Vi henter ut den faktiske feilmeldingen fra serveren
        if ($_.Exception.Response) {
            $Stream = $_.Exception.Response.GetResponseStream()
            $Reader = New-Object System.IO.StreamReader($Stream)
            $ErrorBody = $Reader.ReadToEnd()
            Write-Host "   SERVER SA: $ErrorBody" -ForegroundColor Red
        } else {
            Write-Host "   Klarte ikke koble til. Kjører serveren?" -ForegroundColor Red
        }
    }
}
