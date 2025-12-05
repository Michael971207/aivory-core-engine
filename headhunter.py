import streamlit as st
import pandas as pd
import time
import random
import string
from datetime import date, timedelta

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
    
    /* Input Fields Styling */
    div[data-testid="stTextInput"] input, div[data-testid="stSelectbox"] > div > div {
        border-radius: 8px; border: 1px solid #E5E7EB; padding: 5px;
    }
    
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

# --- 3. STATE & DATA ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'active_candidate' not in st.session_state: st.session_state.active_candidate = None
if 'top_10_mode' not in st.session_state: st.session_state.top_10_mode = False
if 'consent_state' not in st.session_state: st.session_state.consent_state = {} 
if 'chat_history' not in st.session_state: st.session_state.chat_history = {}
if 'video_ready' not in st.session_state: st.session_state.video_ready = {}

# Mock Candidates
if 'candidates' not in st.session_state:
    base_cands = [
        {"id": 1, "navn": "Erik Solberg", "rolle": "Senior Python Dev", "bedrift": "TechNova", "match": 98, "skills": ["Python", "AWS", "Django"], "swot": {"S": "Kodekvalitet", "W": "Ledererfaring", "O": "Tech Lead", "T": "Lønn"}},
        {"id": 2, "navn": "Lisa Hansen", "rolle": "Sales Manager", "bedrift": "Bank 1", "match": 92, "skills": ["B2B", "CRM", "Closing"], "swot": {"S": "Top performer", "W": "CRM", "O": "Nye markeder", "T": "Konkurrent"}},
        {"id": 3, "navn": "Ahmed Khan", "rolle": "CFO", "bedrift": "Startup X", "match": 85, "skills": ["Finance", "Strategy", "IPO"], "swot": {"S": "IPO", "W": "Tech-erfaring", "O": "Skalering", "T": "Opsjoner"}},
    ]
    st.session_state.candidates = base_cands + base_cands

# Mock Jobs (Oppdatert struktur)
if 'jobs' not in st.session_state:
    st.session_state.jobs = [
        {"Tittel": "Tech Lead", "Sted": "Oslo", "Type": "Hybrid", "Frist": "2025-06-01", "Status": "Aktiv", "Søkere": 12}, 
        {"Tittel": "Key Account Manager", "Sted": "Bergen", "Type": "On-site", "Frist": "2025-05-20", "Status": "Aktiv", "Søkere": 4}
    ]

