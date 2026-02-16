import React from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { Container } from '@mui/material';
import { TelegramAuth } from '../components/TelegramAuth';

const TelegramAuthPage: React.FC = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const mac = searchParams.get('mac') || '';
  const venueId = searchParams.get('venue_id') ? Number(searchParams.get('venue_id')) : 0;

  const handleSuccess = () => {
    // Перенаправляем на страницу приветствия (или обратно на портал)
    navigate(`/portal/welcome?mac=${mac}`);
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