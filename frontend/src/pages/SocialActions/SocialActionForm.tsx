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
import api from '@/api/axios';
import { SocialAction, SocialActionFormData, SocialActionType, SocialNetwork } from './types';

interface SocialActionFormProps {
  open: boolean;
  onClose: () => void;
  onSaved: () => void;
  action?: SocialAction | null;
  actionTypes: string[];
  networks: string[];
}

const SocialActionForm: React.FC<SocialActionFormProps> = ({
  open,
  onClose,
  onSaved,
  action,
  actionTypes,
  networks,
}) => {
  const [formData, setFormData] = useState<SocialActionFormData>({
    name: '',
    description: '',
    type: 'subscribe' as SocialActionType,
    network: 'vk' as SocialNetwork,
    config: {},
    is_active: true,
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [validationErrors, setValidationErrors] = useState<Record<string, string>>({});

  useEffect(() => {
    if (action) {
      setFormData({
        name: action.name,
        description: action.description || '',
        type: action.type,
        network: action.network,
        config: action.config,
        is_active: action.is_active,
      });
    } else {
      setFormData({
        name: '',
        description: '',
        type: 'subscribe' as SocialActionType,
        network: 'vk' as SocialNetwork,
        config: {},
        is_active: true,
      });
    }
    setValidationErrors({});
  }, [action]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    if (validationErrors[name]) {
      setValidationErrors((prev) => ({ ...prev, [name]: '' }));
    }
  };

  const handleConfigChange = (field: string, value: any) => {
    setFormData((prev) => ({
      ...prev,
      config: { ...prev.config, [field]: value },
    }));
    if (validationErrors[field]) {
      setValidationErrors((prev) => ({ ...prev, [field]: '' }));
    }
  };

  const handleCheckbox = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData((prev) => ({ ...prev, is_active: e.target.checked }));
  };

  const validate = (): boolean => {
    const errors: Record<string, string> = {};

    if (!formData.name.trim()) {
      errors.name = 'Название не может быть пустым';
    }

    // Проверка config в зависимости от сети
    if (formData.network === 'vk') {
      if (!formData.config.group_id) {
        errors.group_id = 'ID группы обязателен';
      }
      if (!formData.config.access_token) {
        errors.access_token = 'Access token обязателен';
      }
    } else if (formData.network === 'telegram') {
      if (!formData.config.channel_id) {
        errors.channel_id = 'ID канала обязателен';
      }
      if (!formData.config.bot_token) {
        errors.bot_token = 'Bot token обязателен';
      }
    } else if (formData.network === 'viber') {
      if (!formData.config.bot_token) {
        errors.bot_token = 'Bot token обязателен';
      }
    }

    setValidationErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSubmit = async () => {
    if (!validate()) return;

    // Приводим type и network к нижнему регистру перед отправкой
    const dataToSend = {
      ...formData,
      type: formData.type.toLowerCase() as SocialActionType,
      network: formData.network.toLowerCase() as SocialNetwork,
    };

    setLoading(true);
    setError('');
    try {
      const url = action ? `/social/actions/${action.id}` : '/social/actions';
      if (action) {
        await api.put(url, dataToSend);
      } else {
        await api.post(url, dataToSend);
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
    switch (formData.network) {
      case 'vk':
        return (
          <Box sx={{ mt: 2 }}>
            <Typography variant="subtitle2" gutterBottom>Настройки VK</Typography>
            <TextField
              fullWidth
              margin="dense"
              label="ID группы"
              value={formData.config.group_id || ''}
              onChange={(e) => handleConfigChange('group_id', e.target.value)}
              required
              error={!!validationErrors.group_id}
              helperText={validationErrors.group_id}
            />
            <TextField
              fullWidth
              margin="dense"
              label="Access token"
              value={formData.config.access_token || ''}
              onChange={(e) => handleConfigChange('access_token', e.target.value)}
              required
              error={!!validationErrors.access_token}
              helperText={validationErrors.access_token}
            />
          </Box>
        );
      case 'telegram':
        return (
          <Box sx={{ mt: 2 }}>
            <Typography variant="subtitle2" gutterBottom>Настройки Telegram</Typography>
            <TextField
              fullWidth
              margin="dense"
              label="ID канала (с @ или числовой)"
              value={formData.config.channel_id || ''}
              onChange={(e) => handleConfigChange('channel_id', e.target.value)}
              required
              error={!!validationErrors.channel_id}
              helperText={validationErrors.channel_id}
            />
            <TextField
              fullWidth
              margin="dense"
              label="Bot token"
              value={formData.config.bot_token || ''}
              onChange={(e) => handleConfigChange('bot_token', e.target.value)}
              required
              error={!!validationErrors.bot_token}
              helperText={validationErrors.bot_token}
            />
          </Box>
        );
      case 'viber':
        return (
          <Box sx={{ mt: 2 }}>
            <Typography variant="subtitle2" gutterBottom>Настройки Viber</Typography>
            <TextField
              fullWidth
              margin="dense"
              label="Bot token"
              value={formData.config.bot_token || ''}
              onChange={(e) => handleConfigChange('bot_token', e.target.value)}
              required
              error={!!validationErrors.bot_token}
              helperText={validationErrors.bot_token}
            />
            <TextField
              fullWidth
              margin="dense"
              label="Название бота (опционально)"
              value={formData.config.bot_name || ''}
              onChange={(e) => handleConfigChange('bot_name', e.target.value)}
            />
          </Box>
        );
      default:
        return null;
    }
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>{action ? 'Редактировать акцию' : 'Новая социальная акция'}</DialogTitle>
      <DialogContent>
        {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

        <TextField
          select
          fullWidth
          margin="dense"
          name="type"
          label="Тип действия"
          value={formData.type}
          onChange={handleChange}
          required
        >
          {actionTypes.map((type) => (
            <MenuItem key={type} value={type}>{type}</MenuItem>
          ))}
        </TextField>

        <TextField
          select
          fullWidth
          margin="dense"
          name="network"
          label="Социальная сеть"
          value={formData.network}
          onChange={handleChange}
          required
        >
          {networks.map((net) => (
            <MenuItem key={net} value={net}>{net}</MenuItem>
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

        <TextField
          fullWidth
          margin="dense"
          name="description"
          label="Описание"
          multiline
          rows={2}
          value={formData.description}
          onChange={handleChange}
        />

        {renderConfigFields()}

        <FormControlLabel
          control={<Checkbox checked={formData.is_active} onChange={handleCheckbox} />}
          label="Активна"
        />
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Отмена</Button>
        <Button onClick={handleSubmit} variant="contained" disabled={loading}>
          {loading ? 'Сохранение...' : 'Сохранить'}
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default SocialActionForm;