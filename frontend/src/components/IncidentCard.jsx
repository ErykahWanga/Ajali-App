// src/components/IncidentCard.jsx
import { Link } from 'react-router-dom';

export default function IncidentCard({ incident }) {
  return (
    <div className="border dark:border-gray-700 p-4 rounded shadow hover:shadow-md transition">
      <img
        src={`${import.meta.env.VITE_API_URL}/incidents/uploads/${incident.image_filename}`}
        alt={incident.title}
        className="w-full h-40 object-cover rounded mb-2"
      />
      <h3 className="font-semibold">{incident.title}</h3>
      <p className="text-sm text-gray-600 dark:text-gray-300 truncate">{incident.description}</p>
      <Link to={`/incidents/${incident.id}`} className="text-blue-500 text-sm mt-2 inline-block">
        View Details
      </Link>
    </div>
  );
}