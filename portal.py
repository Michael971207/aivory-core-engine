import streamlit as st
import requests
import pypdf

st.set_page_config(page_title="Aivory Portal", page_icon="🧠", layout="centered")
API_URL = "http://127.0.0.1:8000/predict_hiring"

JOB_DATABASE = {
    "Senior AI Utvikler": "Vi søker en ekspert på Python, Machine Learning og AI.",
    "Salgssjef": "Vi trenger en energisk leder som kan drive nysalg."
}

st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2083/2083213.png", width=80)
st.sidebar.title("Karriere")
selected_job = st.radio("Stilling:", list(JOB_DATABASE.keys()))
job_desc = JOB_DATABASE[selected_job]

st.title(f"Søknad: {selected_job}")
st.info(job_desc)

# PDF LESER
auto_text = ""
uploaded_file = st.file_uploader("Last opp CV (PDF)", type="pdf")
if uploaded_file:
    try:
        reader = pypdf.PdfReader(uploaded_file)
        for page in reader.pages: auto_text += page.extract_text() + "\n"
        st.success("CV lest!")
    except: pass

with st.form("app_form"):
    navn = st.text_input("Navn", "Ditt Navn")
    erfaring = st.slider("Erfaring", 0, 20, 5)
    c1, c2, c3 = st.columns(3)
    s = c1.number_input("Struktur", 1, 10, 5)
    d = c2.number_input("Driv", 1, 10, 5)
    sam = c3.number_input("Samarbeid", 1, 10, 5)
    
    st.markdown("**Søknadstekst**")
    tekst = st.text_area("Tekst", value=auto_text, height=150)
    
    submit = st.form_submit_button("Send Søknad 🚀")

if submit:
    payload = {
        "Navn": navn, "Erfaring": int(erfaring), "Struktur": int(s), "Driv": int(d), "Samarbeid": int(sam), "Skill_Match": 80,
        "Jobb_Hopping": 1, "Soknadstekst": tekst, "StillingTittel": selected_job, "JobbBeskrivelse": job_desc
    }
    
    with st.spinner("Sjekker mot bedriftens strategi..."):
        try:
            res = requests.post(API_URL, json=payload)
            if res.status_code == 200:
                data = res.json()
                st.markdown("---")
                
                # VIS KUNNSKAPS-MATCH
                strat = data['kunnskap']
                score = data['analyse']['strategi_match']
                
                st.subheader("🏢 Bedrifts-kultur Match")
                
                if score > 40:
                    st.success(f"🔥 WOW! Du matcher vår interne strategi ({score}%)!")
                    if strat['treff']:
                        st.write("Du nevnte våre fokusområder:")
                        for t in strat['treff']: st.markdown(f"- **{t.upper()}**")
                else:
                    st.warning(f"Greit nok ({score}%), men du kjenner ikke vår interne strategi så godt enda.")
                    st.caption("Tips: Vi er opptatt av 'Rust', 'Serverless' og 'Åpenhet'.")
                
                st.metric("Total Score", f"{data['total_score']}%")
                if data['anbefaling'] == "ANSETT": st.balloons()
                
            else: st.error("Serverfeil")
        except Exception as e: st.error(f"Ingen kontakt: {e}")
