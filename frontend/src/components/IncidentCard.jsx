import { formatDistanceToNow } from 'date-fns';
import MapPreview from './MapPreview';
import { useState } from 'react';
import { Link } from 'react-router-dom'; // 🔴 Missing
import api from '../api/axios';           // 🔴 Missing
import { toast } from 'react-toastify';   // 🔴 Missing

const IncidentCard = ({ incident, showActions = false, onDelete, onEdit }) => {
  const [likes, setLikes] = useState(incident.likes || 0);
  const [liked, setLiked] = useState(false);

  const handleLike = async () => {
    const token = localStorage.getItem('token');
    if (!token) {
      toast.error("You must be logged in to like an incident");
      return;
    }

    try {
      const res = await api.post(`/api/incidents/${incident.id}/like`, {}, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setLiked(res.data.liked);
      setLikes(res.data.likes);
      toast.success(res.data.liked ? "Liked!" : "Removed like");
    } catch (err) {
      toast.error("Could not like incident");
      console.error(err);
    }
  };

  return (
    <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-md">
      {incident.image && (
        <img
          src={incident.image}
          alt={incident.title}
          className="w-full h-48 object-cover rounded-md mb-2"
        />
      )}
      <h3 className="text-xl font-semibold text-primary">{incident.title}</h3>
      <p className="text-gray-600 dark:text-gray-300 line-clamp-2">
        {incident.description}
      </p>
      <p className="text-sm text-gray-500 mt-1">
        {formatDistanceToNow(new Date(incident.created_at))} ago
      </p>

      <MapPreview position={{ lat: incident.latitude, lng: incident.longitude }} />

      <div className="flex justify-between items-center mt-3">
        <button
          onClick={handleLike}
          className={`flex items-center gap-1 ${liked ? 'text-red-600' : 'text-gray-500'}`}
        >
          ❤️ {likes}
        </button>
        {showActions && (
          <div className="flex gap-2">
            <button onClick={() => onEdit(incident)} className="text-blue-600 text-sm">
              Edit
            </button>
            <button onClick={() => onDelete(incident.id)} className="text-red-600 text-sm">
              Delete
            </button>
          </div>
        )}
      </div>

      <Link to={`/incidents/${incident.id}`} className="block mt-3 text-primary hover:underline text-sm">
        View Details →
      </Link>
    </div>
  );
};

export default IncidentCard;