import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import Navbar from './components/Navbar';
import Home from './pages/Home';
import Login from './pages/Login';
import Signup from './pages/Signup';
import CreateIncident from './pages/CreateIncident';
import IncidentDetails from './pages/IncidentDetails';
import AccountReports from './pages/AccountReports';
import AdminDashboard from './pages/AdminDashboard';
import PrivateRoute from './components/PrivateRoute';
import FAB from './components/FAB';
import 'leaflet/dist/leaflet.css';

function App() {
  return (
    <Router>
      <div className="min-h-screen flex flex-col">
        <Navbar />
        <main className="flex-grow container mx-auto px-4 py-6">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/signup" element={<Signup />} />
            <Route
              path="/report"
              element={
                <PrivateRoute>
                  <CreateIncident />
                </PrivateRoute>
              }
            />
            <Route
              path="/account"
              element={
                <PrivateRoute>
                  <AccountReports />
                </PrivateRoute>
              }
            />
            <Route
              path="/admin"
              element={
                <PrivateRoute adminOnly>
                  <AdminDashboard />
                </PrivateRoute>
              }
            />
            <Route path="/incidents/:id" element={<IncidentDetails />} />
          </Routes>
        </main>
        <FAB />
        <ToastContainer position="bottom-right" />
      </div>
    </Router>
  );
}

export default App;