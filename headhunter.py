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

# --- 2. DESIGN SYSTEM ---
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
        cursor: pointer; position: relative;
    }
    .cand-card:hover {
        border-color: #7c3aed; transform: translateX(5px);
        box-shadow: 0 5px 15px rgba(124, 58, 237, 0.1);
    }
    .blur-text { filter: blur(4px); user-select: none; opacity: 0.6; }

    /* Insight Panel */
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
    
    /* Buttons */
    div.stButton > button {
        background-color: #7c3aed; color: white; border: none;
        padding: 0.6rem 1.5rem; border-radius: 8px; font-weight: 700; width: 100%;
    }
    div.stButton > button:hover { background-color: #6d28d9; }
    
    /* Tags & Badges */
    .tag { background: #F3F4F6; padding: 3px 8px; border-radius: 4px; font-size: 0.8rem; margin-right: 5px; color: #333; }
    .match-badge { background: #dcfce7; color: #166534; padding: 4px 10px; border-radius: 12px; font-weight: bold; font-size: 0.8rem; }
</style>
""", unsafe_allow_html=True)

# --- 3. STATE & MOCK DATA ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'active_candidate' not in st.session_state: st.session_state.active_candidate = None
if 'unlocked_ids' not in st.session_state: st.session_state.unlocked_ids = []
if 'top_10_mode' not in st.session_state: st.session_state.top_10_mode = False

if 'candidates' not in st.session_state:
    # Genererer litt flere kandidater for "Topp 10" følelsen
    base_cands = [
        {"id": 1, "navn": "Erik Solberg", "rolle": "Senior Python Dev", "bedrift": "TechNova", "match": 98, "skills": ["Python", "AWS", "Django"], "swot": {"S": "Eksepsjonell kodekvalitet", "W": "Lite ledererfaring", "O": "Tech Lead rolle", "T": "Høy lønn"}},
        {"id": 2, "navn": "Lisa Hansen", "rolle": "Sales Manager", "bedrift": "Bank 1", "match": 92, "skills": ["B2B", "CRM", "Closing"], "swot": {"S": "Top performer", "W": "Utdatert CRM", "O": "Nye markeder", "T": "Vurderer konkurrent"}},
        {"id": 3, "navn": "Ahmed Khan", "rolle": "CFO", "bedrift": "Startup X", "match": 85, "skills": ["Finance", "Strategy", "IPO"], "swot": {"S": "IPO-erfaring", "W": "Kort fartstid", "O": "Skalere", "T": "Krever opsjoner"}},
        {"id": 4, "navn": "Maria Nilsen", "rolle": "UX Lead", "bedrift": "DesignByrået", "match": 81, "skills": ["Figma", "User Testing"], "swot": {"S": "Brukerfokusert", "W": "Lite teknisk", "O": "Bygge designsystem", "T": "Burnout-fare"}},
        {"id": 5, "navn": "Per Olsen", "rolle": "DevOps Engineer", "bedrift": "CloudCorp", "match": 76, "skills": ["Kubernetes", "Azure"], "swot": {"S": "Sertifisert", "W": "Dokumentasjon", "O": "Automatisering", "T": "Konsulenttilbud"}}
    ]
    # Dupliserer for å fylle listen
    st.session_state.candidates = base_cands + base_cands 

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
            st.text_input("E-post", key="l_u", value="admin@aivory.no")
            st.text_input("Passord", type="password", key="l_p", value="1234")
            if st.button("Logg inn"):
                st.session_state.logged_in = True
                st.rerun()

def render_dashboard():
    # SIDEBAR
    with st.sidebar:
        st.title("🏢 Aivory")
        menu = st.radio("Meny", ["Oversikt", "Headhunter Søk", "Legg ut stilling"])
        st.markdown("---")
        if st.button("Logg ut"):
            st.session_state.logged_in = False
            st.rerun()

    # CONTENT
    if menu == "Oversikt":
        st.title("Dashbord")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Kandidater", "850", "+12")
        c2.metric("Matcher", "24", "Høy")
        c3.metric("Meldinger", "8", "Sendt")
        c4.metric("Avg. Score", "88%", "+2%")
        st.info("Velg 'Headhunter Søk' i menyen for å finne kandidater.")

    elif menu == "Legg ut stilling":
        st.title("Ny Stilling")
        st.text_input("Tittel")
        st.text_area("Beskrivelse")
        st.button("Publiser")

    elif menu == "Headhunter Søk":
        st.title("🔍 Active Sourcing")
        
        # --- TOPP 10 KNAPP ---
        c_search, c_btn = st.columns([3, 1])
        with c_search:
            query = st.text_input("Søk i talentbasen...", placeholder="F.eks. Python, Oslo...")
        with c_btn:
            st.write("") # Spacer
            if st.button("🏆 Vis Topp 10 Kandidater"):
                st.session_state.top_10_mode = True
        
        st.markdown("---")
        
        col_list, col_detail = st.columns([1.5, 2])
        
        # --- LISTE (ANONYMISERT) ---
        with col_list:
            display_list = st.session_state.candidates
            
            if st.session_state.top_10_mode:
                st.success("✅ Viser topp 10 kandidater basert på AI-score.")
                display_list = sorted(display_list, key=lambda x: x['match'], reverse=True)[:10]

            for c in display_list:
                is_unlocked = c['id'] in st.session_state.unlocked_ids
                
                # Anonymiserings-logikk
                display_name = c['navn'] if is_unlocked else f"Kandidat-{c['id']} (Anonym)"
                display_comp = f"{c['bedrift']}" if is_unlocked else "Skjult Selskap"
                blur_style = "" if is_unlocked else "filter: blur(0px);" # Kan øke blur hvis ønskelig
                
                st.markdown(f"""
                <div class="cand-card">
                    <div style="display:flex; justify-content:space-between;">
                        <b style="{blur_style}">{display_name}</b>
                        <span class="match-badge">{c['match']}%</span>
                    </div>
                    <p style="color:#6B7280; font-size:0.9rem; margin:0;">{c['rolle']} @ {display_comp}</p>
                    <div style="margin-top:10px;">
                        {' '.join([f'<span class="tag">{s}</span>' for s in c['skills']])}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Velg {'Kandidat' if not is_unlocked else c['navn'].split()[0]} ➡️", key=f"btn_{c['id']}"):
                    st.session_state.active_candidate = c

        # --- DETALJER (SWOT & UNLOCK) ---
        with col_detail:
            if st.session_state.active_candidate:
                cand = st.session_state.active_candidate
                is_unlocked = cand['id'] in st.session_state.unlocked_ids
                swot = cand['swot']
                
                # Header Data
                name_header = cand['navn'] if is_unlocked else "🔒 Anonym Profil"
                comp_header = cand['bedrift'] if is_unlocked else "Nåværende arbeidsgiver skjult"
                
                st.markdown(f"""
                <div class="insight-panel">
                    <h2 style="margin-top:0;">{name_header}</h2>
                    <p style="font-size:1.1rem; color:#7c3aed;">{cand['rolle']} hos {comp_header}</p>
                    
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
                
                # ACTIONS
                c1, c2 = st.columns(2)
                with c1:
                    if not is_unlocked:
                        if st.button("🔓 Lås opp identitet (1 Credit)"):
                            st.session_state.unlocked_ids.append(cand['id'])
                            st.rerun()
                    else:
                        st.success("Identitet verifisert ✅")
                
                with c2:
                    if st.button("✨ Generer AI-melding"):
                        if is_unlocked:
                            st.info(f"Hei {cand['navn'].split()[0]}, jeg har en stilling som passer din profil...")
                        else:
                            st.warning("Du må låse opp profilen først!")

            else:
                st.info("👈 Velg en profil fra listen.")

# --- 5. MAIN ---
if st.session_state.logged_in:
    render_dashboard()
else:
    render_login()
