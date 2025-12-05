import streamlit as st
import pandas as pd
import random

# --- 1. CONFIG ---
st.set_page_config(
    page_title="Aivory Enterprise", 
    page_icon="🏢", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- 2. DESIGN ---
st.markdown("""
<style>
    .stApp { background-color: #FFFFFF; color: #000000; font-family: 'Inter', sans-serif; }
    h1, h2, h3 { color: #000000 !important; font-weight: 800; letter-spacing: -0.5px; }
    
    /* Sidebar */
    section[data-testid="stSidebar"] { background-color: #F9FAFB; border-right: 1px solid #E5E7EB; }
    
    /* Insight Panel */
    .insight-box {
        background-color: #000000; color: white; padding: 20px;
        border-radius: 12px; margin-bottom: 20px; border-left: 5px solid #7c3aed;
    }
    
    /* Buttons */
    div.stButton > button {
        background-color: #7c3aed; color: white; border: none;
        padding: 0.6rem 1.5rem; border-radius: 8px; font-weight: 700; width: 100%;
    }
    div.stButton > button:hover { background-color: #6d28d9; }
</style>
""", unsafe_allow_html=True)

# --- 3. DATA (FEILFRI STRUKTUR) ---
# Vi bruker en Pandas DataFrame for tabellen, som er mye mer robust enn dictionaries
def get_data():
    return pd.DataFrame([
        {"ID": "CAND-881", "Rolle": "Python Dev", "AI Score": 98, "Status": "Vurderes", "Erfaring": "5 år", "Sannsynlighet": "Høy"},
        {"ID": "CAND-332", "Rolle": "Sales Mgr", "AI Score": 94, "Status": "Ny", "Erfaring": "8 år", "Sannsynlighet": "Medium"},
        {"ID": "CAND-102", "Rolle": "CFO", "AI Score": 89, "Status": "Intervju", "Erfaring": "12 år", "Sannsynlighet": "Lav"},
        {"ID": "CAND-551", "Rolle": "UX Design", "AI Score": 76, "Status": "Avvist", "Erfaring": "3 år", "Sannsynlighet": "Høy"},
    ])

# --- 4. VIEW: BEDRIFT ---
def render_bedrift():
    # Sidebar Navigation
    st.sidebar.header("🏢 Aivory Enterprise")
    st.sidebar.markdown("Logget inn som: **Headhunter**")
    st.sidebar.markdown("---")
    
    menu = st.sidebar.radio("Meny", ["Oversikt", "Kandidatsøk (Active)", "Stillinger"])

    if menu == "Oversikt":
        st.title("Oversikt")
        
        # KPI
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Nye Søkere", "12", "+3")
        c2.metric("Screenet av AI", "100%", "Autopilot")
        c3.metric("Intervjuer", "4", "I dag")
        c4.metric("Time-to-Hire", "14 dager", "-50%")
        
        st.markdown("---")
        
        # HEADHUNTER SØK / LISTE
        c_list, c_detail = st.columns([2, 1])
        
        df = get_data()
        
        with c_list:
            st.subheader("🔥 Top Candidates (AI Filtered)")
            # Viser tabellen uten å kræsje på manglende nøkler
            st.dataframe(
                df.style.highlight_max(axis=0, subset=['AI Score'], color='#f3e8ff'), 
                use_container_width=True,
                hide_index=True
            )

        with c_detail:
            st.subheader("💡 AI Insight")
            # Vi hardkoder en "eksempel-analyse" for demo-formål, så den alltid virker
            st.markdown("""
            <div class="insight-box">
                <h4>Anbefaling: CAND-881</h4>
                <p>Denne profilen har perfekt match på tekniske krav (Python/AWS).</p>
                <br>
                <p style="color:#a78bfa; font-style:italic;">"AI beregner 85% sannsynlighet for at kandidaten takker ja til intervju."</p>
            </div>
            """, unsafe_allow_html=True)
            
            c_act1, c_act2 = st.columns(2)
            c_act1.button("Lås opp Kontaktinfo")
            c_act2.button("Send AI-Melding")

    elif menu == "Kandidatsøk (Active)":
        st.title("🔍 Active Sourcing")
        st.text_input("Søk etter kompetanse (f.eks. 'Java + Finans')", placeholder="Skriv søkeord...")
        st.info("Koble til LinkedIn Recruiter for å søke i 800M+ profiler.")

    elif menu == "Stillinger":
        st.title("💼 Åpne Stillinger")
        st.write("Her administrerer du aktive oppdrag.")

if __name__ == "__main__":
    render_bedrift()
