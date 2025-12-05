import streamlit as st
import pandas as pd
import time
import random
from datetime import datetime

# --- 1. SYSTEM CONFIGURATION ---
st.set_page_config(
    page_title="Aivory Certify", 
    page_icon="⚡", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- 2. AIVORY MODERN DESIGN (Violet/Black/White) ---
st.markdown("""
<style>
    /* Base */
    .stApp { 
        background-color: #FFFFFF; 
        font-family: 'Inter', sans-serif; 
        color: #000000;
    }
    
    /* Typography */
    h1, h2, h3 { color: #000000 !important; font-weight: 800; letter-spacing: -0.5px; }
    p, label { color: #374151; }
    
    /* Workflow Steps (Wizard Card) */
    .step-container {
        background-color: #FFFFFF;
        padding: 40px;
        border-radius: 16px;
        border: 2px solid #F3F4F6;
        box-shadow: 0 10px 40px rgba(0,0,0,0.03);
        margin-bottom: 20px;
    }
    
    /* Upload Zone - High Visibility Violet */
    div[data-testid="stFileUploader"] {
        border: 2px dashed #7c3aed;
        border-radius: 12px;
        padding: 30px;
        background-color: #f5f3ff; /* Light Violet tint */
    }
    div[data-testid="stFileUploader"] section { background-color: transparent; }
    
    /* AI Insights Card (Dark Mode Contrast) */
    .ai-card {
        background-color: #000000;
        color: white;
        padding: 25px;
        border-radius: 12px;
        margin-bottom: 20px;
        border-left: 5px solid #7c3aed;
    }
    
    /* Buttons (Aivory Violet) */
    div.stButton > button {
        background-color: #7c3aed; 
        color: white;
        border: none;
        padding: 0.8rem 2rem;
        border-radius: 8px;
        font-weight: 700;
        font-size: 1rem;
        width: 100%;
        transition: 0.2s;
    }
    div.stButton > button:hover {
        background-color: #6d28d9; 
        box-shadow: 0 5px 15px rgba(124, 58, 237, 0.4);
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #FAFAFA;
        border-right: 1px solid #E5E7EB;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. DOMAIN KNOWLEDGE & EXAM CONTENT ---
SECTOR_EXAMS = {
    "Consulting": {
        "skills": ["Analytical Reasoning", "Case Solving", "Client Communication"],
        "question": "Client X taper 10% markedsandel årlig til tross for et voksende marked. Identifiser tre potensielle rotårsaker og en hypotese for verifisering."
    },
    "Finance": {
        "skills": ["Financial Modeling", "Risk Assessment", "Excel"],
        "question": "Beskriv hvordan du vil vurdere kredittverdigheten til et selskap med volatile kontantstrømmer i et høyrente-miljø."
    },
    "Law": {
        "skills": ["Compliance", "Contract Law", "Risk Mitigation"],
        "question": "En internasjonal klient står overfor anklager om GDPR-brudd. Skisser en strategi for de første 24 timene for å minimere juridisk risiko."
    },
    "Corporate": {
        "skills": ["Project Management", "Stakeholder Mgmt", "Strategy"],
        "question": "Du leder et tverrfaglig team som ligger bak skjema. Hvordan prioriterer du ressurser for å sikre at milepæler nås?"
    }
}

# --- 4. AI ENGINE (SIMULATED) ---
def ai_evaluate_candidate(cv_file, answer_text, sector):
    with st.spinner("Aivory Engine analyserer kompetanse..."):
        time.sleep(1.5) 
        
    base_score = random.randint(70, 95)
    
    return {
        "score": base_score,
        "match_grade": "Top Talent" if base_score > 90 else "Qualified",
        "red_flags": [],
        "screening_time": "0.3 sekunder"
    }

# --- 5. STATE MANAGEMENT ---
if 'role' not in st.session_state: st.session_state.role = 'Candidate'
if 'exam_stage' not in st.session_state: st.session_state.exam_stage = 1
if 'candidate_data' not in st.session_state: st.session_state.candidate_data = {}

# --- 6. CANDIDATE INTERFACE (Aivory Exam) ---
def render_candidate_portal():
    st.markdown("## ⚡ Aivory Certify")
    st.caption("Verifiser din kompetanse gjennom vår AI-drevne fagprøve.")

    # PROGRESS BAR (Violet)
    st.markdown(f"""
    <div style="background-color:#E5E7EB; height:8px; border-radius:4px; margin-bottom:30px;">
        <div style="background-color:#7c3aed; height:8px; border-radius:4px; width:{ (st.session_state.exam_stage / 3) * 100 }%;"></div>
    </div>
    """, unsafe_allow_html=True)

    # --- STAGE 1: DOCUMENT SUBMISSION ---
    if st.session_state.exam_stage == 1:
        with st.container():
            st.markdown("""
            <div class="step-container">
                <h3>Steg 1: Identifisering</h3>
                <p>For å låse opp den praktiske prøven, må vi verifisere profilen din med en CV.</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Fullt Navn")
                sector = st.selectbox("Velg Sertifiseringsspor", list(SECTOR_EXAMS.keys()))
            
            with col2:
                cv = st.file_uploader("Last opp CV / Resume (PDF)", type=['pdf', 'docx'])

            st.write("") # Spacer
            if cv and name:
                st.success("✅ Profil verifisert. Aivory Exam er ulåst.")
                if st.button("Start Praktisk Eksamen ➡️", type="primary"):
                    st.session_state.candidate_data = {"name": name, "sector": sector, "cv": cv}
                    st.session_state.exam_stage = 2
                    st.rerun()
            else:
                st.info("💡 Last opp CV for å gå videre.")

    # --- STAGE 2: PRACTICAL EXAM ---
    elif st.session_state.exam_stage == 2:
        sector = st.session_state.candidate_data['sector']
        exam_content = SECTOR_EXAMS[sector]
        
        with st.container():
            st.markdown(f"""
            <div class="step-container">
                <h3>Steg 2: Fagprøve - {sector}</h3>
                <p><b>Kompetansemål:</b> {', '.join(exam_content['skills'])}</p>
                <hr style="border-top: 1px solid #E5E7EB;">
                <h4>🧠 Case Oppgave:</h4>
                <p style="font-size:1.1rem; font-weight:500;">{exam_content['question']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            answer = st.text_area("Ditt svar:", height=250, placeholder="Strukturer svaret ditt tydelig her...")
            
            if st.button("Lever Besvarelse & Analyser"):
                if len(answer) < 20:
                    st.error("Svaret er for kort.")
                else:
                    result = ai_evaluate_candidate(st.session_state.candidate_data['cv'], answer, sector)
                    st.session_state.candidate_data.update({"answer": answer, "ai_result": result})
                    st.session_state.exam_stage = 3
                    st.rerun()

    # --- STAGE 3: COMPLETION ---
    elif st.session_state.exam_stage == 3:
        st.balloons()
        st.markdown("""
        <div class="step-container" style="text-align:center;">
            <h1 style="color:#7c3aed !important; font-size:3rem;">Fullført!</h1>
            <p>Din besvarelse er kryptert og sendt til Aivory Engine.</p>
            <br>
            <div style="background:#F3F4F6; padding:15px; border-radius:8px; display:inline-block;">
                <b>Forventet responstid:</b> < 24 timer
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Tilbake til Start"):
            st.session_state.exam_stage = 1
            st.rerun()

# --- 7. RECRUITER INTERFACE (Aivory Dashboard) ---
def render_recruiter_dashboard():
    st.markdown("## 🚀 Aivory Admin Dashboard")
    st.caption("Sanntidsinnsikt i kandidat-pipelinen.")

    # KPI SECTION
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Spart Screening-tid", "95%", "AI Automatisert")
    c2.metric("Respons-hastighet", "100x", "Instant Match")
    c3.metric("Søkere Behandlet", "100%", "Ingen kø")
    c4.metric("Top Talents", "14", "Siste 24t")

    st.markdown("---")

    # CANDIDATE LIST
    st.subheader("Kandidat Pipeline (Live)")
    
    data = [
        {"ID": "CAND-992", "Spor": "Finance", "Aivory Score": 96, "Status": "Anbefalt", "Skills": "Modeling, Excel"},
        {"ID": "CAND-841", "Spor": "Law", "Aivory Score": 92, "Status": "Anbefalt", "Skills": "GDPR, Risk"},
        {"ID": "CAND-331", "Spor": "Consulting", "Aivory Score": 88, "Status": "Vurderes", "Skills": "Strategy"},
        {"ID": "CAND-112", "Spor": "Corporate", "Aivory Score": 65, "Status": "Avvist", "Skills": "Mgmt"},
    ]
    df = pd.DataFrame(data)

    col_table, col_ai = st.columns([2, 1])

    with col_table:
        st.dataframe(df.style.highlight_max(axis=0, subset=['Aivory Score'], color='#f3e8ff'), use_container_width=True)

    with col_ai:
        st.markdown("""
        <div class="ai-card">
            <h4 style="color:white !important; margin-top:0;">🤖 Aivory Insight</h4>
            <p><b>CAND-992</b> viser eksepsjonell analytisk styrke i Finance-modulen.</p>
            <p style="color:#a78bfa;"><i>Anbefaling: Innkall til intervju umiddelbart.</i></p>
        </div>
        """, unsafe_allow_html=True)
        st.button("Lås opp Kontaktinfo (GDPR Logget)")

# --- 8. MAIN ROUTER ---
st.sidebar.title("Aivory Navigasjon")
mode = st.sidebar.radio("Visningsmodus", ["Kandidat Portal", "Rekrutterer Dashboard"])

if mode == "Kandidat Portal":
    render_candidate_portal()
else:
    render_recruiter_dashboard()

