import React, { useState, useEffect } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Button,
  FormControlLabel,
  Checkbox,
  MenuItem,
  Alert,
  Box,
  Typography,
} from '@mui/material';
import api from '@/api/axios'; // Импортируем настроенный axios
import { SmsProvider, SmsProviderType, SmsProviderFormData } from './types';

interface ProviderFormProps {
  open: boolean;
  onClose: () => void;
  onSaved: () => void;
  provider?: SmsProvider | null;
  providerTypes: string[]; // список типов с бэкенда
}

const ProviderForm: React.FC<ProviderFormProps> = ({
  open,
  onClose,
  onSaved,
  provider,
  providerTypes,
}) => {
  const [formData, setFormData] = useState<SmsProviderFormData>({
    name: '',
    type: 'rocketsms' as SmsProviderType,
    config: {},
    is_active: true,
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [validationErrors, setValidationErrors] = useState<Record<string, string>>({});

  useEffect(() => {
    if (provider) {
      setFormData({
        name: provider.name,
        type: provider.type,
        config: provider.config,
        is_active: provider.is_active,
      });
    } else {
      setFormData({
        name: '',
        type: 'rocketsms' as SmsProviderType,
        config: {},
        is_active: true,
      });
    }
    setValidationErrors({});
  }, [provider]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    // очищаем ошибку для этого поля при вводе
    if (validationErrors[name]) {
      setValidationErrors((prev) => ({ ...prev, [name]: '' }));
    }
  };

  const handleConfigChange = (field: string, value: any) => {
    setFormData((prev) => ({
      ...prev,
      config: { ...prev.config, [field]: value },
    }));
    // очищаем ошибку для config
    if (validationErrors.config) {
      setValidationErrors((prev) => ({ ...prev, config: '' }));
    }
  };

  const handleCheckbox = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData((prev) => ({ ...prev, is_active: e.target.checked }));
  };

  const handleTypeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newType = e.target.value as SmsProviderType;
    setFormData({
      ...formData,
      type: newType,
      config: {},
    });
    setValidationErrors({});
  };

  const validate = (): boolean => {
    const errors: Record<string, string> = {};

    if (!formData.name.trim()) {
      errors.name = 'Название не может быть пустым';
    }

    // Проверка config в зависимости от типа
    if (Object.keys(formData.config).length === 0) {
      errors.config = 'Конфигурация не может быть пустой';
    } else {
      if (formData.type === 'rocketsms') {
        if (!formData.config.username) {
          errors.username = 'Логин обязателен';
        }
        if (!formData.config.password_md5) {
          errors.password_md5 = 'MD5-пароль обязателен';
        }
      } else if (formData.type === 'callpassword') {
        if (!formData.config.api_key) {
          errors.api_key = 'API ключ обязателен';
        }
        // Можно добавить проверку api_secret, если он есть
      }
    }

    setValidationErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSubmit = async () => {
    if (!validate()) {
      return;
    }

    setLoading(true);
    setError('');
    try {
      const url = provider 
        ? `/sms-providers/${provider.id}`
        : '/sms-providers';
      
      if (provider) {
        await api.put(url, formData);
      } else {
        await api.post(url, formData);
      }

      onSaved();
      onClose();
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Ошибка сохранения');
    } finally {
      setLoading(false);
    }
  };

  const renderConfigFields = () => {
    switch (formData.type) {
      case 'rocketsms':
        return (
          <Box sx={{ mt: 2 }}>
            <Typography variant="subtitle2" gutterBottom>Настройки RocketSMS</Typography>
            <TextField
              fullWidth
              margin="dense"
              label="Логин"
              value={formData.config.username || ''}
              onChange={(e) => handleConfigChange('username', e.target.value)}
              required
              error={!!validationErrors.username}
              helperText={validationErrors.username}
            />
            <TextField
              fullWidth
              margin="dense"
              label="MD5 пароль"
              value={formData.config.password_md5 || ''}
              onChange={(e) => handleConfigChange('password_md5', e.target.value)}
              required
              error={!!validationErrors.password_md5}
              helperText={validationErrors.password_md5 || "MD5-хеш пароля от личного кабинета"}
            />
            <TextField
              fullWidth
              margin="dense"
              label="Отправитель (sender)"
              value={formData.config.sender || ''}
              onChange={(e) => handleConfigChange('sender', e.target.value)}
              helperText="Альфа-имя, если не указано - используется имя по умолчанию"
            />
          </Box>
        );
      case 'callpassword':
        return (
          <Box sx={{ mt: 2 }}>
            <Typography variant="subtitle2" gutterBottom>Настройки CallPassword</Typography>
            <TextField
              fullWidth
              margin="dense"
              label="API ключ"
              value={formData.config.api_key || ''}
              onChange={(e) => handleConfigChange('api_key', e.target.value)}
              required
              error={!!validationErrors.api_key}
              helperText={validationErrors.api_key}
            />
            <TextField
              fullWidth
              margin="dense"
              label="API секрет"
              value={formData.config.api_secret || ''}
              onChange={(e) => handleConfigChange('api_secret', e.target.value)}
              required
              error={!!validationErrors.api_secret}
              helperText={validationErrors.api_secret}
            />
            <TextField
              fullWidth
              margin="dense"
              label="Таймаут (сек)"
              value={formData.config.timeout || 60}
              onChange={(e) => handleConfigChange('timeout', e.target.value)}
              type="number"
            />
          </Box>
        );
      default:
        return null;
    }
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>
        {provider ? 'Редактировать провайдера' : 'Новый SMS-провайдер'}
      </DialogTitle>
      <DialogContent>
        {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
        
        <TextField
          select
          fullWidth
          margin="dense"
          name="type"
          label="Тип провайдера"
          value={formData.type}
          onChange={handleTypeChange}
          required
        >
          {providerTypes.map((type) => (
            <MenuItem key={type} value={type}>
              {type === 'rocketsms' ? 'RocketSMS' : 'CallPassword'}
            </MenuItem>
          ))}
        </TextField>

        <TextField
          fullWidth
          margin="dense"
          name="name"
          label="Название"
          value={formData.name}
          onChange={handleChange}
          required
          error={!!validationErrors.name}
          helperText={validationErrors.name}
        />

        {renderConfigFields()}
        {validationErrors.config && (
          <Alert severity="error" sx={{ mt: 1 }}>{validationErrors.config}</Alert>
        )}

        <FormControlLabel
          control={
            <Checkbox
              checked={formData.is_active}
              onChange={handleCheckbox}
            />
          }
          label="Активен"
        />
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Отмена</Button>
        <Button 
          onClick={handleSubmit} 
          variant="contained" 
          disabled={loading}
        >
          {loading ? 'Сохранение...' : 'Сохранить'}
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default ProviderForm;