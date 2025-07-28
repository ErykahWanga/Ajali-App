// src/pages/AccountReports.jsx
import { useEffect, useState } from 'react';
import api from '../api';
import IncidentCard from '../components/IncidentCard';

export default function AccountReports() {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchReports = async () => {
      try {
        const res = await api.get('/incidents/my');
        setReports(res.data);
      } catch (err) {
        console.error('Failed to load reports:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchReports();
  }, []);

  return (
    <div className="container mx-auto px-4 py-6">
      <h1 className="text-2xl font-bold mb-4">My Reports</h1>
      {loading ? (
        <p>Loading...</p>
      ) : reports.length ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {reports.map((report) => (
            <IncidentCard key={report.id} incident={report} />
          ))}
        </div>
      ) : (
        <p>No reports yet.</p>
      )}
    </div>
  );
}