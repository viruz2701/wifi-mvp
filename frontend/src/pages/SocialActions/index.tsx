import { useState, useEffect, useCallback } from 'react';
import { Container } from '@mui/material';
import SocialActionsList from './SocialActionsList';
import SocialActionForm from './SocialActionForm';
import { SocialAction } from './types';
import api from '@/api/axios';

const SocialActionsPage = () => {
  const [formOpen, setFormOpen] = useState(false);
  const [editingAction, setEditingAction] = useState<SocialAction | null>(null);
  const [actionTypes, setActionTypes] = useState<string[]>([]);
  const [networks, setNetworks] = useState<string[]>([]);

  const fetchTypes = useCallback(async () => {
    try {
      const response = await api.get('/social/types');
      setActionTypes(response.data);
    } catch (err) {
      console.error('Failed to load action types:', err);
    }
  }, []);

  const fetchNetworks = useCallback(async () => {
    try {
      const response = await api.get('/social/networks');
      setNetworks(response.data);
    } catch (err) {
      console.error('Failed to load networks:', err);
    }
  }, []);

  useEffect(() => {
    fetchTypes();
    fetchNetworks();
  }, [fetchTypes, fetchNetworks]);

  const handleAdd = () => {
    setEditingAction(null);
    setFormOpen(true);
  };

  const handleEdit = (action: SocialAction) => {
    setEditingAction(action);
    setFormOpen(true);
  };

  const handleSaved = () => {
    window.location.reload();
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4 }}>
      <SocialActionsList onEdit={handleEdit} onAdd={handleAdd} />
      <SocialActionForm
        open={formOpen}
        onClose={() => setFormOpen(false)}
        onSaved={handleSaved}
        action={editingAction}
        actionTypes={actionTypes}
        networks={networks}
      />
    </Container>
  );
};

export default SocialActionsPage;