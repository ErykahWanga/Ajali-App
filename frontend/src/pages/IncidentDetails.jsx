// src/pages/IncidentDetails.jsx
import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import api from '../api';

export default function IncidentDetails() {
  const { id } = useParams();
  const [incident, setIncident] = useState(null);

  useEffect(() => {
    const fetchIncident = async () => {
      try {
        const res = await api.get(`/incidents/${id}`);
        setIncident(res.data);
      } catch (err) {
        console.error('Failed to load incident:', err);
      }
    };

    fetchIncident();
  }, [id]);

  if (!incident) return <div className="container mx-auto px-4 py-8">Loading...</div>;

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold">{incident.title}</h1>
      <img
        src={incident.image_url || 'https://via.placeholder.com/600x400'}
        alt={incident.title}
        className="w-full h-64 object-cover rounded my-4"
      />
      <p className="mb-2"><strong>Description:</strong> {incident.description}</p>
      <p><strong>Location:</strong> {incident.latitude}, {incident.longitude}</p>
    </div>
  );
}