import React from 'react';
import { useSearchParams } from 'react-router-dom';
import { Container } from '@mui/material';
import { TelegramAuth } from '../components/TelegramAuth';

const TelegramAuthPage: React.FC = () => {
  const [searchParams] = useSearchParams();
  const mac = searchParams.get('mac') || '';
  const venueId = searchParams.get('venue_id') ? Number(searchParams.get('venue_id')) : 0;

  const handleSuccess = () => {
    // Перенаправляем на страницу приветствия портала (бэкенд)
    window.location.href = `/portal/${venueId}/welcome?mac=${mac}`;
  };

  if (!mac || !venueId) {
    return <div>Ошибка: не указаны параметры</div>;
  }

  return (
    <Container maxWidth="sm" sx={{ mt: 4 }}>
      <TelegramAuth venueId={venueId} mac={mac} onSuccess={handleSuccess} />
    </Container>
  );
};

export default TelegramAuthPage;