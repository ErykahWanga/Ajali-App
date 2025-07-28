
// src/pages/Home.jsx
import { useEffect, useState } from 'react';
import api from '../api';
import IncidentCard from '../components/IncidentCard';

export default function Home() {
  const [incidents, setIncidents] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchIncidents = async () => {
      try {
        const res = await api.get('/incidents');
        setIncidents(res.data);
      } catch (err) {
        console.error('Failed to load incidents:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchIncidents();
  }, []);

  return (
    <div className="container mx-auto px-4 py-6">
      <div className="mb-8 text-center">
        <h1 className="text-3xl font-bold mb-4 text-gray-800 dark:text-white">Ajali Reporter</h1>
        <p className="text-lg text-gray-600 dark:text-gray-300 mb-6">
          Report road accidents and emergencies in Kenya. Help keep our roads safer.
        </p>
      </div>

      <h2 className="text-2xl font-bold mb-4 text-gray-800 dark:text-white">Recent Incidents</h2>
      {loading ? (
        <p className="text-gray-600 dark:text-gray-300">Loading incidents...</p>
      ) : incidents.length ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {incidents.map((incident) => (
            <IncidentCard key={incident.id} incident={incident} />
          ))}
        </div>
      ) : (
        <p className="text-gray-600 dark:text-gray-300">No incidents reported yet.</p>
      )}

      <div className="mt-12">
        <h3 className="text-xl font-bold mb-4 text-gray-800 dark:text-white">Emergency Contacts</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <a 
            href="tel:+254700000000" 
            className="block bg-red-500 hover:bg-red-600 text-white text-center py-3 rounded-lg transition font-medium"
          >
            🚨 Call Police
          </a>
          <a 
            href="tel:+254711111111" 
            className="block bg-green-500 hover:bg-green-600 text-white text-center py-3 rounded-lg transition font-medium"
          >
            🏥 Call Red Cross
          </a>
        </div>
      </div>
    </div>
  );
}