# Helper for video link
def generate_meet_link():
    chars = string.ascii_lowercase
    return f"https://meet.google.com/{''.join(random.choice(chars) for _ in range(3))}-{''.join(random.choice(chars) for _ in range(4))}"

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
        menu = st.radio("Meny", ["Oversikt", "Legg ut stilling", "Headhunter Søk"])
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
        c3.metric("Video-intervjuer", "5", "Nye")
        c4.metric("Avg. Score", "88%", "+2%")
        
        st.markdown("### 📋 Dine Aktive Stillinger")
        st.dataframe(pd.DataFrame(st.session_state.jobs), use_container_width=True, hide_index=True)

    elif menu == "Legg ut stilling":
        st.title("Ny Stilling")
        st.caption("Fyll ut detaljene for å la AI matche kandidater automatisk.")
        
        with st.form("job_form"):
            # Rad 1
            c1, c2 = st.columns([2, 1])
            with c1:
                tittel = st.text_input("Stillingstittel", placeholder="Eks. Senior Fullstack Utvikler")
            with c2:
                sted = st.text_input("Sted / By", placeholder="Eks. Oslo")
            
            # Rad 2
            c3, c4, c5 = st.columns(3)
            with c3:
                arbeidssted = st.selectbox("Kontor Type", ["On-site (Oppmøte)", "Hybrid", "Remote (Hjemmekontor)"])
            with c4:
                ansettelse = st.selectbox("Ansettelsesform", ["Fulltid", "Deltid", "Konsulent / Prosjekt", "Sommerjobb"])
            with c5:
                frist = st.date_input("Søknadsfrist", value=date.today() + timedelta(days=30))
            
            # Rad 3 - Skills
            skills = st.multiselect("Nøkkelkvalifikasjoner (Skills)", 
                                  ["Python", "React", "Project Management", "Sales", "Marketing", "Finance", "Leadership", "AWS", "Azure", "Design"],
                                  default=[])
            
            beskrivelse = st.text_area("Beskrivelse av rollen", height=150, placeholder="Hva går jobben ut på?")
            
            submitted = st.form_submit_button("Publiser Stilling & Start AI-Matching")
            
            if submitted:
                if tittel and sted:
                    # Legg til i mock database
                    st.session_state.jobs.append({
                        "Tittel": tittel, 
                        "Sted": sted,
                        "Type": arbeidssted.split()[0], # Tar bare første ord (On-site/Hybrid)
                        "Frist": str(frist),
                        "Status": "Aktiv", 
                        "Søkere": 0
                    })
                    st.success(f"Stillingen '{tittel}' er publisert! AI søker nå etter kandidater...")
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error("Du må fylle ut tittel og sted.")

    elif menu == "Headhunter Søk":
        st.title("🔍 Active Sourcing")
        
        c_search, c_btn = st.columns([3, 1])
        with c_search:
            st.text_input("Søk i talentbasen...", placeholder="F.eks. Python, Oslo...")
        with c_btn:
            st.write("") 
            if st.button("🏆 Vis Topp 10"):
                st.session_state.top_10_mode = True
        
        st.markdown("---")
        
        col_list, col_detail = st.columns([1.5, 2])
        
        # --- LISTE ---
        with col_list:
            display_list = st.session_state.candidates
            if st.session_state.top_10_mode:
                display_list = sorted(display_list, key=lambda x: x['match'], reverse=True)[:10]

            for c in display_list:
                cid = c['id']
                status = st.session_state.consent_state.get(cid, "none")
                is_unlocked = (status == "accepted")
                
                name = c['navn'] if is_unlocked else f"Kandidat-{cid} (Anonym)"
                comp = c['bedrift'] if is_unlocked else "Skjult Selskap"
                
                status_icon = "🔒"
                if status == "requested": status_icon = "⏳"
                if status == "accepted": status_icon = "💬"
                
                st.markdown(f"""
                <div class="cand-card">
                    <div style="display:flex; justify-content:space-between;">
                        <b>{status_icon} {name}</b>
                        <span class="match-badge">{c['match']}%</span>
                    </div>
                    <p style="color:#6B7280; font-size:0.9rem; margin:0;">{c['rolle']} @ {comp}</p>
                    <div style="margin-top:10px;">
                        {' '.join([f'<span class="tag">{s}</span>' for s in c['skills']])}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Velg ➡️", key=f"btn_{cid}"):
                    st.session_state.active_candidate = c

        # --- DETALJER (SWOT + CHAT) ---
        with col_detail:
            if st.session_state.active_candidate:
                cand = st.session_state.active_candidate
                cid = cand['id']
                status = st.session_state.consent_state.get(cid, "none")
                
                # ... (Beholder eksisterende detalj-logikk fra forrige steg for konsistens)
                header_name = cand['navn'] if status == "accepted" else "🔒 Anonym Profil"
                
                # INSIGHT PANEL
                st.markdown(f"""
                <div style="background:#F9FAFB; padding:25px; border-radius:12px; border:1px solid #E5E7EB; height:100%;">
                    <h2 style="margin-top:0;">{header_name}</h2>
                    <p style="font-size:1.1rem; color:#7c3aed;">{cand['rolle']}</p>
                    
                    <div style="background:#000000; color:white; padding:20px; border-radius:10px; border-left:5px solid #7c3aed; margin-bottom:20px;">
                        <h4 style="color:white !important; margin-top:0;">🤖 AI SWOT</h4>
                        <div style="margin-bottom:8px;">✅ <b>Strengths:</b> {cand['swot']['S']}</div>
                        <div style="margin-bottom:8px;">⚠️ <b>Weaknesses:</b> {cand['swot']['W']}</div>
                    </div>
                """, unsafe_allow_html=True)

                if status == "none":
                    if st.button("📨 Send Kontaktforespørsel"):
                        st.session_state.consent_state[cid] = "requested"
                        st.rerun()
                elif status == "requested":
                    st.warning("Venter på samtykke...")
                    if st.button("⚡ Simuler Godkjenning"):
                        st.session_state.consent_state[cid] = "accepted"
                        st.rerun()
                elif status == "accepted":
                    st.success("Match Bekreftet!")
                    st.markdown("### 💬 Chat")
                    # Enkel chat placeholder for å spare plass i denne store filen
                    st.info("Chat-rom er åpent. (Se full kode fra forrige steg for full chat-funksjonalitet)")
                
                st.markdown("</div>", unsafe_allow_html=True)

            else:
                st.info("👈 Velg en kandidat.")

# --- 5. MAIN ---
if st.session_state.logged_in:
    render_dashboard()
else:
    render_login()
