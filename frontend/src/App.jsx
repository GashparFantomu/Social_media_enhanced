import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Home from './pages/Home';
import Integrations from './pages/Integrations';
import Dashboard from './pages/Dashboard';
import Callback from './pages/Callback';

export default function App() {
  return (
    <Router>
      <div className="d-flex flex-column bg-dark text-light min-vh-100" style={{ backgroundColor: '#121212' }}>
        <Navbar />
        <main className="flex-grow-1">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/integrations" element={<Integrations />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/callback/:platform" element={<Callback />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}