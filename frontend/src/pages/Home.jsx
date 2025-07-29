import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../api/axios';
import IncidentCard from '../components/IncidentCard';
import { toast } from 'react-toastify';

const Home = () => {
  const [incidents, setIncidents] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchIncidents = async () => {
      try {
        const res = await api.get('/api/incidents');
        setIncidents(res.data);
      } catch (err) {
        toast.error('Failed to load incidents');
        // Fallback mock data
        setIncidents([
          {
            id: 1,
            title: "Car Accident at Ngong Road",
            description: "Two vehicles collided near the junction. One injured.",
            latitude: -1.3306,
            longitude: 36.7568,
            image: "https://picsum.photos/seed/inc1/800/400",
            created_at: "2024-04-05T10:00:00Z",
            likes: 5,
          },
          {
            id: 2,
            title: "Fire at Gikomba Market",
            description: "Small fire broke out in the eastern wing. Firefighters responded.",
            latitude: -1.2921,
            longitude: 36.8219,
            image: "https://picsum.photos/seed/inc2/800/400",
            created_at: "2024-04-04T15:30:00Z",
            likes: 12,
          },
        ]);
      } finally {
        setLoading(false);
      }
    };
    fetchIncidents();
  }, []);

  if (loading) return <p className="text-center py-10">Loading incidents...</p>;

  return (
    <div className="container mx-auto px-4 py-6">
      <h1 className="text-3xl font-bold mb-4 text-primary">Ajali Reporter</h1>
      <p className="mb-6 text-gray-700 dark:text-gray-300">
        Report road accidents and emergencies in Kenya. Stay safe, stay informed.
      </p>

      <div className="flex gap-4 mb-6">
        <a href="tel:999" className="flex-1 bg-red-600 text-white p-3 rounded text-center">🚨 Police: 999</a>
        <a href="tel:112" className="flex-1 bg-blue-600 text-white p-3 rounded text-center">🏥 Red Cross: 112</a>
      </div>

      <h2 className="text-2xl font-semibold mb-4">Recent Incidents</h2>
      {incidents.length === 0 ? (
        <p>No incidents reported yet.</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {incidents.map((inc) => (
            <IncidentCard key={inc.id} incident={inc} />
          ))}
        </div>
      )}

      <div className="mt-8 text-center">
        <Link to="/report" className="btn-primary">Report an Incident</Link>
      </div>
    </div>
  );
};

export default Home;