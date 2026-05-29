import { useState, useEffect } from 'react';

export default function Dashboard() {
  const [masterPost, setMasterPost] = useState('');
  const [geminiKey, setGeminiKey] = useState('');
  const [loading, setLoading] = useState(false);
  const [generatedContent, setGeneratedContent] = useState(null);

  // Stările pentru butoanele de publicare
  const [tokens, setTokens] = useState({});
  const [publishStatus, setPublishStatus] = useState({});

  useEffect(() => {
    setTokens({
      linkedin: localStorage.getItem('linkedin_token'),
      facebook: localStorage.getItem('facebook_token'),
      x: localStorage.getItem('x_token'),
      threads: localStorage.getItem('threads_token'),
    });

    const savedGemini = localStorage.getItem('gemini_key');
    if (savedGemini) setGeminiKey(savedGemini);
  }, []);

  const handleGeminiKeyChange = (e) => {
    setGeminiKey(e.target.value);
    localStorage.setItem('gemini_key', e.target.value);
  };

  const handleGenerate = async () => {
    if (!masterPost.trim() || !geminiKey.trim()) {
      alert('⚠️ Te rog să introduci textul brut și cheia Gemini AI!');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch('http://localhost:5000/api/adapt', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ master_post: masterPost, gemini_key: geminiKey })
      });

      const data = await response.json();
      if (response.ok) {
        // Presupunem că Gemini returnează { x: "...", linkedin: "..." }
        // Clonăm textele și pentru Facebook și Threads
        setGeneratedContent({
          x: data.x,
          linkedin: data.linkedin,
          facebook: data.linkedin, // Facebook preia formatul LinkedIn
          threads: data.x          // Threads preia formatul X
        });
      } else {
        alert(`❌ Eroare: ${data.error}`);
      }
    } catch (err) {
      alert('❌ Nu s-a putut contacta serverul backend (Flask). Este pornit?');
    } finally {
      setLoading(false);
    }
  };

  const handlePublish = async (platform, text) => {
    setPublishStatus(prev => ({ ...prev, [platform]: 'loading' }));

    try {
      const response = await fetch(`http://localhost:5000/api/publish/${platform}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          text: text,
          token: tokens[platform],
          // urn: "urn:li:person:..." -> Pentru LinkedIn, în producție îl luăm din profil. Îl simulăm acum.
          urn: 'urn:li:person:TEST_STUDENT'
        })
      });

      if (response.ok) {
        setPublishStatus(prev => ({ ...prev, [platform]: 'success' }));
      } else {
        setPublishStatus(prev => ({ ...prev, [platform]: 'error' }));
      }
    } catch (err) {
      setPublishStatus(prev => ({ ...prev, [platform]: 'error' }));
    }
  };

  return (
    <div className="container py-4">
      <h2 className="text-white mb-4">🧠 Panou de Control AI</h2>

      {/* Zonă Configurare Rapidă Gemini */}
      <div className="p-3 mb-4 rounded bg-dark border border-secondary">
        <label className="form-label text-secondary fw-bold">Cheie API Google Gemini</label>
        <input
          type="password"
          className="form-control bg-black text-white border-secondary"
          placeholder="Introdu cheia ta Gemini pentru a activa AI-ul..."
          value={geminiKey}
          onChange={handleGeminiKeyChange}
        />
      </div>

      {/* Zona de Input Text */}
      <div className="mb-4">
        <label className="form-label text-white fw-bold">Ce vrei să postezi astăzi?</label>
        <textarea
          className="form-control bg-dark text-white border-secondary"
          rows="4"
          placeholder="Scrie ideea ta brută aici (ex: Am terminat faza de design pentru proiectul de semestru)..."
          value={masterPost}
          onChange={(e) => setMasterPost(e.target.value)}
        ></textarea>
        <button
          onClick={handleGenerate}
          className="btn btn-primary mt-3 px-4 fw-bold"
          disabled={loading}
        >
          {loading ? '🧠 Se procesează cu AI...' : '✨ Adaptează Conținutul'}
        </button>
      </div>

      {/* Zona cu cele 4 Platforme */}
      {generatedContent && (
        <div className="row g-4 mt-2">
          {[
            { id: 'x', name: 'X (Twitter)', icon: '⬛', text: generatedContent.x },
            { id: 'linkedin', name: 'LinkedIn', icon: '🟦', text: generatedContent.linkedin },
            { id: 'facebook', name: 'Facebook', icon: '🔷', text: generatedContent.facebook },
            { id: 'threads', name: 'Threads', icon: '🧬', text: generatedContent.threads }
          ].map(platform => (
            <div className="col-md-6" key={platform.id}>
              <div className="card bg-dark border-secondary h-100">
                <div className="card-header border-secondary d-flex justify-content-between align-items-center bg-black">
                  <h5 className="text-white m-0">{platform.icon} {platform.name}</h5>
                  {!tokens[platform.id] && <span className="badge bg-warning text-black">Neconectat</span>}
                </div>
                <div className="card-body text-light">
                  <p className="card-text p-2 rounded bg-black border border-secondary" style={{ whiteSpace: 'pre-wrap' }}>
                    {platform.text}
                  </p>
                </div>
                <div className="card-footer border-secondary d-flex justify-content-between align-items-center bg-black">
                  <small className="text-muted">Gata de trimis</small>
                  <button
                    onClick={() => handlePublish(platform.id, platform.text)}
                    className={`btn btn-sm fw-bold ${
                      publishStatus[platform.id] === 'success' ? 'btn-success' :
                      publishStatus[platform.id] === 'error' ? 'btn-danger' : 'btn-info'
                    }`}
                    disabled={!tokens[platform.id] || publishStatus[platform.id] === 'loading'}
                  >
                    {publishStatus[platform.id] === 'loading' ? 'Se publică...' :
                     publishStatus[platform.id] === 'success' ? '✅ Publicat!' :
                     publishStatus[platform.id] === 'error' ? '❌ Eroare' : 'Trimite Postarea'}
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}