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
import { venueSchema, VenueFormValues } from '@/validation/venueSchema';

interface VenueFormProps {
  open: boolean;
  onClose: () => void;
  onSaved: () => void;
  venueId?: number;
}

export default function VenueForm({ open, onClose, onSaved, venueId }: VenueFormProps) {
  const [form, setForm] = useState<VenueFormValues>({
    name: '',
    domain: null,
    description: '',
    address: '',
    contact_phone: '',
    contact_email: '',
    is_active: true,
    ssl_enabled: false,
  });
  const [errors, setErrors] = useState<Record<string, string | undefined>>({});
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
        domain: null,
        description: '',
        address: '',
        contact_phone: '',
        contact_email: '',
        is_active: true,
        ssl_enabled: false,
      });
    }
  }, [open, venueId]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, type, checked } = e.target;
    setForm((prev) => ({ ...prev, [name]: type === 'checkbox' ? checked : value === '' ? null : value }));
    if (errors[name]) setErrors((prev) => ({ ...prev, [name]: undefined }));
  };

  const cleanForm = (data: VenueFormValues) => {
    const result: any = {};
    for (const key in data) {
      const value = data[key as keyof VenueFormValues];
      if (value !== null) {
        result[key] = value;
      }
    }
    return result;
  };

  const handleSubmit = async () => {
    try {
      await venueSchema.validate(form, { abortEarly: false });
      setErrors({});

      setLoading(true);
      setApiError('');
      if (venueId) {
        await api.put(`/venues/${venueId}`, cleanForm(form));
      } else {
        await api.post('/venues', cleanForm(form));
      }
      onSaved();
      onClose();
    } catch (err: any) {
      if (err.name === 'ValidationError') {
        const validationErrors: Record<string, string | undefined> = {};
        err.inner.forEach((e: any) => {
          if (e.path) validationErrors[e.path] = e.message;
        });
        setErrors(validationErrors);
      } else {
        setApiError(err.response?.data?.detail || 'Ошибка сохранения');
      }
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
          value={form.domain || ''}
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