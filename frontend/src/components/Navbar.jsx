// src/components/Navbar.jsx
import { Link, useNavigate } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';
import { logout } from '../store/authSlice';
import ThemeToggle from './ThemeToggle';

export default function Navbar() {
  const { user, token } = useSelector((state) => state.auth);
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const handleLogout = () => {
    dispatch(logout());
    navigate('/');
  };

  return (
    <nav className="fixed top-0 left-0 right-0 bg-white dark:bg-gray-800 shadow-md z-50">
      <div className="container mx-auto px-4 py-3 flex justify-between items-center">
        <Link to="/" className="text-xl font-bold text-blue-600 dark:text-blue-400">
          Ajali Reporter
        </Link>
        
        <div className="hidden md:flex items-center space-x-6">
          <Link to="/" className="text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition">
            Home
          </Link>
          
          {token ? (
            <>
              <Link to="/report" className="text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition">
                Report Incident
              </Link>
              <Link to="/account" className="text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition">
                My Reports
              </Link>
              {user && user.is_admin && (
                <Link to="/admin" className="text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition">
                  Admin
                </Link>
              )}
            </>
          ) : (
            <Link to="/login" className="text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition">
              Report Incident
            </Link>
          )}
        </div>

        <div className="flex items-center space-x-4">
          <ThemeToggle />
          {token ? (
            <>
              <span className="hidden md:inline text-gray-800 dark:text-gray-200">Hi, {user.username}</span>
              <button 
                onClick={handleLogout} 
                className="text-sm bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded transition"
              >
                Logout
              </button>
            </>
          ) : (
            <Link 
              to="/login" 
              className="text-sm bg-blue-500 hover:bg-blue-600 text-white px-3 py-1 rounded transition"
            >
              Login
            </Link>
          )}
        </div>
      </div>

      {/* Mobile Navigation */}
      <div className="md:hidden border-t dark:border-gray-700">
        <div className="container mx-auto px-4 py-2 flex flex-wrap gap-4">
          <Link to="/" className="text-sm text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition">
            Home
          </Link>
          
          {token ? (
            <>
              <Link to="/report" className="text-sm text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition">
                Report
              </Link>
              <Link to="/account" className="text-sm text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition">
                My Reports
              </Link>
              {user && user.is_admin && (
                <Link to="/admin" className="text-sm text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition">
                  Admin
                </Link>
              )}
            </>
          ) : (
            <Link to="/login" className="text-sm text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition">
              Report
            </Link>
          )}
        </div>
      </div>
    </nav>
  );
}