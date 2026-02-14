import { useState } from 'react';
import VenuesList from './VenuesList';
import VenueForm from './VenueForm';

export default function VenuesPage() {
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
    // Перезагрузить список
    window.location.reload();
  };

  return (
    <>
      <VenuesList onEdit={handleEdit} onAdd={handleAdd} />
      <VenueForm
        open={formOpen}
        onClose={() => setFormOpen(false)}
        onSaved={handleSaved}
        venueId={editingId}
      />
    </>
  );
}
