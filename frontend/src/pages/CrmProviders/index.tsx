import React, { useState, useEffect } from 'react';
import { Container } from '@mui/material';
import CrmProvidersList from './CrmProvidersList';
import CrmProviderForm from './CrmProviderForm';
import { CrmProvider } from './types';
import api from '@/api/axios';

const CrmProvidersPage: React.FC = () => {
  const [formOpen, setFormOpen] = useState(false);
  const [editingProvider, setEditingProvider] = useState<CrmProvider | null>(null);
  const [providerTypes, setProviderTypes] = useState<string[]>([]);

  useEffect(() => {
    fetchProviderTypes();
  }, []);

  const fetchProviderTypes = async () => {
    try {
      const response = await api.get('/crm/types');
      setProviderTypes(response.data);
    } catch (err) {
      console.error('Failed to load provider types:', err);
    }
  };

  const handleAdd = () => {
    setEditingProvider(null);
    setFormOpen(true);
  };

  const handleEdit = (provider: CrmProvider) => {
    setEditingProvider(provider);
    setFormOpen(true);
  };

  const handleSaved = () => {
    // Перезагрузить список через ререндер компонента CrmProvidersList
    window.location.reload(); // или использовать state, но для простоты так
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4 }}>
      <CrmProvidersList onEdit={handleEdit} onAdd={handleAdd} />
      <CrmProviderForm
        open={formOpen}
        onClose={() => setFormOpen(false)}
        onSaved={handleSaved}
        provider={editingProvider}
        providerTypes={providerTypes}
      />
    </Container>
  );
};

export default CrmProvidersPage;