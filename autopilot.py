import sqlite3
import time
import datetime

print("🤖 AIVORY AUTOPILOT ACTIVATED")
print("Overvåker databasen for nye kandidater...")
print("-" * 40)

def run_autopilot():
    while True:
        try:
            conn = sqlite3.connect('aivory_logs.db')
            c = conn.cursor()
            
            # 1. Finn kandidater som venter (Status = NEW)
            c.execute("SELECT rowid, navn, score, stilling FROM logs WHERE status = 'NEW'")
            candidates = c.fetchall()
            
            if candidates:
                print(f"👀 Fant {len(candidates)} nye søknader. Analyserer...")
                
                for row in candidates:
                    cid, navn, score, stilling = row
                    score = float(score) if score else 0
                    
                    action = ""
                    new_status = "NEW"
                    
                    # --- AUTOPILOT LOGIKK ---
                    if score >= 80:
                        # Superkandidat! Inviter med en gang.
                        new_status = "INTERVIEW"
                        action = "AUTO-INVITE: Booket intervju (Score > 80)"
                        print(f"   🚀 {navn}: Høy score ({score}%) -> Inviterer automatisk!")
                        
                    elif score < 40:
                        # Dårlig match. Avslå høflig.
                        new_status = "REJECTED"
                        action = "AUTO-REJECT: Lav score (Score < 40)"
                        print(f"   ❌ {navn}: Lav score ({score}%) -> Sender avslag.")
                        
                    else:
                        # Mellomting. La mennesket bestemme.
                        new_status = "REVIEW" # Vent på sjefen
                        action = "PENDING: Trenger manuell vurdering."
                        print(f"   🤔 {navn}: Usikker ({score}%) -> Sendt til manuell sjekk.")
                    
                    # Oppdater databasen
                    c.execute("UPDATE logs SET status = ?, autopilot_action = ? WHERE rowid = ?", (new_status, action, cid))
                    conn.commit()
            
            conn.close()
            
        except Exception as e:
            print(f"Feil i autopilot: {e}")
            
        # Sov i 5 sekunder før neste sjekk
        time.sleep(5)

if __name__ == "__main__":
    run_autopilot()
