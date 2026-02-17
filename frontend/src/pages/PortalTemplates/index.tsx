import { useState } from 'react';
import TemplatesList from './TemplatesList';
import TemplateForm from './TemplateForm';
import { BuiltinTemplates } from './BuiltinTemplates';
import { Button, Stack } from '@mui/material';
import LibraryBooksIcon from '@mui/icons-material/LibraryBooks';

export default function PortalTemplatesPage() {
  const [formOpen, setFormOpen] = useState(false);
  const [builtinOpen, setBuiltinOpen] = useState(false);
  const [editingId, setEditingId] = useState<number | undefined>();
  const [refreshKey, setRefreshKey] = useState(0);

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
  };

  return (
    <>
      <Stack direction="row" justifyContent="space-between" alignItems="center" mb={2}>
        <div />
        <Stack direction="row" spacing={2}>
          <Button variant="outlined" startIcon={<LibraryBooksIcon />} onClick={() => setBuiltinOpen(true)}>
            Выбрать из готовых
          </Button>
          <Button variant="contained" onClick={handleAdd}>
            Добавить
          </Button>
        </Stack>
      </Stack>
      <TemplatesList key={refreshKey} onEdit={handleEdit} onAdd={handleAdd} />
      <TemplateForm
        open={formOpen}
        onClose={() => setFormOpen(false)}
        onSaved={handleSaved}
        templateId={editingId}
      />
      <BuiltinTemplates
        open={builtinOpen}
        onClose={() => setBuiltinOpen(false)}
        onImported={handleSaved}
      />
    </>
  );
}