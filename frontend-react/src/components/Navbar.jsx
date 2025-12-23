import { Link, useLocation } from 'react-router-dom';
import { useTheme } from '../context/ThemeContext';
import './Navbar.css';

function Navbar() {
    const location = useLocation();
    const { theme, toggleTheme } = useTheme();

    return (
        <nav className="navbar">
            <div className="navbar-container">
                <Link to="/" className="logo">
                    <span className="logo-icon">🏥</span>
                    <span className="logo-text">TestCaseAI</span>
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
                    <li>
                        <button onClick={toggleTheme} className="theme-toggle" aria-label="Toggle theme">
                            {theme === 'light' ? '🌙' : '☀️'}
                        </button>
                    </li>
                </ul>
            </div>
        </nav>
    );
}

export default Navbar;
