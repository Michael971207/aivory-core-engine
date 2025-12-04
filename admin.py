import streamlit as st
import sqlite3
import pandas as pd
import time

# --- OPPSETT ---
st.set_page_config(page_title="Aivory Admin", page_icon="🛡️", layout="wide")

st.title("🛡️ Aivory Command Center")
st.markdown("Overvåker sanntidsdata fra **Aivory API Node 1**")

# --- KOBLING TIL DATABASE ---
def get_data():
    try:
        conn = sqlite3.connect('aivory_logs.db')
        df = pd.read_sql_query("SELECT * FROM logs ORDER BY tidspunkt DESC", conn)
        conn.close()
        return df
    except:
        return pd.DataFrame()

# Knapp for å oppdatere manuelt (eller vi kan la den auto-refreshe)
if st.button("🔄 Oppdater data"):
    st.rerun()

# Hent data
df = get_data()

if df.empty:
    st.warning("Ingen data i loggen enda. Kjør test_api.ps1!")
else:
    # --- TOPPSTATISTIKK (KPI-er) ---
    col1, col2, col3, col4 = st.columns(4)
    
    total = len(df)
    ansatt = len(df[df['beslutning'] == 'ANSETT'])
    avvist = total - ansatt
    rate = (ansatt / total) * 100
    
    col1.metric("Totalt Vurdert", total)
    col2.metric("Anbefalt Ansettelse", ansatt, delta=f"{rate:.1f}% rate")
    col3.metric("Avvist", avvist, delta_color="inverse")
    
    # Regn ut gjennomsnittlig score
    avg_score = df['score'].mean()
    col4.metric("Snitt Kvalitet (Score)", f"{avg_score:.1f}%")

    st.markdown("---")

    # --- GRAFER ---
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("Beslutningsfordeling")
        st.bar_chart(df['beslutning'].value_counts())
        
    with c2:
        st.subheader("Kandidat Kvalitet over Tid")
        # Vi trenger bare score-kolonnen for linjediagrammet
        st.line_chart(df['score'].tolist())

    # --- RAW DATA TABELL ---
    st.subheader("📋 Siste Aktivitet (Live Logg)")
    
    # Vi farger tabellen basert på beslutning
    def color_decision(val):
        color = '#d4edda' if val == 'ANSETT' else '#f8d7da' # Grønn eller Rød bakgrunn
        return f'background-color: {color}'

    st.dataframe(
        df.style.applymap(color_decision, subset=['beslutning']),
        use_container_width=True
    )

    # --- EKSPORT ---
    st.download_button(
        label="📥 Last ned Rapport (CSV)",
        data=df.to_csv(index=False).encode('utf-8'),
        file_name='aivory_full_report.csv',
        mime='text/csv',
    )
