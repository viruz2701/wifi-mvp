// src/pages/CrmProviders/CrmProviderForm.tsx
import { useState, useEffect } from 'react';
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
import { AxiosError } from 'axios';
import { CrmProvider, CrmProviderFormData } from './types';

interface CrmProviderFormProps {
  open: boolean;
  onClose: () => void;
  onSaved: () => void;
  provider?: CrmProvider | null;
  providerTypes: string[];
}

const CrmProviderForm: React.FC<CrmProviderFormProps> = ({
  open,
  onClose,
  onSaved,
  provider,
  providerTypes,
}) => {
  const [formData, setFormData] = useState<CrmProviderFormData>({
    name: '',
    type: 'bitrix24',
    config: {},
    is_active: true,
    priority: 0,
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
        priority: provider.priority,
      });
    } else {
      setFormData({
        name: '',
        type: 'bitrix24',
        config: {},
        is_active: true,
        priority: 0,
      });
    }
    setValidationErrors({});
  }, [provider]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    if (validationErrors[name]) {
      setValidationErrors((prev) => ({ ...prev, [name]: '' }));
    }
  };

  const handleConfigChange = (field: string, value: string | number | boolean) => {
    setFormData((prev) => ({
      ...prev,
      config: { ...prev.config, [field]: value },
    }));
    if (validationErrors[field]) {
      setValidationErrors((prev) => ({ ...prev, [field]: '' }));
    }
  };

  const handleFieldMappingChange = (field: string, value: string) => {
    setFormData((prev) => ({
      ...prev,
      config: {
        ...prev.config,
        field_mapping: {
          ...(prev.config.field_mapping as Record<string, string> || {}),
          [field]: value,
        },
      },
    }));
  };

  const handleCheckbox = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData((prev) => ({ ...prev, is_active: e.target.checked }));
  };

  const handleTypeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newType = e.target.value as 'bitrix24';
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

    if (formData.type === 'bitrix24') {
      const config = formData.config as { webhook_url?: string };
      if (!config.webhook_url) {
        errors.webhook_url = 'URL вебхука обязателен';
      } else {
        try {
          new URL(config.webhook_url);
        } catch {
          errors.webhook_url = 'Некорректный URL';
        }
      }
    }

    setValidationErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSubmit = async () => {
    if (!validate()) return;

    setLoading(true);
    setError('');
    try {
      const url = provider ? `/crm/providers/${provider.id}` : '/crm/providers';
      if (provider) {
        await api.put(url, formData);
      } else {
        await api.post(url, formData);
      }
      onSaved();
      onClose();
    } catch (err) {
      if (err instanceof AxiosError) {
        setError(err.response?.data?.detail || err.message || 'Ошибка сохранения');
      } else {
        setError('Ошибка сохранения');
      }
    } finally {
      setLoading(false);
    }
  };

  const renderConfigFields = () => {
    switch (formData.type) {
      case 'bitrix24': {
        const config = formData.config as { webhook_url?: string; field_mapping?: Record<string, string> };
        return (
          <Box sx={{ mt: 2 }}>
            <Typography variant="subtitle2" gutterBottom>Настройки Bitrix24</Typography>
            <TextField
              fullWidth
              margin="dense"
              label="URL вебхука"
              value={config.webhook_url || ''}
              onChange={(e) => handleConfigChange('webhook_url', e.target.value)}
              required
              error={!!validationErrors.webhook_url}
              helperText={validationErrors.webhook_url || "https://ваш-портал.bitrix24.ru/rest/1/токен/"}
            />
            <TextField
              fullWidth
              margin="dense"
              label="Маппинг поля телефона (опционально)"
              value={config.field_mapping?.phone || 'PHONE'}
              onChange={(e) => handleFieldMappingChange('phone', e.target.value)}
            />
            <TextField
              fullWidth
              margin="dense"
              label="Маппинг поля email"
              value={config.field_mapping?.email || 'EMAIL'}
              onChange={(e) => handleFieldMappingChange('email', e.target.value)}
            />
            <TextField
              fullWidth
              margin="dense"
              label="Маппинг поля имени"
              value={config.field_mapping?.full_name || 'NAME'}
              onChange={(e) => handleFieldMappingChange('full_name', e.target.value)}
            />
            <TextField
              fullWidth
              margin="dense"
              label="Маппинг поля согласия"
              value={config.field_mapping?.marketing_consent || 'UF_CONSENT'}
              onChange={(e) => handleFieldMappingChange('marketing_consent', e.target.value)}
            />
          </Box>
        );
      }
      default:
        return null;
    }
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>{provider ? 'Редактировать CRM-провайдера' : 'Новый CRM-провайдер'}</DialogTitle>
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
              {type === 'bitrix24' ? 'Bitrix24' : type}
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

        <TextField
          fullWidth
          margin="dense"
          name="priority"
          label="Приоритет (меньше = выше)"
          type="number"
          value={formData.priority}
          onChange={handleChange}
          InputProps={{ inputProps: { min: 0 } }}
        />

        {renderConfigFields()}

        <FormControlLabel
          control={<Checkbox checked={formData.is_active} onChange={handleCheckbox} />}
          label="Активен"
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

export default CrmProviderForm;