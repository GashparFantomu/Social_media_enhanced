import streamlit as st
from ai_adapt import adapteaza_continut
from social_publish import publica_pe_x, publica_pe_linkedin

# Setări vizuale pentru pagină
st.set_page_config(page_title="AI Social Cross-Poster", page_icon="🚀", layout="wide")

st.title("🚀 AI Social Cross-Poster")
st.markdown("Acest instrument preia un mesaj brut și îl adaptează inteligent pentru LinkedIn și X.")

# Input-ul principal de la utilizator
master_post = st.text_area(
    "Introdu Master Post-ul aici:",
    height=150,
    placeholder="Ex: Echipa noastră organizează un nou laborator de tip Hackathon AI-First de 7 săptămâni..."
)

# Declanșarea fluxului la apăsarea butonului
if st.button("✨ Generează și Publică", type="primary"):
    if not master_post.strip():
        st.warning("Te rog să introduci un text mai întâi!")
    else:
        # Adaptarea cu AI
        with st.spinner("🧠 AI-ul analizează și adaptează conținutul..."):
            continut_generat = adapteaza_continut(master_post)

        if not continut_generat:
            st.error("❌ Eroare la generarea textului. Verifică logurile sau cheia API.")
        else:
            st.success("✅ Conținut generat cu succes!")
            text_x = continut_generat.get("x", "")
            text_linkedin = continut_generat.get("linkedin", "")

            # Structurarea pe coloane pentru afișare clară
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("⬛ X (Twitter)")
                st.info(text_x)

                with st.spinner("Se publică pe X..."):
                    if publica_pe_x(text_x):
                        st.success("Publicat cu succes pe X!")
                    else:
                        st.error("Eroare la publicare pe X. Verifică logurile.")

            with col2:
                st.subheader("🟦 LinkedIn")
                st.info(text_linkedin)

                with st.spinner("Se publică pe LinkedIn..."):
                    if publica_pe_linkedin(text_linkedin):
                        st.success("Publicat cu succes pe LinkedIn!")
                    else:
                        st.error("Eroare la publicare pe LinkedIn. Verifică logurile.")