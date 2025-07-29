import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../api/axios';
import MapPreview from '../components/MapPreview';
import { toast } from 'react-toastify';

const IncidentDetails = () => {
  const { id } = useParams();
  const [incident, setIncident] = useState(null);
  const [loading, setLoading] = useState(true);

  const [comments, setComments] = useState([]);
const [newComment, setNewComment] = useState('');

useEffect(() => {
  const fetchComments = async () => {
    const res = await api.get(`/api/incidents/${id}/comments`);
    setComments(res.data);
  };
  fetchComments();
}, [id]);

const handleSubmit = async (e) => {
  e.preventDefault();
  const res = await api.post(`/api/incidents/${id}/comments`, { text: newComment });
  setComments([res.data, ...comments]);
  setNewComment('');
};

  useEffect(() => {
    const fetchIncident = async () => {
      try {
        const res = await api.get(`/api/incidents/${id}`);
        setIncident(res.data);
      } catch (err) {
        toast.error('Failed to load incident');
      } finally {
        setLoading(false);
      }
    };
    fetchIncident();
  }, [id]);

  if (loading) return <p className="text-center py-10">Loading...</p>;
  if (!incident) return <p>Incident not found.</p>;

  return (
    <div className="container mx-auto px-4 py-6 max-w-3xl">
      <Link to="/" className="text-primary hover:underline mb-4 block">← Back to Feed</Link>
      <h1 className="text-3xl font-bold mb-4">{incident.title}</h1>
      {incident.image && (
        <img src={incident.image} alt={incident.title} className="w-full h-64 object-cover rounded-lg mb-4" />
      )}
      <p className="text-lg mb-4">{incident.description}</p>
      <p className="text-sm text-gray-500">
        Reported {new Date(incident.created_at).toLocaleString()}
      </p>

      <h3 className="text-xl font-semibold mt-6 mb-2">Location</h3>
      <MapPreview position={{ lat: incident.latitude, lng: incident.longitude }} />

      <div className="mt-6">
        <button className="text-red-600">❤️ Like</button>
      </div>
      <form onSubmit={handleSubmit} className="mt-4">
        <textarea
          value={newComment}
          onChange={e => setNewComment(e.target.value)}
          className="input w-full"
          rows="2"
          placeholder="Add a comment..."
        />
        <button type="submit" className="btn-primary mt-2">Comment</button>
      </form>
    </div>
  );
};

export default IncidentDetails;