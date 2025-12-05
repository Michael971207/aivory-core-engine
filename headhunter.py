import streamlit as st
import sqlite3
import pandas as pd
import requests
import hashlib

st.set_page_config(page_title="Aivory Admin", page_icon="🪐", layout="wide")
API_URL = "http://127.0.0.1:8000"

st.markdown("""
<style>
    .stApp { background-color: #030014; color: #E2E8F0; }
    div[data-testid="stContainer"], .stDataFrame {
        background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 16px; padding: 20px;
    }
    div.stButton > button { background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%); color: white; border: none; border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

def get_data():
    conn = sqlite3.connect('aivory_logs.db')
    try: df = pd.read_sql_query("SELECT * FROM logs ORDER BY tidspunkt DESC", conn)
    except: df = pd.DataFrame()
    conn.close()
    return df

st.title("🪐 Aivory Command Center")

tab1, tab2 = st.tabs(["📥 Innboks", "🏗️ Jobb Admin"])

with tab1:
    df = get_data()
    if df.empty:
        st.warning("No candidates yet.")
    else:
        for i, row in df.iterrows():
            with st.container():
                c1, c2, c3, c4 = st.columns([2, 1, 2, 2])
                name_disp = row['navn'] if row['candidate_consent'] and row['company_consent'] else f"Kandidat-{row['id']}"
                
                c1.markdown(f"### {name_disp}")
                c1.caption(row['stilling'])
                c2.metric("Score", f"{row['score']}%")
                
                # Status Actions
                if not row['company_consent']:
                    if c3.button("Request Contact", key=f"req_{i}"):
                        requests.post(f"{API_URL}/update_consent", json={"navn": row['navn'], "who": "company", "action": True}); st.rerun()
                elif not row['candidate_consent']:
                    c3.info("Waiting for candidate...")
                else:
                    c3.success("Connected")
                    msg = c4.text_input("Chat", key=f"chat_{i}")
                    if c4.button("Send", key=f"snd_{i}"):
                        requests.post(f"{API_URL}/send_chat", json={"navn": row['navn'], "sender": "Bedrift", "message": msg})

with tab2:
    st.subheader("Create Job")
    with st.form("new"):
        t = st.text_input("Title")
        b = st.text_area("Desc")
        if st.form_submit_button("Publish"):
            requests.post(f"{API_URL}/create_job", json={"tittel": t, "beskrivelse": b})
            st.success("Published!")
