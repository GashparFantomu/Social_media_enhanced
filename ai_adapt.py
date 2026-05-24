import json

try:
    import google.generativeai as genai

    _HAS_GENAI = True
except Exception:
    genai = None
    _HAS_GENAI = False


def adapteaza_continut(master_post, api_key):
    """Adaptează textul pentru LinkedIn și X folosind AI-ul Gemini."""

    if not _HAS_GENAI:
        # Fallback dacă SDK-ul Google nu este instalat corect
        linkedin_text = master_post.strip() + "\n\n(Adaptare mock pentru LinkedIn: ton profesional, 3-4 hashtag-uri.)"
        x_text = master_post.strip()[:275]
        if len(master_post.strip()) > 275:
            x_text = x_text.rstrip() + '...'
        return {"linkedin": linkedin_text, "x": x_text}

    try:
        # Configurăm Gemini cu cheia primită de la utilizator în interfață
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')

        prompt = f"""
        Ești un expert în social media marketing. Adaptează următorul "Master Post" pentru:
        - LinkedIn: Ton profesional, 3-4 hashtag-uri, extinde ideea pentru zona de business.
        - X (Twitter): Concis, de impact, ton dinamic, maxim 280 de caractere.

        Master Post:
        "{master_post}"

        Returnează rezultatul EXCLUSIV în format JSON, cu această structură exactă (fără blocuri markdown precum ```json):
        {{
            "linkedin": "textul pentru linkedin aici",
            "x": "textul pentru twitter aici"
        }}
        """

        response = model.generate_content(prompt)
        # Curățăm rezultatul ca să putem extrage JSON-ul pur
        rezultat_curat = response.text.strip().replace('```json', '').replace('```', '')
        return json.loads(rezultat_curat)

    except Exception as e:
        print(f"Eroare AI: {e}")
        return None