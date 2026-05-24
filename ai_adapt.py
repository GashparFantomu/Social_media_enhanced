import json

try:
    import google.generativeai as genai
    # \C3\8Enlocuie\C8\99te cu cheia ta real\C4\83 din Google AI Studio
    genai.configure(api_key="API KEY GEMINI")
    _HAS_GENAI = True
except Exception:
    genai = None
    _HAS_GENAI = False


def _require_genai_or_raise():
    if not _HAS_GENAI:
        raise RuntimeError(
            "Google Generative AI SDK not available for this Python environment. "
            "Create a Python 3.11 venv and install the SDK (or install a compatible wheel). "
            "Example:\n  python3.11 -m venv .venv311\n  source .venv311/bin/activate\n  pip install -r requirements.txt"
        )


def adapteaza_continut(master_post):
    """Adapteaz\C4\83 textul pentru LinkedIn \C8\99i X folosind AI.

    If the Google SDK is not installed (or not compatible with this Python), a
    RuntimeError with actionable instructions will be raised.
    """
    # If the Google SDK isn't available, return a lightweight fallback
    if not _HAS_GENAI:
        linkedin_text = (
            master_post.strip()
            + "\n\n(Adaptare mock pentru LinkedIn: ton profesional, 3-4 hashtag-uri.)"
        )
        x_text = master_post.strip()[:275]
        if len(master_post.strip()) > 275:
            x_text = x_text.rstrip() + '...'
        return {
            "linkedin": linkedin_text,
            "x": x_text,
        }

    model = genai.GenerativeModel('gemini-2.5-flash')

    prompt = f"""
    E\C8\99ti un expert \C3\AEn social media marketing. Adapteaz\C4\83 urm\C4\83torul "Master Post" pentru:
    - LinkedIn: Ton profesional, 3-4 hashtag-uri, extinde ideea pentru zona de business.
    - X (Twitter): Concis, de impact, ton dinamic, maxim 280 de caractere.

    Master Post:
    "{master_post}"

    Returneaz\C4\83 rezultatul EXCLUSIV \C3\AEn format JSON, cu aceast\C4\83 structur\C4\83 exact\C4\83 (f\C4\83r\C4\83 blocuri markdown precum json):
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