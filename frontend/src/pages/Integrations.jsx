import { useState } from 'react';

export default function Integrations() {
  const [connections, setConnections] = useState(() => ({
    linkedin: !!localStorage.getItem('linkedin_token'),
    facebook: !!localStorage.getItem('facebook_token'),
    x: !!localStorage.getItem('x_token'),
    threads: !!localStorage.getItem('threads_token'),
  }));

  const handleConnect = (platform) => {
    if (connections[platform]) {
      localStorage.removeItem(`${platform}_token`);
      setConnections(prev => ({
        ...prev,
        [platform]: false
      }));
    } else {
      if (platform === 'linkedin') {
        const clientId = "AICI_PUI_CLIENT_ID_UL_REAL";
        const redirectUri = encodeURIComponent("http://localhost:5173/callback/linkedin");
        const scope = "w_member_social";

        window.location.assign(`https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=${clientId}&redirect_uri=${redirectUri}&scope=${scope}&state=randomsecret123`);
      }
      else if (platform === 'facebook') {
        const clientId = "AICI_PUI_CLIENT_ID_UL_REAL_META";
        const redirectUri = encodeURIComponent("http://localhost:5173/callback/facebook");
        const scope = "pages_manage_posts,pages_read_engagement";

        window.location.assign(`https://www.facebook.com/v18.0/dialog/oauth?client_id=${clientId}&redirect_uri=${redirectUri}&scope=${scope}`);
      }
      else if (platform === 'x' || platform === 'threads') {
        const mockTokenValue = "mock_token_demo_123";
        localStorage.setItem(`${platform}_token`, mockTokenValue);

        setConnections(prev => ({
          ...prev,
          [platform]: true
        }));
      }
    }
  };

  return (
    <div className="container py-4">
      <h2 className="text-white mb-4">🔑 Conectează Rețelele Tale Sociale</h2>
      <p className="text-secondary mb-4">Apasă pe butoanele de mai jos pentru a acorda aplicației permisiunea de a posta automat în numele tău.</p>

      <div className="row g-4">
        {[
          { id: 'linkedin', name: 'LinkedIn', color: 'btn-outline-info', icon: '🟦' },
          { id: 'facebook', name: 'Facebook', color: 'btn-outline-primary', icon: '🔷' },
          { id: 'x', name: 'X (Twitter)', color: 'btn-outline-light', icon: '⬛' },
          { id: 'threads', name: 'Threads', color: 'btn-outline-secondary', icon: '🧬' }
        ].map(platform => (
          <div className="col-md-6" key={platform.id}>
            <div className="p-4 rounded bg-dark border border-secondary d-flex justify-content-between align-items-center">
              <div>
                <h4 className="text-white mb-1">{platform.icon} {platform.name}</h4>
                <small className={connections[platform.id] ? "text-success" : "text-muted"}>
                  {connections[platform.id] ? "● Conectat corect" : "○ Neconectat"}
                </small>
              </div>
              <button
                onClick={() => handleConnect(platform.id)}
                className={`btn ${connections[platform.id] ? 'btn-danger' : platform.color}`}
              >
                {connections[platform.id] ? 'Deconectează' : 'Conectează'}
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}