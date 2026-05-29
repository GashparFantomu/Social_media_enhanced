import { Link } from 'react-router-dom';

export default function Navbar() {
  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark border-bottom border-secondary px-4">
      <div className="container-fluid">
        <Link className="navbar-brand fw-bold text-primary" to="/">🚀 AI Cross-Poster</Link>
        <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-collapse navbar-nav ms-auto mb-2 mb-lg-0">
            <li className="nav-item"><Link className="nav-link" to="/dashboard">🧠 Dashboard</Link></li>
            <li className="nav-item"><Link className="nav-link" to="/integrations">🔑 Integrări</Link></li>
          </ul>
        </div>
      </div>
    </nav>
  );
}
