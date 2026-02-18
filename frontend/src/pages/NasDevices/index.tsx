import { useState, useEffect, useRef } from 'react';
import NasDevicesList from './NasDevicesList';
import NasDeviceForm from './NasDeviceForm';
import ErrorBoundary from '@/components/ErrorBoundary';

export default function NasDevicesPage() {
  const [formOpen, setFormOpen] = useState(false);
  const [editingId, setEditingId] = useState<number | undefined>();
  const [refreshKey, setRefreshKey] = useState(0);
  const isMounted = useRef(true);

  useEffect(() => {
    isMounted.current = true;
    return () => {
      isMounted.current = false;
    };
  }, []);

  const handleAdd = () => {
    setEditingId(undefined);
    setFormOpen(true);
  };

  const handleEdit = (id: number) => {
    setEditingId(id);
    setFormOpen(true);
  };

  const handleSaved = () => {
    setRefreshKey(prev => prev + 1);
    // Небольшая задержка перед закрытием, чтобы React успел завершить обновление
    setTimeout(() => {
      if (isMounted.current) {
        setFormOpen(false);
      }
    }, 100);
  };

  return (
    <>
      <NasDevicesList key={refreshKey} onEdit={handleEdit} onAdd={handleAdd} />
      <ErrorBoundary>
        <NasDeviceForm
          open={formOpen}
          onClose={() => setFormOpen(false)}
          onSaved={handleSaved}
          deviceId={editingId}
        />
      </ErrorBoundary>
    </>
  );
}