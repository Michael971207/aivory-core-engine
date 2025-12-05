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
    .stApp { background-color: #F8FAFC; color: #0f172a; font-family: 'Inter', sans-serif; }
    h1, h2, h3, h4 { color: #000000 !important; font-weight: 800; letter-spacing: -0.5px; }
    
    /* Dashboard Stat Card */
    .stat-card {
        background-color: #FFFFFF;
        padding: 25px;
        border-radius: 16px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        transition: 0.2s;
    }
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        border-color: #7c3aed;
    }
    .stat-value { font-size: 2.5rem; font-weight: 800; color: #0F172A; margin: 10px 0; }
    .stat-label { color: #64748B; font-size: 0.9rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; }
    .stat-delta { font-size: 0.9rem; font-weight: bold; }
    .delta-up { color: #10B981; background: #ECFDF5; padding: 2px 8px; border-radius: 12px; }
    .icon-box { float: right; background: #F3F4F6; padding: 10px; border-radius: 12px; font-size: 1.5rem; }

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

    /* Insight Panel */
    .insight-panel {
        background: #FFFFFF; padding: 25px; border-radius: 12px;
        border: 1px solid #E5E7EB; height: 100%; box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }

    /* Chat Elements */
    .chat-bubble-me {
        background-color: #7c3aed; color: white; padding: 10px 15px;
        border-radius: 15px 15px 0 15px; margin: 5px 0 5px auto;
        width: fit-content; max-width: 80%; font-size: 0.9rem;
    }
    .chat-bubble-other {
        background-color: #F1F5F9; color: black; padding: 10px 15px;
        border-radius: 15px 15px 15px 0; margin: 5px 0;
        width: fit-content; max-width: 80%; font-size: 0.9rem;
    }
    
    /* Booking Card Style */
    .booking-card {
        background: white; border: 1px solid #E5E7EB; padding: 15px;
        border-radius: 12px; margin: 10px 0 10px auto; width: 80%;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05); border-left: 5px solid #10B981;
    }
    .meet-link { color: #2563EB; text-decoration: underline; font-weight: bold; }

    /* SWOT Box */
    .swot-container {
        background-color: #000000; color: white; padding: 20px;
        border-radius: 10px; margin-top: 20px; border-left: 5px solid #7c3aed;
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

# Mock Jobs
if 'jobs' not in st.session_state:
    st.session_state.jobs = [
        {"Tittel": "Tech Lead", "Sted": "Oslo", "Type": "Hybrid", "Frist": "2025-06-01", "Status": "Aktiv", "Søkere": 12}, 
        {"Tittel": "Key Account Manager", "Sted": "Bergen", "Type": "On-site", "Frist": "2025-05-20", "Status": "Aktiv", "Søkere": 4},
        {"Tittel": "UX Designer", "Sted": "Remote", "Type": "Remote", "Frist": "2025-05-15", "Status": "Aktiv", "Søkere": 28},
    ]

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
        st.markdown("<br>", unsafe_allow_html=True)
        
        # --- PRO KPI CARDS ---
        k1, k2, k3, k4 = st.columns(4)
        
        with k1:
            st.markdown("""
            <div class="stat-card">
                <div class="icon-box">👥</div>
                <div class="stat-label">Total Talent Pool</div>
                <div class="stat-value">1,240</div>
                <span class="stat-delta delta-up">↑ 12% denne uken</span>
            </div>
            """, unsafe_allow_html=True)
            
        with k2:
            st.markdown("""
            <div class="stat-card">
                <div class="icon-box">🤖</div>
                <div class="stat-label">AI Matches</div>
                <div class="stat-value">24</div>
                <span class="stat-delta delta-up">↑ Høy Relevans</span>
            </div>
            """, unsafe_allow_html=True)
            
        with k3:
            st.markdown("""
            <div class="stat-card">
                <div class="icon-box">💬</div>
                <div class="stat-label">Intervjuer</div>
                <div class="stat-value">8</div>
                <span class="stat-delta delta-up">2 i dag</span>
            </div>
            """, unsafe_allow_html=True)
            
        with k4:
            st.markdown("""
            <div class="stat-card">
                <div class="icon-box">⚡</div>
                <div class="stat-label">Time-to-Hire</div>
                <div class="stat-value">14d</div>
                <span class="stat-delta delta-up">↓ 50% Raskere</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br><br>", unsafe_allow_html=True)

        # --- GRAF & TABELL ---
        col_main, col_side = st.columns([2, 1])
        
        with col_main:
            st.subheader("📈 Søkervekst per Stilling")
            # Lager data for grafen
            chart_data = pd.DataFrame(st.session_state.jobs).set_index("Tittel")[["Søkere"]]
            st.bar_chart(chart_data, color="#7c3aed")
            
            st.markdown("### 📋 Aktive Stillinger")
            st.dataframe(pd.DataFrame(st.session_state.jobs), use_container_width=True, hide_index=True)

        with col_side:
            st.subheader("🔔 Siste Hendelser")
            st.info("Erik S. godtok videointervju (10 min siden)")
            st.info("Ny kandidat matchet 'Tech Lead' (1t siden)")
            st.success("Stilling 'UX Designer' publisert.")
            
            with st.container(border=True):
                st.markdown("**AI Tips:**")
                st.caption("Du har 3 nye kandidater i 'Tech Lead' pipelinen som scorer over 90%. Bør sjekkes i dag.")
                if st.button("Gå til kandidater"):
                    pass # Navigasjon logikk her

    elif menu == "Legg ut stilling":
        st.title("Ny Stilling")
        with st.form("job_form"):
            c1, c2 = st.columns([2, 1])
            with c1: tittel = st.text_input("Stillingstittel", placeholder="Eks. Senior Fullstack Utvikler")
            with c2: sted = st.text_input("Sted / By", placeholder="Eks. Oslo")
            
            c3, c4, c5 = st.columns(3)
            with c3: arbeidssted = st.selectbox("Kontor Type", ["On-site (Oppmøte)", "Hybrid", "Remote (Hjemmekontor)"])
            with c4: ansettelse = st.selectbox("Ansettelsesform", ["Fulltid", "Deltid", "Konsulent / Prosjekt", "Sommerjobb"])
            with c5: frist = st.date_input("Søknadsfrist", value=date.today() + timedelta(days=30))
            
            skills = st.multiselect("Nøkkelkvalifikasjoner", ["Python", "React", "Sales", "Leadership", "AWS", "Design"], default=[])
            beskrivelse = st.text_area("Beskrivelse", height=150)
            
            if st.form_submit_button("Publiser Stilling"):
                if tittel:
                    st.session_state.jobs.append({"Tittel": tittel, "Sted": sted, "Type": arbeidssted.split()[0], "Frist": str(frist), "Status": "Aktiv", "Søkere": 0})
                    st.success("Stilling publisert!")
                    time.sleep(1)
                    st.rerun()

    elif menu == "Headhunter Søk":
        st.title("🔍 Active Sourcing")
        
        c_search, c_btn = st.columns([3, 1])
        with c_search: st.text_input("Søk i talentbasen...", placeholder="F.eks. Python, Oslo...")
        with c_btn:
            st.write("") 
            if st.button("🏆 Vis Topp 10"): st.session_state.top_10_mode = True
        
        st.markdown("---")
        
        col_list, col_detail = st.columns([1.5, 2])
        
        # LISTE
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
                status_icon = "🔒" if not is_unlocked else "💬"
                
                st.markdown(f"""
                <div class="cand-card">
                    <div style="display:flex; justify-content:space-between;">
                        <b>{status_icon} {name}</b>
                        <span class="match-badge">{c['match']}%</span>
                    </div>
                    <p style="color:#6B7280; font-size:0.9rem; margin:0;">{c['rolle']} @ {comp}</p>
                    <div style="margin-top:10px;">{' '.join([f'<span class="tag">{s}</span>' for s in c['skills']])}</div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Velg ➡️", key=f"btn_{cid}"):
                    st.session_state.active_candidate = c

        # DETALJER
        with col_detail:
            if st.session_state.active_candidate:
                cand = st.session_state.active_candidate
                cid = cand['id']
                status = st.session_state.consent_state.get(cid, "none")
                is_unlocked = (status == "accepted")
                header_name = cand['navn'] if is_unlocked else "🔒 Anonym Profil"
                
                st.markdown(f"""
                <div class="insight-panel">
                    <h2 style="margin-top:0;">{header_name}</h2>
                    <p style="font-size:1.1rem; color:#7c3aed;">{cand['rolle']}</p>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
<div class="swot-container">
<h4 style="color:white !important; margin-top:0;">🤖 AI SWOT ANALYSE</h4>
<div style="margin-bottom:8px;">✅ <b>Strengths:</b> {cand['swot']['S']}</div>
<div style="margin-bottom:8px;">⚠️ <b>Weaknesses:</b> {cand['swot']['W']}</div>
<div style="margin-bottom:8px;">🚀 <b>Opportunities:</b> {cand['swot']['O']}</div>
<div style="margin-bottom:8px;">🛡️ <b>Threats:</b> {cand['swot']['T']}</div>
</div>
""", unsafe_allow_html=True)

                if status == "none":
                    st.write("")
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
                    st.markdown("### 💬 Dialog")
                    chat_container = st.container(height=300)
                    history = st.session_state.chat_history.get(cid, [])
                    with chat_container:
                        for msg in history:
                            if msg.get('type') == 'booking_card':
                                st.markdown(f"""<div class="booking-card"><h4>📅 Videoinvitasjon</h4><p><a href="{msg['link']}" class="meet-link" target="_blank">Klikk her for å bli med</a></p></div>""", unsafe_allow_html=True)
                            else:
                                div_class = "chat-bubble-me" if msg['role'] == "me" else "chat-bubble-other"
                                st.markdown(f"<div class='{div_class}'>{msg['msg']}</div>", unsafe_allow_html=True)
                    
                    with st.expander("📅 Book Møte"):
                        if st.button("Send Link"):
                            history.append({"role": "me", "type": "booking_card", "link": generate_meet_link()})
                            st.session_state.chat_history[cid] = history
                            st.rerun()
                    
                    new_msg = st.chat_input("Skriv melding...")
                    if new_msg:
                        history.append({"role": "me", "msg": new_msg})
                        st.session_state.chat_history[cid] = history
                        st.rerun()
                
                st.markdown("</div>", unsafe_allow_html=True)

            else:
                st.info("👈 Velg en kandidat.")

# --- 5. MAIN ---
if st.session_state.logged_in:
    render_dashboard()
else:
    render_login()
