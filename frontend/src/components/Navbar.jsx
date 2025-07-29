// src/components/Navbar.jsx
import { Link, useNavigate } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';
import { logout } from '../store/authSlice';
import ThemeToggle from './ThemeToggle';

const Navbar = () => {
  const { isAuthenticated, user } = useSelector((state) => state.auth);
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const handleLogout = () => {
    dispatch(logout());
    navigate('/');
  };

  return (
    <nav className="bg-primary text-light shadow-md">
      <div className="container mx-auto px-4 py-3 flex justify-between items-center">
        <Link to="/" className="text-2xl font-bold">Ajali Reporter</Link>

        <div className="flex items-center gap-4">
          <ThemeToggle />

          {isAuthenticated ? (
            <>
              <span className="text-sm">Hello, {user.username}</span>
              <Link to="/account" className="btn-light">My Reports</Link>
              <Link to="/report" className="btn-light">Report</Link>
              {user.is_admin && <Link to="/admin" className="text-sm underline">Admin</Link>}
              <button onClick={handleLogout} className="btn-secondary">Logout</button>
            </>
          ) : (
            <>
              <Link to="/login" className="btn-light">Login</Link>
              <Link to="/signup" className="btn-light">Sign Up</Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;