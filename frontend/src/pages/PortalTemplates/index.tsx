import { useState } from 'react';
import TemplatesList from './TemplatesList';
import TemplateForm from './TemplateForm';

export default function PortalTemplatesPage() {
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
      <TemplatesList onEdit={handleEdit} onAdd={handleAdd} />
      <TemplateForm
        open={formOpen}
        onClose={() => setFormOpen(false)}
        onSaved={handleSaved}
        templateId={editingId}
      />
    </>
  );
}
