import React, { useState, useEffect } from 'react';
import {
  Paper, Typography, TextField, Button, Stack, Alert, CircularProgress, Divider,
} from '@mui/material';
import api from '@/api/axios';
import { useSnackbar } from '@/hooks/useSnackbar';
import { LoadingScreen } from '@/components/LoadingScreen';

interface Settings {
  telegram_bot_token: string;
  telegram_bot_username: string;
  telegram_bot_webhook_url: string;
  wireguard_server_public_key: string;
  wireguard_server_endpoint: string;
}

const SettingsPage: React.FC = () => {
  const [settings, setSettings] = useState<Settings>({
    telegram_bot_token: '',
    telegram_bot_username: '',
    telegram_bot_webhook_url: '',
    wireguard_server_public_key: '',
    wireguard_server_endpoint: '',
  });
  const [loading, setLoading] = useState(false);
  const [initialLoading, setInitialLoading] = useState(true);
  const [validationErrors, setValidationErrors] = useState<Partial<Settings>>({});
  const { showSuccess, showError } = useSnackbar();

  useEffect(() => {
    fetchSettings();
  }, []);

  const fetchSettings = async () => {
    setInitialLoading(true);
    try {
      const keys: (keyof Settings)[] = [
        'telegram_bot_token',
        'telegram_bot_username',
        'telegram_bot_webhook_url',
        'wireguard_server_public_key',
        'wireguard_server_endpoint',
      ];
      const promises = keys.map(key => api.get(`/settings/${key}`).catch(() => ({ data: { value: '' } })));
      const results = await Promise.all(promises);
      const newSettings: any = {};
      keys.forEach((key, idx) => {
        newSettings[key] = results[idx].data.value || '';
      });
      setSettings(newSettings);
    } catch (err) {
      showError('Ошибка загрузки настроек');
    } finally {
      setInitialLoading(false);
    }
  };

  const handleChange = (key: keyof Settings) => (e: React.ChangeEvent<HTMLInputElement>) => {
    setSettings(prev => ({ ...prev, [key]: e.target.value }));
    if (validationErrors[key]) {
      setValidationErrors(prev => ({ ...prev, [key]: '' }));
    }
  };

  const validate = (): boolean => {
    const errors: Partial<Settings> = {};
    if (!settings.telegram_bot_token.trim()) {
      errors.telegram_bot_token = 'Токен не может быть пустым';
    }
    if (!settings.telegram_bot_username.trim()) {
      errors.telegram_bot_username = 'Имя пользователя не может быть пустым';
    }
    if (!settings.telegram_bot_webhook_url.trim()) {
      errors.telegram_bot_webhook_url = 'URL вебхука не может быть пустым';
    } else {
      try {
        new URL(settings.telegram_bot_webhook_url);
      } catch {
        errors.telegram_bot_webhook_url = 'Некорректный URL';
      }
    }
    // WireGuard поля не обязательны
    setValidationErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSave = async () => {
    if (!validate()) return;

    setLoading(true);
    try {
      const updates = Object.entries(settings).map(([key, value]) =>
        api.put(`/settings/${key}`, { value })
      );
      await Promise.all(updates);
      showSuccess('Настройки сохранены');
    } catch (err) {
      showError('Ошибка сохранения');
    } finally {
      setLoading(false);
    }
  };

  if (initialLoading) return <LoadingScreen message="Загрузка настроек..." />;

  return (
    <Paper sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>Настройки системы</Typography>
      
      <Typography variant="h6" sx={{ mt: 2 }}>Telegram бот</Typography>
      <Stack spacing={2}>
        <TextField
          label="Telegram Bot Token"
          value={settings.telegram_bot_token}
          onChange={handleChange('telegram_bot_token')}
          fullWidth
          type="password"
          error={!!validationErrors.telegram_bot_token}
          helperText={validationErrors.telegram_bot_token}
        />
        <TextField
          label="Telegram Bot Username"
          value={settings.telegram_bot_username}
          onChange={handleChange('telegram_bot_username')}
          fullWidth
          error={!!validationErrors.telegram_bot_username}
          helperText={validationErrors.telegram_bot_username}
        />
        <TextField
          label="Telegram Bot Webhook URL"
          value={settings.telegram_bot_webhook_url}
          onChange={handleChange('telegram_bot_webhook_url')}
          fullWidth
          placeholder="https://example.com/webhook"
          error={!!validationErrors.telegram_bot_webhook_url}
          helperText={validationErrors.telegram_bot_webhook_url}
        />
      </Stack>

      <Divider sx={{ my: 3 }} />

      <Typography variant="h6" gutterBottom>WireGuard (для подключения к NAS)</Typography>
      <Stack spacing={2}>
        <TextField
          label="Публичный ключ сервера"
          value={settings.wireguard_server_public_key}
          onChange={handleChange('wireguard_server_public_key')}
          fullWidth
          multiline
          rows={2}
          placeholder="Публичный ключ WireGuard сервера"
        />
        <TextField
          label="Endpoint сервера"
          value={settings.wireguard_server_endpoint}
          onChange={handleChange('wireguard_server_endpoint')}
          fullWidth
          placeholder="vpn.example.com:51820"
        />
      </Stack>

      <Button variant="contained" onClick={handleSave} disabled={loading} sx={{ mt: 2 }}>
        {loading ? <CircularProgress size={24} /> : 'Сохранить'}
      </Button>
    </Paper>
  );
};

export default SettingsPage;