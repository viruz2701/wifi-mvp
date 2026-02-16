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
  }, [provider]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleConfigChange = (field: string, value: any) => {
    setFormData((prev) => ({
      ...prev,
      config: { ...prev.config, [field]: value },
    }));
  };

  const handleCheckbox = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData((prev) => ({ ...prev, is_active: e.target.checked }));
  };

  const handleTypeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newType = e.target.value as SmsProviderType;
    // Сбрасываем конфиг при смене типа
    setFormData({
      ...formData,
      type: newType,
      config: {},
    });
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
            />
            <TextField
              fullWidth
              margin="dense"
              label="MD5 пароль"
              value={formData.config.password_md5 || ''}
              onChange={(e) => handleConfigChange('password_md5', e.target.value)}
              required
              helperText="MD5-хеш пароля от личного кабинета"
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
            <Typography variant="subtitle2" gutterBottom>Настройки CallPassword (будут уточнены)</Typography>
            <TextField
              fullWidth
              margin="dense"
              label="API ключ"
              value={formData.config.api_key || ''}
              onChange={(e) => handleConfigChange('api_key', e.target.value)}
              required
            />
            {/* Добавим остальные поля после изучения API */}
          </Box>
        );
      default:
        return null;
    }
  };

  const handleSubmit = async () => {
    setLoading(true);
    setError('');
    try {
      const url = provider 
        ? `/api/v1/sms-providers/${provider.id}`
        : '/api/v1/sms-providers';
      const method = provider ? 'PUT' : 'POST';
      
      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Ошибка сохранения');
      }

      onSaved();
      onClose();
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
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
        />

        {renderConfigFields()}

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