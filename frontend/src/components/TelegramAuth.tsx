import React, { useState, useEffect } from 'react';
import { Box, Typography, Paper, CircularProgress, Alert } from '@mui/material';
import QRCode from 'qrcode.react';

interface TelegramAuthProps {
  venueId: number;
  mac: string;
  onSuccess: () => void;
}

export const TelegramAuth: React.FC<TelegramAuthProps> = ({ venueId, mac, onSuccess }) => {
  const [state, setState] = useState<string | null>(null);
  const [botLink, setBotLink] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const initAuth = async () => {
      try {
        const response = await fetch('/api/v1/auth/telegram/init', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ mac, venue_id: venueId })
        });
        if (!response.ok) throw new Error('Failed to init');
        const data = await response.json();
        setState(data.state);
        setBotLink(data.bot_link);
      } catch (err) {
        setError('Ошибка инициализации');
      } finally {
        setLoading(false);
      }
    };
    initAuth();
  }, [mac, venueId]);

  useEffect(() => {
    if (!state) return;

    const eventSource = new EventSource(`/api/v1/auth/telegram/events?state=${state}`);
    eventSource.onmessage = (event) => {
      if (event.data === 'success') {
        onSuccess();
        eventSource.close();
      }
    };
    eventSource.onerror = () => {
      // Можно обработать ошибку, но пока игнорируем
    };

    return () => {
      eventSource.close();
    };
  }, [state, onSuccess]);

  if (loading) return <CircularProgress />;
  if (error) return <Alert severity="error">{error}</Alert>;

  return (
    <Paper sx={{ p: 4, maxWidth: 400, mx: 'auto', textAlign: 'center' }}>
      <Typography variant="h5" gutterBottom>Авторизация через Telegram</Typography>
      <Box sx={{ my: 3 }}>
        {botLink && (
          <>
            <QRCode value={botLink} size={200} />
            <Typography variant="body2" sx={{ mt: 2 }}>
              Отсканируйте QR-код или перейдите по ссылке:
            </Typography>
            <Typography variant="body1">
              <a href={botLink} target="_blank" rel="noopener noreferrer">{botLink}</a>
            </Typography>
          </>
        )}
      </Box>
      <Typography variant="body2" color="text.secondary">
        Откройте Telegram, нажмите "Поделиться номером телефона" и вернитесь сюда.
      </Typography>
    </Paper>
  );
};