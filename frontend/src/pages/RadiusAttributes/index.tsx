import { useState } from 'react';
import { Container } from '@mui/material';
import RadiusAttributesList from './RadiusAttributesList';
import RadiusAttributeForm from './RadiusAttributeForm';
import { RadiusAttribute } from './types';

const RadiusAttributesPage = () => {
  const [formOpen, setFormOpen] = useState(false);
  const [editingAttribute, setEditingAttribute] = useState<RadiusAttribute | null>(null);

  const handleAdd = () => {
    setEditingAttribute(null);
    setFormOpen(true);
  };

  const handleEdit = (attr: RadiusAttribute) => {
    setEditingAttribute(attr);
    setFormOpen(true);
  };

  const handleSaved = () => {
    window.location.reload();
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4 }}>
      <RadiusAttributesList onEdit={handleEdit} onAdd={handleAdd} />
      <RadiusAttributeForm
        open={formOpen}
        onClose={() => setFormOpen(false)}
        onSaved={handleSaved}
        attribute={editingAttribute}
      />
    </Container>
  );
};

export default RadiusAttributesPage;