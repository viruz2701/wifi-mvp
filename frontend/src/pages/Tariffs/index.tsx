import React, { useState } from 'react';
import { Container } from '@mui/material';
import TariffsList from './TariffsList';
import TariffForm from './TariffForm';
import { Tariff } from './types';

const TariffsPage: React.FC = () => {
  const [formOpen, setFormOpen] = useState(false);
  const [editingTariff, setEditingTariff] = useState<Tariff | null>(null);

  const handleAdd = () => {
    setEditingTariff(null);
    setFormOpen(true);
  };

  const handleEdit = (tariff: Tariff) => {
    setEditingTariff(tariff);
    setFormOpen(true);
  };

  const handleSaved = () => {
    window.location.reload();
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4 }}>
      <TariffsList onEdit={handleEdit} onAdd={handleAdd} />
      <TariffForm
        open={formOpen}
        onClose={() => setFormOpen(false)}
        onSaved={handleSaved}
        tariff={editingTariff}
      />
    </Container>
  );
};

export default TariffsPage;