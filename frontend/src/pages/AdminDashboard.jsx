import { useEffect, useState } from 'react';
import api from '../api/axios';
import IncidentCard from '../components/IncidentCard';
import { toast } from 'react-toastify';

const AdminDashboard = () => {
  const [incidents, setIncidents] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchIncidents = async () => {
      try {
        const res = await api.get('/api/incidents');
        setIncidents(res.data);
      } catch (err) {
        toast.error('Failed to load incidents');
      } finally {
        setLoading(false);
      }
    };
    fetchIncidents();
  }, []);

  const handleDelete = async (id) => {
    if (!window.confirm('Delete this incident?')) return;
    try {
      await api.delete(`/api/incidents/${id}`);
      setIncidents(incidents.filter(i => i.id !== id));
      toast.success('Incident deleted');
    } catch (err) {
      toast.error('Delete failed');
    }
  };

  if (loading) return <p>Loading dashboard...</p>;

  return (
    <div className="container mx-auto px-4 py-6">
      <h1 className="text-2xl font-bold mb-6">Admin Dashboard</h1>
      <p className="mb-6">Manage all reported incidents.</p>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {incidents.map((inc) => (
          <IncidentCard
            key={inc.id}
            incident={inc}
            showActions={true}
            onDelete={handleDelete}
            onEdit={() => {}}
          />
        ))}
      </div>
    </div>
  );
};

export default AdminDashboard;