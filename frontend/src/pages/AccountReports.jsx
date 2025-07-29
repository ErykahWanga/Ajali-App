import { useEffect, useState } from 'react';
import { useSelector } from 'react-redux';
import api from '../api/axios';
import IncidentCard from '../components/IncidentCard';
import { toast } from 'react-toastify';

const AccountReports = () => {
  const { user } = useSelector((state) => state.auth);
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchReports = async () => {
      try {
        const res = await api.get(`/api/users/${user.id}/incidents`);
        setReports(res.data);
      } catch (err) {
        toast.error('Failed to load your reports');
      } finally {
        setLoading(false);
      }
    };
    if (user) fetchReports();
  }, [user]);

  const handleDelete = async (id) => {
    if (!window.confirm('Delete this report?')) return;
    try {
      await api.delete(`/api/incidents/${id}`);
      setReports(reports.filter(r => r.id !== id));
      toast.success('Report deleted');
    } catch (err) {
      toast.error('Delete failed');
    }
  };

  const handleEdit = (incident) => {
    // Future: Navigate to edit form
    toast.info('Edit feature coming soon');
  };

  if (loading) return <p>Loading your reports...</p>;

  return (
    <div className="container mx-auto px-4 py-6">
      <h1 className="text-2xl font-bold mb-6">Your Reports</h1>
      {reports.length === 0 ? (
        <p>You haven't reported any incidents yet.</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {reports.map((rep) => (
            <IncidentCard
              key={rep.id}
              incident={rep}
              showActions={true}
              onDelete={handleDelete}
              onEdit={handleEdit}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default AccountReports;