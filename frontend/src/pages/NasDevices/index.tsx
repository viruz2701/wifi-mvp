import { useState } from 'react';
import NasDevicesList from './NasDevicesList';
import NasDeviceForm from './NasDeviceForm';

export default function NasDevicesPage() {
  const [formOpen, setFormOpen] = useState(false);
  const [editingId, setEditingId] = useState<number | undefined>();

  const handleAdd = () => {
    setEditingId(undefined);
    setFormOpen(true);
  };

  const handleEdit = (id: number) => {
    setEditingId(id);
    setFormOpen(true);
  };

  const handleSaved = () => {
    window.location.reload();
  };

  return (
    <>
      <NasDevicesList onEdit={handleEdit} onAdd={handleAdd} />
      <NasDeviceForm
        open={formOpen}
        onClose={() => setFormOpen(false)}
        onSaved={handleSaved}
        deviceId={editingId}
      />
    </>
  );
}