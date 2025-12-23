import { Link, useLocation } from 'react-router-dom';
import './Navbar.css';

function Navbar() {
    const location = useLocation();

    return (
        <nav className="navbar">
            <div className="navbar-container">
                <Link to="/" className="logo">
                    <span className="logo-icon">🏥</span>
                    <span>TestCaseAI</span>
                </Link>
                <ul className="nav-links">
                    <li>
                        <Link to="/" className={location.pathname === '/' ? 'active' : ''}>
                            Dashboard
                        </Link>
                    </li>
                    <li>
                        <Link to="/upload" className={location.pathname === '/upload' ? 'active' : ''}>
                            Upload PDF
                        </Link>
                    </li>
                    <li>
                        <Link to="/history" className={location.pathname === '/history' ? 'active' : ''}>
                            History
                        </Link>
                    </li>
                </ul>
            </div>
        </nav>
    );
}

export default Navbar;
