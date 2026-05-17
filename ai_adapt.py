import json
import google.generativeai as genai

# Înlocuiește cu cheia ta reală din Google AI Studio
genai.configure(api_key="CHEIA_TA_GEMINI")


def adapteaza_continut(master_post):
    """Adaptează textul pentru LinkedIn și X folosind AI."""
    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt = f"""
    Ești un expert în social media marketing. Adaptează următorul "Master Post" pentru:
    - LinkedIn: Ton profesional, 3-4 hashtag-uri, extinde ideea pentru zona de business.
    - X (Twitter): Concis, de impact, ton dinamic, maxim 280 de caractere.

    Master Post:
    "{master_post}"

    Returnează rezultatul EXCLUSIV în format JSON, cu această structură exactă (fără blocuri markdown precum json):
    {{
        "linkedin": "textul pentru linkedin aici",
        "x": "textul pentru twitter aici"
    }}
    """

    try:
        response = model.generate_content(prompt)
        rezultat_curat = response.text.strip().replace('json', '').replace('```', '')
        return json.loads(rezultat_curat)
    except Exception as e:
        print(f"Eroare AI: {e}")
        return None