import { useState, useEffect } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Button,
  Checkbox,
  FormControlLabel,
  Alert,
} from '@mui/material';
import api from '@/api/axios';

interface VenueFormProps {
  open: boolean;
  onClose: () => void;
  onSaved: () => void;
  venueId?: number;
}

export default function VenueForm({ open, onClose, onSaved, venueId }: VenueFormProps) {
  const [form, setForm] = useState({
    name: '',
    domain: '',
    description: '',
    address: '',
    contact_phone: '',
    contact_email: '',
    is_active: true,
    ssl_enabled: false,
  });
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(false);
  const [apiError, setApiError] = useState('');

  useEffect(() => {
    if (open && venueId) {
      api.get(`/venues/${venueId}`).then(res => {
        setForm(res.data);
      }).catch(() => setApiError('Ошибка загрузки данных'));
    } else if (open) {
      setForm({
        name: '',
        domain: '',
        description: '',
        address: '',
        contact_phone: '',
        contact_email: '',
        is_active: true,
        ssl_enabled: false,
      });
    }
  }, [open, venueId]);

  const validate = () => {
    const newErrors: Record<string, string> = {};
    if (!form.name.trim()) newErrors.name = 'Название обязательно';
    if (form.domain && !/^[a-z0-9.-]+\.[a-z]{2,}$/.test(form.domain)) {
      newErrors.domain = 'Некорректный домен';
    }
    if (form.contact_email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.contact_email)) {
      newErrors.contact_email = 'Некорректный email';
    }
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, type, checked } = e.target;
    setForm((prev) => ({ ...prev, [name]: type === 'checkbox' ? checked : value }));
    // Сбрасываем ошибку для этого поля
    if (errors[name]) setErrors((prev) => ({ ...prev, [name]: undefined }));
  };

  const handleSubmit = async () => {
    if (!validate()) return;
    setLoading(true);
    setApiError('');
    try {
      if (venueId) {
        await api.put(`/venues/${venueId}`, form);
      } else {
        await api.post('/venues', form);
      }
      onSaved();
      onClose();
    } catch (err: any) {
      setApiError(err.response?.data?.detail || 'Ошибка сохранения');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>{venueId ? 'Редактировать площадку' : 'Новая площадка'}</DialogTitle>
      <DialogContent>
        {apiError && <Alert severity="error" sx={{ mb: 2 }}>{apiError}</Alert>}
        <TextField
          autoFocus
          margin="dense"
          name="name"
          label="Название"
          fullWidth
          value={form.name}
          onChange={handleChange}
          error={!!errors.name}
          helperText={errors.name}
          required
        />
        <TextField
          margin="dense"
          name="domain"
          label="Домен"
          fullWidth
          value={form.domain}
          onChange={handleChange}
          error={!!errors.domain}
          helperText={errors.domain}
        />
        <TextField
          margin="dense"
          name="description"
          label="Описание"
          fullWidth
          multiline
          rows={2}
          value={form.description}
          onChange={handleChange}
        />
        <TextField
          margin="dense"
          name="address"
          label="Адрес"
          fullWidth
          value={form.address}
          onChange={handleChange}
        />
        <TextField
          margin="dense"
          name="contact_phone"
          label="Телефон"
          fullWidth
          value={form.contact_phone}
          onChange={handleChange}
        />
        <TextField
          margin="dense"
          name="contact_email"
          label="Email"
          fullWidth
          value={form.contact_email}
          onChange={handleChange}
          error={!!errors.contact_email}
          helperText={errors.contact_email}
        />
        <FormControlLabel
          control={<Checkbox name="is_active" checked={form.is_active} onChange={handleChange} />}
          label="Активна"
        />
        <FormControlLabel
          control={<Checkbox name="ssl_enabled" checked={form.ssl_enabled} onChange={handleChange} />}
          label="HTTPS"
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
}
