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
  MenuItem,
} from '@mui/material';
import { getBanner, createBanner, updateBanner } from '@/api/banners';
import { getVenues } from '@/api/venues';
import { Venue } from '@/types';
import { bannerSchema, BannerFormValues } from '@/validation/bannerSchema';

interface BannerFormProps {
  open: boolean;
  onClose: () => void;
  onSaved: () => void;
  bannerId?: number;
}

export default function BannerForm({ open, onClose, onSaved, bannerId }: BannerFormProps) {
  const [form, setForm] = useState<BannerFormValues>({
    venue_id: 1,
    target_url: '',
    image_url: null,
    is_active: true,
  });
  const [venues, setVenues] = useState<Venue[]>([]);
  const [errors, setErrors] = useState<Record<string, string | undefined>>({});
  const [loading, setLoading] = useState(false);
  const [apiError, setApiError] = useState('');

  useEffect(() => {
    getVenues().then(res => setVenues(res.data));
  }, []);

  useEffect(() => {
    if (open && bannerId) {
      getBanner(bannerId).then(res => {
        setForm(res.data);
      }).catch(() => setApiError('Ошибка загрузки данных'));
    } else if (open) {
      setForm({
        venue_id: venues[0]?.id || 1,
        target_url: '',
        image_url: null,
        is_active: true,
      });
    }
  }, [open, bannerId, venues]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value === '' ? null : value }));
    if (errors[name]) setErrors((prev) => ({ ...prev, [name]: undefined }));
  };

  const handleCheckbox = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm((prev) => ({ ...prev, is_active: e.target.checked }));
  };

  const cleanForm = (data: BannerFormValues) => {
    const result: any = {};
    for (const key in data) {
      if (data[key as keyof BannerFormValues] !== null) {
        result[key] = data[key as keyof BannerFormValues];
      }
    }
    return result;
  };

  const handleSubmit = async () => {
    try {
      await bannerSchema.validate(form, { abortEarly: false });
      setErrors({});

      setLoading(true);
      setApiError('');
      if (bannerId) {
        await updateBanner(bannerId, cleanForm(form));
      } else {
        await createBanner(cleanForm(form));
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
      <DialogTitle>{bannerId ? 'Редактировать баннер' : 'Новый баннер'}</DialogTitle>
      <DialogContent>
        {apiError && <Alert severity="error" sx={{ mb: 2 }}>{apiError}</Alert>}
        <TextField
          select
          margin="dense"
          name="venue_id"
          label="Площадка"
          fullWidth
          value={form.venue_id}
          onChange={handleChange}
        >
          {venues.map(v => <MenuItem key={v.id} value={v.id}>{v.name}</MenuItem>)}
        </TextField>
        <TextField
          margin="dense"
          name="target_url"
          label="URL перехода"
          fullWidth
          value={form.target_url}
          onChange={handleChange}
          error={!!errors.target_url}
          helperText={errors.target_url}
          required
        />
        <TextField
          margin="dense"
          name="image_url"
          label="URL изображения (будет заполнено после загрузки)"
          fullWidth
          value={form.image_url || ''}
          onChange={handleChange}
          disabled
        />
        <FormControlLabel
          control={<Checkbox checked={form.is_active} onChange={handleCheckbox} />}
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
}