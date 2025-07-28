// src/components/FAB.jsx
import { Link } from 'react-router-dom';

export default function FAB() {
  return (
    <Link
      to="/report"
      className="fixed bottom-6 right-6 bg-red-600 hover:bg-red-700 text-white p-4 rounded-full shadow-lg transition transform hover:scale-105 z-40"
    >
      <span className="text-xl">🚨</span>
    </Link>
  );
}