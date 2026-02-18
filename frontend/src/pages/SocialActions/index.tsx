import React, { useState, useEffect } from 'react';
import { Container } from '@mui/material';
import SocialActionsList from './SocialActionsList';
import SocialActionForm from './SocialActionForm';
import { SocialAction } from './types';
import api from '@/api/axios';

const SocialActionsPage: React.FC = () => {
  const [formOpen, setFormOpen] = useState(false);
  const [editingAction, setEditingAction] = useState<SocialAction | null>(null);
  const [actionTypes, setActionTypes] = useState<string[]>([]);
  const [networks, setNetworks] = useState<string[]>([]);

  useEffect(() => {
    fetchTypes();
    fetchNetworks();
  }, []);

  const fetchTypes = async () => {
    try {
      const response = await api.get('/social/types');
      setActionTypes(response.data);
    } catch (err) {
      console.error('Failed to load action types:', err);
    }
  };

  const fetchNetworks = async () => {
    try {
      const response = await api.get('/social/networks');
      setNetworks(response.data);
    } catch (err) {
      console.error('Failed to load networks:', err);
    }
  };

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