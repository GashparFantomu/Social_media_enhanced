from flask import Flask, request, jsonify
from flask_cors import CORS
from ai_adapt import adapteaza_continut
from social_publish import publica_pe_x, publica_pe_linkedin, publica_pe_facebook, publica_pe_threads

app = Flask(__name__)
CORS(app)  # Permite conexiunea de la serverul de React (localhost:3000)


@app.route('/api/adapt', methods=['POST'])
def api_adapt():
    """Primește textul brut și cheia Gemini, returnează textele optimizate."""
    data = request.json
    master_post = data.get('master_post', '')
    gemini_key = data.get('gemini_key', '')

    if not master_post or not gemini_key:
        return jsonify({'error': 'Lipsesc date obligatorii'}), 400

    continut_generat = adapteaza_continut(master_post, gemini_key)
    if not continut_generat:
        return jsonify({'error': 'Eroare la generarea prin Gemini AI'}), 500

    return jsonify(continut_generat)


@app.route('/api/publish/linkedin', methods=['POST'])
def api_publish_linkedin():
    data = request.json
    text = data.get('text')
    token = data.get('token')
    urn = data.get('urn')

    if publica_pe_linkedin(text, token, urn):
        return jsonify({'status': 'success', 'message': 'Publicat pe LinkedIn'})
    return jsonify({'status': 'error', 'message': 'Eroare la publicare'}), 500


# Poti adauga rute similare pentru /api/publish/x, /api/publish/facebook etc.

if __name__ == '__main__':
    app.run(debug=True, port=5000)