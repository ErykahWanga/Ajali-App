// src/App.jsx
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Login from './pages/Login';
import Signup from './pages/Signup';
import CreateIncident from './pages/CreateIncident';
import IncidentDetails from './pages/IncidentDetails';
import AccountReports from './pages/AccountReports';
import AdminDashboard from './pages/AdminDashboard';
import Navbar from './components/Navbar';
import PrivateRoute from './components/PrivateRoute';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import FAB from './components/FAB';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-white dark:bg-gray-900">
        <Navbar />
        <div className="pt-16"> {/* This adds padding for the fixed navbar */}
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/signup" element={<Signup />} />
            <Route path="/incidents/:id" element={<IncidentDetails />} />
            <Route element={<PrivateRoute />}>
              <Route path="/report" element={<CreateIncident />} />
              <Route path="/account" element={<AccountReports />} />
              <Route path="/admin" element={<AdminDashboard />} />
            </Route>
          </Routes>
        </div>
        <FAB />
        <ToastContainer position="bottom-right" />
      </div>
    </Router>
  );
}

export default App;