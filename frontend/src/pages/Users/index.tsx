import { useState } from 'react';
import UsersList from './UsersList';
import UserForm from './UserForm';

export default function UsersPage() {
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
      <UsersList onEdit={handleEdit} onAdd={handleAdd} />
      <UserForm
        open={formOpen}
        onClose={() => setFormOpen(false)}
        onSaved={handleSaved}
        userId={editingId}
      />
    </>
  );
}