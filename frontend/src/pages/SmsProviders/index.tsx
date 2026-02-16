import React, { useState, useEffect } from 'react';
import { Container } from '@mui/material';
import ProvidersList from './ProvidersList';
import ProviderForm from './ProviderForm';
import { SmsProvider } from './types';

const SmsProvidersPage: React.FC = () => {
  const [formOpen, setFormOpen] = useState(false);
  const [editingProvider, setEditingProvider] = useState<SmsProvider | null>(null);
  const [providerTypes, setProviderTypes] = useState<string[]>([]);

  useEffect(() => {
    // Загружаем доступные типы провайдеров
    fetch('/api/v1/sms-providers/types', {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
      },
    })
      .then(res => res.json())
      .then(data => setProviderTypes(data))
      .catch(err => console.error('Failed to load provider types:', err));
  }, []);

  const handleAdd = () => {
    setEditingProvider(null);
    setFormOpen(true);
  };

  const handleEdit = (provider: SmsProvider) => {
    setEditingProvider(provider);
    setFormOpen(true);
  };

  const handleSaved = () => {
    // Перезагружаем список через ререндер компонента ProvidersList
    window.location.reload(); // простой способ, можно улучшить через state
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4 }}>
      <ProvidersList onEdit={handleEdit} onAdd={handleAdd} />
      <ProviderForm
        open={formOpen}
        onClose={() => setFormOpen(false)}
        onSaved={handleSaved}
        provider={editingProvider}
        providerTypes={providerTypes}
      />
    </Container>
  );
};

export default SmsProvidersPage;