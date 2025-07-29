import { Link } from 'react-router-dom';

const FAB = () => {
  return (
    <Link
      to="/report"
      className="fixed bottom-6 right-6 w-14 h-14 bg-primary hover:bg-red-700 text-white rounded-full flex items-center justify-center shadow-lg transition transform hover:scale-105"
      title="Report Incident"
    >
      +
    </Link>
  );
};

export default FAB;