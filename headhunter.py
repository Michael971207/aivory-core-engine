import streamlit as st
import sqlite3
import pandas as pd
import requests

st.set_page_config(page_title="Aivory Risk Monitor", page_icon="🚨", layout="wide")
API_URL = "http://127.0.0.1:8000"

def get_data():
    conn = sqlite3.connect('aivory_logs.db')
    try: df = pd.read_sql_query("SELECT * FROM logs ORDER BY tidspunkt DESC", conn)
    except: df = pd.DataFrame()
    conn.close()
    return df

df = get_data()

st.sidebar.title("Aivory Admin")
mode = st.sidebar.radio("Meny:", ["⚠️ Flight Risk", "📋 Oversikt"])

st.title("💼 Aivory Risk Management")

if mode == "⚠️ Flight Risk":
    st.header("Lojalitets-analyse")
    st.markdown("AI-en predikerer hvem som slutter tidlig basert på jobbhistorikk og personlighet.")
    
    if not df.empty and 'flight_risk' in df.columns:
        # Filtrer kun de som er anbefalt ANSETT
        hires = df[df['beslutning'] == 'ANSETT'].copy()
        
        if hires.empty:
            st.warning("Ingen ansettelser å analysere.")
        else:
            col1, col2, col3 = st.columns(3)
            high_risk = len(hires[hires['flight_risk'].str.contains("HØY", na=False)])
            safe = len(hires) - high_risk
            
            col1.metric("Anbefalte Kandidater", len(hires))
            col2.metric("Trygge valg", safe)
            col3.metric("Flight Risk (Fare)", high_risk, delta_color="inverse")
            
            st.markdown("### 🚨 Risiko-listen")
            for i, row in hires.iterrows():
                risk = row['flight_risk'] if row['flight_risk'] else "Ukjent"
                
                if "HØY" in risk:
                    st.error(f"⚠️ **{row['navn']}** ({row['stilling']})")
                    st.write(f"Risiko: {risk}")
                    st.caption("Årsak: Sannsynligvis historikk med hyppige jobbytter + rastløs personlighet.")
                elif "MEDIUM" in risk:
                    st.warning(f"✋ **{row['navn']}** - Risiko: {risk}")
                else:
                    st.success(f"✅ **{row['navn']}** - Risiko: {risk} (Lojal)")
                    
    else:
        st.info("Databasen mangler lojalitetsdata. Kjør nye tester via API/Portal.")

elif mode == "📋 Oversikt":
    st.dataframe(df)
