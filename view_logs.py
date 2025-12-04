import sqlite3
import pandas as pd

# Koble til databasen
try:
    conn = sqlite3.connect('aivory_logs.db')
    
    # Les alt innholdet
    df = pd.read_sql_query("SELECT * FROM logs", conn)
    
    if df.empty:
        print("Loggen er tom.")
    else:
        print("\n--- AIVORY MASTER LOGG (DATABASE) ---")
        print(df.to_string(index=False))
        print("-" * 50)
        print(f"Totalt antall vurderinger lagret: {len(df)}")
        
    conn.close()
except:
    print("Finner ingen database enda.")
