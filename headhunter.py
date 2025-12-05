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

    /* Insight Panel */
    .insight-panel {
        background: #F9FAFB; padding: 25px; border-radius: 12px;
        border: 1px solid #E5E7EB; height: 100%;
    }

    /* Chat Bobler */
    .chat-bubble-me {
        background-color: #7c3aed; color: white; padding: 10px 15px;
        border-radius: 15px 15px 0 15px; margin: 5px 0 5px auto;
        width: fit-content; max-width: 80%;
    }
    .chat-bubble-other {
        background-color: #E5E7EB; color: black; padding: 10px 15px;
        border-radius: 15px 15px 15px 0; margin: 5px 0;
        width: fit-content; max-width: 80%;
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
if 'top_10_mode' not in st.session_state: st.session_state.top_10_mode = False

# Lagrer tilstand for samtykke og chat per kandidat
if 'consent_state' not in st.session_state: st.session_state.consent_state = {} 
if 'chat_history' not in st.session_state: st.session_state.chat_history = {}

if 'candidates' not in st.session_state:
    base_cands = [
        {"id": 1, "navn": "Erik Solberg", "rolle": "Senior Python Dev", "bedrift": "TechNova", "match": 98, "skills": ["Python", "AWS", "Django"], "swot": {"S": "Kodekvalitet", "W": "Ledererfaring", "O": "Tech Lead", "T": "Lønn"}},
        {"id": 2, "navn": "Lisa Hansen", "rolle": "Sales Manager", "bedrift": "Bank 1", "match": 92, "skills": ["B2B", "CRM", "Closing"], "swot": {"S": "Top performer", "W": "CRM", "O": "Nye markeder", "T": "Konkurrent"}},
        {"id": 3, "navn": "Ahmed Khan", "rolle": "CFO", "bedrift": "Startup X", "match": 85, "skills": ["Finance", "Strategy", "IPO"], "swot": {"S": "IPO", "W": "Tech-erfaring", "O": "Skalering", "T": "Opsjoner"}},
        {"id": 4, "navn": "Maria Nilsen", "rolle": "UX Lead", "bedrift": "DesignByrået", "match": 81, "skills": ["Figma", "User Testing"], "swot": {"S": "Brukerfokus", "W": "Koding", "O": "Designsystem", "T": "Tidspress"}},
    ]
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
        c3.metric("Aktive Chatter", "3", "Nye")
        c4.metric("Avg. Score", "88%", "+2%")
        st.info("Gå til 'Headhunter Søk' for å finne talenter.")

    elif menu == "Legg ut stilling":
        st.title("Ny Stilling")
        st.text_input("Tittel")
        st.text_area("Beskrivelse")
        st.button("Publiser")

    elif menu == "Headhunter Søk":
        st.title("🔍 Active Sourcing")
        
        c_search, c_btn = st.columns([3, 1])
        with c_search:
            query = st.text_input("Søk i talentbasen...", placeholder="F.eks. Python, Oslo...")
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
                # Sjekk status i vår consent_state dict
                status = st.session_state.consent_state.get(cid, "none") # none, requested, accepted
                
                is_unlocked = (status == "accepted")
                
                # Visning
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

        # --- DETALJER (CHAT & SAMTYKKE) ---
        with col_detail:
            if st.session_state.active_candidate:
                cand = st.session_state.active_candidate
                cid = cand['id']
                status = st.session_state.consent_state.get(cid, "none")
                
                # Header
                is_unlocked = (status == "accepted")
                header_name = cand['navn'] if is_unlocked else "🔒 Anonym Profil"
                
                st.markdown(f"""
                <div class="insight-panel">
                    <h2 style="margin-top:0;">{header_name}</h2>
                    <p style="font-size:1.1rem; color:#7c3aed;">{cand['rolle']}</p>
                """, unsafe_allow_html=True)
                
                # --- LOGIKK FOR SAMTYKKE ---
                if status == "none":
                    st.info("Denne profilen er anonym. Du må sende en forespørsel for å opprette kontakt.")
                    st.markdown("### 🤖 AI SWOT")
                    st.write(f"✅ Styrker: {cand['swot']['S']}")
                    st.write(f"⚠️ Svakheter: {cand['swot']['W']}")
                    
                    st.write("")
                    if st.button("📨 Send Kontaktforespørsel (Gi Samtykke)"):
                        st.session_state.consent_state[cid] = "requested"
                        st.rerun()

                elif status == "requested":
                    st.warning("⏳ Venter på samtykke fra kandidat...")
                    st.markdown(f"**{cand['navn']}** har mottatt din forespørsel. Når de godkjenner, åpnes chatten.")
                    
                    st.markdown("---")
                    st.caption("(Demo-funksjon: Simuler at kandidaten svarer)")
                    if st.button("⚡ Simuler: Kandidat Godkjenner"):
                        st.session_state.consent_state[cid] = "accepted"
                        # Start chat med en melding
                        st.session_state.chat_history[cid] = [
                            {"role": "other", "msg": f"Hei! Takk for interessen. Jeg tar gjerne en prat om stillingen hos dere."}
                        ]
                        st.rerun()

                elif status == "accepted":
                    st.success("✅ Match! Begge parter har gitt samtykke.")
                    
                    # CHAT UI
                    st.markdown("### 💬 Chat")
                    chat_container = st.container(height=300)
                    
                    # Hent historikk
                    history = st.session_state.chat_history.get(cid, [])
                    
                    with chat_container:
                        for msg in history:
                            div_class = "chat-bubble-me" if msg['role'] == "me" else "chat-bubble-other"
                            st.markdown(f"<div class='{div_class}'>{msg['msg']}</div>", unsafe_allow_html=True)
                    
                    # Input
                    new_msg = st.chat_input("Skriv en melding...")
                    if new_msg:
                        history.append({"role": "me", "msg": new_msg})
                        st.session_state.chat_history[cid] = history
                        st.rerun()
                
                st.markdown("</div>", unsafe_allow_html=True) # End insight-panel

            else:
                st.info("👈 Velg en profil for å starte.")

# --- 5. MAIN ---
if st.session_state.logged_in:
    render_dashboard()
else:
    render_login()
