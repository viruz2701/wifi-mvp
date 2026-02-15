import { useState } from 'react';
import BannersList from './BannersList';
import BannerForm from './BannerForm';

export default function BannersPage() {
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
      <BannersList onEdit={handleEdit} onAdd={handleAdd} />
      <BannerForm
        open={formOpen}
        onClose={() => setFormOpen(false)}
        onSaved={handleSaved}
        bannerId={editingId}
      />
    </>
  );
}