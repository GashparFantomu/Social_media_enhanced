import streamlit as st
from ai_adapt import adapteaza_continut
from social_publish import publica_pe_x, publica_pe_linkedin, publica_pe_facebook, publica_pe_threads

# Setări vizuale pentru pagină
st.set_page_config(page_title="AI Social Cross-Poster", page_icon="🚀", layout="wide")

# --- MENIU LATERAL PENTRU TOKEN-URI ---
with st.sidebar:
    st.header("🔑 Setări și Credențiale")
    st.markdown("Introdu cheile pentru a utiliza aplicația. Nimic nu se salvează permanent.")

    st.subheader("Google Gemini (AI)")
    gemini_api_key = st.text_input("Gemini API Key", type="password")

    st.subheader("Twitter (X)")
    x_api_key = st.text_input("X API Key", type="password")
    x_api_secret = st.text_input("X API Secret", type="password")
    x_access_token = st.text_input("X Access Token", type="password")
    x_access_secret = st.text_input("X Access Token Secret", type="password")

    st.subheader("LinkedIn")
    linkedin_token = st.text_input("Access Token LinkedIn", type="password")
    linkedin_urn = st.text_input("LinkedIn URN (ex: urn:li:person:12345)", type="password")

    st.subheader("Facebook")
    fb_token = st.text_input("Page Access Token Facebook", type="password")
    fb_page_id = st.text_input("Facebook Page ID", type="default")

    st.subheader("Threads (Meta)")
    threads_token = st.text_input("Threads Access Token", type="password")

# --- INTERFAȚA PRINCIPALĂ ---
st.title("🚀 AI Social Cross-Poster")
st.markdown("Acest instrument preia un mesaj brut și îl adaptează inteligent pentru mai multe platforme sociale.")

# Input-ul principal de la utilizator
master_post = st.text_area(
    "Introdu Master Post-ul aici:",
    height=150,
    placeholder="Ex: Echipa noastră organizează un nou laborator de tip Hackathon AI-First de 7 săptămâni..."
)

# Declanșarea fluxului la apăsarea butonului
if st.button("✨ Generează și Publică", type="primary"):
    if not master_post.strip():
        st.warning("⚠️ Te rog să introduci un text mai întâi!")
    elif not gemini_api_key:
        st.warning("⚠️ Te rog să introduci cheia API pentru Gemini în meniul din stânga!")
    else:
        with st.spinner("🧠 AI-ul analizează și adaptează conținutul..."):
            continut_generat = adapteaza_continut(master_post, gemini_api_key)

        if not continut_generat:
            st.error("❌ Eroare la generarea textului. Verifică logurile sau cheia API Gemini.")
        else:
            st.success("✅ Conținut generat cu succes!")
            text_x = continut_generat.get("x", "")
            text_linkedin = continut_generat.get("linkedin", "")

            # Structurarea pe 4 coloane egale pentru afișare clară
            col1, col2, col3, col4 = st.columns(4)

            # --- COLOANA 1: X (TWITTER) ---
            with col1:
                st.subheader("⬛ X (Twitter)")
                st.info(text_x)

                with st.spinner("Se publică pe X..."):
                    if not all([x_api_key, x_api_secret, x_access_token, x_access_secret]):
                        st.warning("Nu ai introdus credențialele pentru X. Postarea nu a fost publicată automat.")
                    else:
                        if publica_pe_x(text_x, x_api_key, x_api_secret, x_access_token, x_access_secret):
                            st.success("Publicat cu succes pe X!")
                        else:
                            st.error("Eroare la publicare pe X. Verifică logurile.")

            # --- COLOANA 2: LINKEDIN ---
            with col2:
                st.subheader("🟦 LinkedIn")
                st.info(text_linkedin)

                with st.spinner("Se publică pe LinkedIn..."):
                    if not all([linkedin_token, linkedin_urn]):
                        st.warning("Nu ai introdus credențialele pentru LinkedIn. Postarea nu a fost publicată automat.")
                    else:
                        if publica_pe_linkedin(text_linkedin, linkedin_token, linkedin_urn):
                            st.success("Publicat cu succes pe LinkedIn!")
                        else:
                            st.error("Eroare la publicare pe LinkedIn. Verifică logurile.")

            # --- COLOANA 3: FACEBOOK ---
            with col3:
                st.subheader("🔷 Facebook")
                st.info(text_linkedin)  # Se potrivește stilul mai lung și detaliat de la LinkedIn

                with st.spinner("Se publică pe Facebook..."):
                    if not all([fb_token, fb_page_id]):
                        st.warning("Nu ai introdus credențialele pentru Facebook. Postarea nu a fost publicată automat.")
                    else:
                        if publica_pe_facebook(text_linkedin, fb_token, fb_page_id):
                            st.success("Publicat cu succes pe Facebook!")
                        else:
                            st.error("Eroare la publicare pe Facebook. Verifică logurile.")

            # --- COLOANA 4: THREADS ---
            with col4:
                st.subheader("🧬 Threads")
                st.info(text_x)  # Se potrivește stilul scurt și dinamic de la X

                with st.spinner("Se publică pe Threads..."):
                    if not threads_token:
                        st.warning("Nu ai introdus credențialele pentru Threads. Postarea nu a fost publicată automat.")
                    else:
                        if publica_pe_threads(text_x, threads_token):
                            st.success("Publicat cu succes pe Threads!")
                        else:
                            st.error("Eroare la publicare pe Threads. Verifică logurile.")