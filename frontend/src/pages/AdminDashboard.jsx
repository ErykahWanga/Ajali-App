// src/pages/AdminDashboard.jsx
import { useEffect, useState } from 'react';
import api from '../api';
import IncidentCard from '../components/IncidentCard';

export default function AdminDashboard() {
  const [incidents, setIncidents] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAllIncidents = async () => {
      try {
        const res = await api.get('/admin/incidents');
        setIncidents(res.data);
      } catch (err) {
        console.error('Failed to load incidents:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchAllIncidents();
  }, []);

  return (
    <div className="container mx-auto px-4 py-6">
      <h1 className="text-2xl font-bold mb-4">Admin Dashboard</h1>
      {loading ? (
        <p>Loading...</p>
      ) : incidents.length ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {incidents.map((incident) => (
            <IncidentCard key={incident.id} incident={incident} />
          ))}
        </div>
      ) : (
        <p>No incidents yet.</p>
      )}
    </div>
  );
}