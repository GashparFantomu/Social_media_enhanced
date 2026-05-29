import { useEffect } from 'react';
import { useNavigate, useParams, useSearchParams } from 'react-router-dom';

export default function Callback() {
  const { platform } = useParams(); // va fi 'linkedin' sau 'facebook'
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();

  useEffect(() => {
    const code = searchParams.get('code');

    if (code) {
      // Trimitem codul către serverul Flask pentru a obține Token-ul final, real
      fetch(`http://localhost:5000/api/auth/${platform}/callback`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code: code })
      })
      .then(res => res.json())
      .then(data => {
        if (data.access_token) {
          // 🎉 Am primit token-ul real! Îl salvăm în browser
          localStorage.setItem(`${platform}_token`, data.access_token);

          // Dacă e Meta, putem folosi token-ul și pentru Threads în funcție de permisiuni
          if (platform === 'facebook') {
            localStorage.setItem('threads_token', data.access_token);
          }

          navigate('/dashboard'); // Îl trimitem direct să își vadă postările generate
        } else {
          alert('Eroare la preluarea token-ului de acces de la rețeaua socială.');
          navigate('/integrations');
        }
      })
      .catch(() => {
        alert('Eroare de comunicare cu serverul Flask în timpul autentificării.');
        navigate('/integrations');
      });
    }
  }, [platform, searchParams, navigate]);

  return (
    <div className="container text-center my-5 py-5 text-white">
      <div className="spinner-border text-primary mb-3" role="status"></div>
      <h3>Se securizează conexiunea cu {platform}...</h3>
      <p className="text-secondary">Te redirecționăm imediat.</p>
    </div>
  );
}