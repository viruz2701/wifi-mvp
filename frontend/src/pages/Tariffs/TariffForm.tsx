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
  Alert,
} from '@mui/material';
import api from '@/api/axios';
import { AxiosError } from 'axios';
import { Tariff, TariffFormData } from './types';

interface TariffFormProps {
  open: boolean;
  onClose: () => void;
  onSaved: () => void;
  tariff?: Tariff | null;
}

const TariffForm: React.FC<TariffFormProps> = ({
  open,
  onClose,
  onSaved,
  tariff,
}) => {
  const [formData, setFormData] = useState<TariffFormData>({
    name: '',
    description: '',
    price: 0,
    currency: 'RUB',
    duration_hours: 1,
    speed_limit_up_kbps: undefined,
    speed_limit_down_kbps: undefined,
    is_active: true,
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [validationErrors, setValidationErrors] = useState<Record<string, string>>({});

  useEffect(() => {
    if (tariff) {
      setFormData({
        name: tariff.name,
        description: tariff.description || '',
        price: tariff.price,
        currency: tariff.currency,
        duration_hours: tariff.duration_hours,
        speed_limit_up_kbps: tariff.speed_limit_up_kbps,
        speed_limit_down_kbps: tariff.speed_limit_down_kbps,
        is_active: tariff.is_active,
      });
    } else {
      setFormData({
        name: '',
        description: '',
        price: 0,
        currency: 'RUB',
        duration_hours: 1,
        speed_limit_up_kbps: undefined,
        speed_limit_down_kbps: undefined,
        is_active: true,
      });
    }
    setValidationErrors({});
  }, [tariff]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));
    if (validationErrors[name]) {
      setValidationErrors((prev) => ({ ...prev, [name]: '' }));
    }
  };

  const validate = (): boolean => {
    const errors: Record<string, string> = {};
    if (!formData.name.trim()) errors.name = 'Название обязательно';
    if (formData.price < 0) errors.price = 'Цена не может быть отрицательной';
    if (formData.duration_hours < 1) errors.duration_hours = 'Длительность должна быть ≥ 1';
    setValidationErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSubmit = async () => {
    if (!validate()) return;

    setLoading(true);
    setError('');
    try {
      const url = tariff ? `/tariff-plans/${tariff.id}` : '/tariff-plans/';
      if (tariff) {
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

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>{tariff ? 'Редактировать тариф' : 'Новый тариф'}</DialogTitle>
      <DialogContent>
        {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

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

        <TextField
          fullWidth
          margin="dense"
          name="price"
          label="Цена"
          type="number"
          value={formData.price}
          onChange={handleChange}
          required
          error={!!validationErrors.price}
          helperText={validationErrors.price}
          InputProps={{ inputProps: { min: 0, step: 0.01 } }}
        />

        <TextField
          fullWidth
          margin="dense"
          name="currency"
          label="Валюта"
          value={formData.currency}
          onChange={handleChange}
          required
        />

        <TextField
          fullWidth
          margin="dense"
          name="duration_hours"
          label="Длительность (часы)"
          type="number"
          value={formData.duration_hours}
          onChange={handleChange}
          required
          error={!!validationErrors.duration_hours}
          helperText={validationErrors.duration_hours}
          InputProps={{ inputProps: { min: 1 } }}
        />

        <TextField
          fullWidth
          margin="dense"
          name="speed_limit_up_kbps"
          label="Скорость вверх (kbps, опционально)"
          type="number"
          value={formData.speed_limit_up_kbps ?? ''}
          onChange={handleChange}
        />

        <TextField
          fullWidth
          margin="dense"
          name="speed_limit_down_kbps"
          label="Скорость вниз (kbps, опционально)"
          type="number"
          value={formData.speed_limit_down_kbps ?? ''}
          onChange={handleChange}
        />

        <FormControlLabel
          control={<Checkbox name="is_active" checked={formData.is_active} onChange={handleChange} />}
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

export default TariffForm;