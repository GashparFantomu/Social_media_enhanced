import { Link } from 'react-router-dom';

export default function Home() {
  return (
    <div className="container text-center my-5 py-5">
      <h1 className="display-4 fw-bold text-white mb-3">Distribuie conținutul inteligent, peste tot.</h1>
      <p className="lead text-secondary mb-4 mx-auto" style={{ maxWidth: '600px' }}>
        Scrie un singur text brut. Inteligența Artificială îl va optimiza automat pentru specificul fiecărei platforme și îl va publica instantaneu.
      </p>
      <div className="d-grid gap-3 d-sm-flex justify-content-sm-center">
        <Link to="/dashboard" className="btn btn-primary btn-lg px-4 gap-3">Mergi la Dashboard</Link>
        <Link to="/integrations" className="btn btn-outline-secondary btn-lg px-4">Configurează Integrări</Link>
      </div>
    </div>
  );
}