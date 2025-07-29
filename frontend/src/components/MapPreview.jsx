import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

import { Icon } from 'leaflet';

delete Icon.Default.prototype._getIconUrl;

Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
});

const MapPreview = ({ position }) => {
  if (!position || !position.lat || !position.lng) return <p className="text-gray-500">Location not available</p>;

  return (
    <div className="h-64 rounded-lg overflow-hidden">
      <MapContainer
        center={[position.lat, position.lng]}
        zoom={13}
        style={{ height: '100%', width: '100%' }}
        zoomControl={false}
      >
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        <Marker position={[position.lat, position.lng]}>
          <Popup>{position.lat.toFixed(4)}, {position.lng.toFixed(4)}</Popup>
        </Marker>
      </MapContainer>
    </div>
  );
};

export default MapPreview;