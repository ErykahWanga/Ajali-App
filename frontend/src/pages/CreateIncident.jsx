// src/pages/CreateIncident.jsx
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import api from '../api';

export default function CreateIncident() {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [latitude, setLatitude] = useState('');
  const [longitude, setLongitude] = useState('');
  const [image, setImage] = useState(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    const formData = new FormData();
    formData.append('title', title);
    formData.append('description', description);
    formData.append('latitude', latitude);
    formData.append('longitude', longitude);
    if (image) formData.append('image', image);

    try {
      await api.post('/incidents', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      toast.success('Incident reported!');
      navigate('/');
    } catch (err) {
      toast.error('Failed to submit report');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8 max-w-lg">
      <h2 className="text-2xl font-bold mb-4">Report an Incident</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          type="text"
          placeholder="Title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
          className="w-full px-3 py-2 border rounded dark:bg-gray-800"
        />
        <textarea
          placeholder="Description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          required
          className="w-full px-3 py-2 border rounded dark:bg-gray-800"
        />
        <input
          type="number"
          placeholder="Latitude"
          step="any"
          value={latitude}
          onChange={(e) => setLatitude(e.target.value)}
          required
          className="w-full px-3 py-2 border rounded dark:bg-gray-800"
        />
        <input
          type="number"
          placeholder="Longitude"
          step="any"
          value={longitude}
          onChange={(e) => setLongitude(e.target.value)}
          required
          className="w-full px-3 py-2 border rounded dark:bg-gray-800"
        />
        <input
          type="file"
          accept="image/*"
          onChange={(e) => setImage(e.target.files[0])}
          className="w-full px-3 py-2 border rounded dark:bg-gray-800"
        />
        <button
          disabled={loading}
          type="submit"
          className="w-full bg-blue-500 text-white py-2 rounded disabled:opacity-50"
        >
          {loading ? 'Submitting...' : 'Submit Report'}
        </button>
      </form>
    </div>
  );
}