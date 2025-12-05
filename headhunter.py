import streamlit as st
import pandas as pd
import time
import random

# --- 1. CONFIG ---
st.set_page_config(
    page_title="Aivory Enterprise", 
    page_icon="🏢", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- 2. DESIGN SYSTEM (Violet/Black High-End) ---
st.markdown("""
<style>
    .stApp { background-color: #FFFFFF; color: #000000; font-family: 'Inter', sans-serif; }
    h1, h2, h3, h4 { color: #000000 !important; font-weight: 800; letter-spacing: -0.5px; }
    
    /* Login Box */
    .auth-box {
        max-width: 450px; margin: 0 auto; padding: 40px;
        background: white; border: 1px solid #E5E7EB; border-radius: 16px;
        box-shadow: 0 20px 50px rgba(0,0,0,0.08); text-align: center;
    }

    /* Candidate Card */
    .cand-card {
        background: white; border: 1px solid #E5E7EB; padding: 20px;
        border-radius: 12px; margin-bottom: 10px; transition: 0.2s;
        cursor: pointer;
    }
    .cand-card:hover {
        border-color: #7c3aed; transform: translateX(5px);
        box-shadow: 0 5px 15px rgba(124, 58, 237, 0.1);
    }

    /* Insight Panel (Right) */
    .insight-panel {
        background: #F9FAFB; padding: 25px; border-radius: 12px;
        border: 1px solid #E5E7EB; height: 100%;
    }

    /* SWOT Box */
    .swot-box {
        background: #000000; color: white; padding: 20px;
        border-radius: 10px; margin-top: 20px; border-left: 5px solid #7c3aed;
    }
    .swot-item { margin-bottom: 8px; font-size: 0.9rem; }
    
    /* Tags & Badges */
    .tag { background: #F3F4F6; padding: 3px 8px; border-radius: 4px; font-size: 0.8rem; margin-right: 5px; color: #333; }
    .match-badge { background: #dcfce7; color: #166534; padding: 4px 10px; border-radius: 12px; font-weight: bold; font-size: 0.8rem; }

    /* Buttons */
    div.stButton > button {
        background-color: #7c3aed; color: white; border: none;
        padding: 0.6rem 1.5rem; border-radius: 8px; font-weight: 700; width: 100%;
    }
    div.stButton > button:hover { background-color: #6d28d9; }
</style>
""", unsafe_allow_html=True)

# --- 3. STATE & DATA INITIALIZATION (CRITICAL FIX) ---
if 'logged_in' not in st.session_state: 
    st.session_state.logged_in = False

if 'active_candidate' not in st.session_state: 
    st.session_state.active_candidate = None

if 'company_name' not in st.session_state:
    st.session_state.company_name = "Ukjent Bedrift"

# Mock Data - Lastes kun én gang
if 'candidates' not in st.session_state:
    st.session_state.candidates = [
        {
            "id": 1, "navn": "Erik Solberg", "rolle": "Senior Python Dev", "bedrift": "TechNova", 
            "match": 98, "skills": ["Python", "AWS", "Django"], 
            "swot": {"S": "Eksepsjonell kodekvalitet", "W": "Lite ledererfaring", "O": "Kan ta Tech Lead rolle", "T": "Høy lønnsforventning"}
        },
        {
            "id": 2, "navn": "Lisa Hansen", "rolle": "Sales Manager", "bedrift": "Bank 1", 
            "match": 92, "skills": ["B2B", "CRM", "Closing"], 
            "swot": {"S": "Top performer 2024", "W": "Utdatert CRM-kunnskap", "O": "Nye markeder", "T": "Vurderer konkurrent"}
        },
        {
            "id": 3, "navn": "Ahmed Khan", "rolle": "CFO", "bedrift": "Startup X", 
            "match": 85, "skills": ["Finance", "Strategy", "IPO"], 
            "swot": {"S": "IPO-erfaring", "W": "Kort fartstid i tech", "O": "Skalere økonomiavdeling", "T": "Krever opsjoner"}
        }
    ]

if 'jobs' not in st.session_state:
    st.session_state.jobs = [
        {"Tittel": "Tech Lead", "Status": "Aktiv", "Søkere": 12}, 
        {"Tittel": "Key Account Manager", "Status": "Aktiv", "Søkere": 4}
    ]

# --- 4. VIEWS ---

def render_login():
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        st.markdown("""
        <div class="auth-box">
            <h1 style="font-size: 3rem; margin-bottom: 0;">Aivory.</h1>
            <p style="color: #6B7280; margin-bottom: 20px;">Enterprise Headhunting Suite</p>
        </div>
        """, unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Logg Inn", "Registrer Bedrift"])
        
        with tab1:
            st.text_input("E-post", key="l_user", value="admin@aivory.no")
            st.text_input("Passord", type="password", key="l_pass", value="1234")
            if st.button("Logg inn"):
                st.session_state.logged_in = True
                st.session_state.company_name = "TechNova AS"
                st.rerun()
                
        with tab2:
            bedrift_navn = st.text_input("Bedriftsnavn")
            st.text_input("Admin E-post")
            st.text_input("Passord", type="password")
            if st.button("Opprett Bedriftsprofil"):
                st.session_state.logged_in = True
                st.session_state.company_name = bedrift_navn
                st.rerun()

def render_dashboard():
    # --- SIDEBAR ---
    with st.sidebar:
        st.title("🏢 Aivory")
        st.caption(f"Logget inn: {st.session_state.company_name}")
        st.markdown("---")
        menu = st.radio("Navigasjon", ["Oversikt", "Headhunter Søk (Active)", "Legg ut stilling"])
        st.markdown("---")
        if st.button("Logg ut"):
            st.session_state.logged_in = False
            st.session_state.active_candidate = None
            st.rerun()

    # --- CONTENT ---
    if menu == "Oversikt":
        st.title(f"Hei, {st.session_state.company_name} 👋")
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Kandidater i base", "1,240", "+12")
        c2.metric("AI-intervjuer", "14", "Denne uken")
        c3.metric("Åpne stillinger", str(len(st.session_state.jobs)), "Active")
        c4.metric("Avg. Match", "88%", "+2%")
        
        st.markdown("### 📋 Dine Aktive Stillinger")
        st.dataframe(pd.DataFrame(st.session_state.jobs), use_container_width=True, hide_index=True)

    elif menu == "Legg ut stilling":
        st.title("Ny Stilling")
        st.info("AI analyserer jobbeskrivelsen automatisk.")
        with st.form("job_form"):
            t = st.text_input("Stillingstittel")
            st.selectbox("Avdeling", ["Tech", "Salg", "Ledelse"])
            st.text_area("Beskrivelse", height=150)
            
            if st.form_submit_button("Publiser"):
                st.session_state.jobs.append({"Tittel": t, "Status": "Aktiv", "Søkere": 0})
                st.success(f"Stillingen '{t}' er publisert!")
                time.sleep(1)
                st.rerun()

    elif menu == "Headhunter Søk (Active)":
        st.title("🔍 Active Sourcing")
        
        col_list, col_detail = st.columns([1.5, 2])
        
        # LISTE (Venstre)
        with col_list:
            st.text_input("Søk i talentbasen...", placeholder="F.eks. Python, Oslo...")
            st.markdown(f"**Fant {len(st.session_state.candidates)} top matches:**")
            
            for c in st.session_state.candidates:
                # Kandidatkort
                st.markdown(f"""
                <div class="cand-card">
                    <div style="display:flex; justify-content:space-between;">
                        <b>{c['navn']}</b>
                        <span class="match-badge">{c['match']}% Match</span>
                    </div>
                    <p style="color:#6B7280; font-size:0.9rem; margin:0;">{c['rolle']} @ {c['bedrift']}</p>
                    <div style="margin-top:10px;">
                        {' '.join([f'<span class="tag">{s}</span>' for s in c['skills']])}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Unik nøkkel for hver knapp for å unngå DuplicateWidgetID error
                if st.button(f"Velg {c['navn']} ➡️", key=f"btn_select_{c['id']}"):
                    st.session_state.active_candidate = c

        # DETALJER (Høyre - The "Cool Stuff")
        with col_detail:
            if st.session_state.active_candidate:
                cand = st.session_state.active_candidate
                swot = cand['swot']
                
                st.markdown(f"""
                <div class="insight-panel">
                    <h2 style="margin-top:0;">{cand['navn']}</h2>
                    <p style="font-size:1.1rem; color:#7c3aed;">{cand['rolle']}</p>
                    
                    <div class="swot-box">
                        <h4 style="color:white !important; margin-top:0;">🤖 AI SWOT ANALYSE</h4>
                        <div class="swot-item">✅ <b>Strengths:</b> {swot['S']}</div>
                        <div class="swot-item">⚠️ <b>Weaknesses:</b> {swot['W']}</div>
                        <div class="swot-item">🚀 <b>Opportunities:</b> {swot['O']}</div>
                        <div class="swot-item">🛡️ <b>Threats:</b> {swot['T']}</div>
                    </div>
                    <br>
                </div>
                """, unsafe_allow_html=True)
                
                # DE KULE KNAPPENE
                c_btn1, c_btn2 = st.columns(2)
                with c_btn1:
                    if st.button("✨ Generer Melding"):
                        st.info(f"Hei {cand['navn']}, basert på din profil hos {cand['bedrift']}...")
                with c_btn2:
                    if st.button("🔓 Lås opp Kontaktinfo"):
                        st.success("E-post: skjult@talent.no (Ulåst!)")
                        
                st.button("📌 Lagre til Shortlist", type="primary")
                
            else:
                st.info("👈 Velg en kandidat fra listen til venstre.")

# --- 5. MAIN ---
if st.session_state.logged_in:
    render_dashboard()
else:
    render_login()
