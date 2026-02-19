// src/pages/Users/UserForm.tsx
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
import { getUser, createUser, updateUser } from '@/api/users';
import { getVenues } from '@/api/venues';
import { Venue } from '@/types';
import { userSchema, UserFormValues } from '@/validation/userSchema';
import { AxiosError } from 'axios';

interface UserFormProps {
  open: boolean;
  onClose: () => void;
  onSaved: () => void;
  userId?: number;
}

export default function UserForm({ open, onClose, onSaved, userId }: UserFormProps) {
  const [form, setForm] = useState<UserFormValues>({
    email: '',
    password: '',
    role: 'admin',
    venue_id: null,
    is_active: true,
    is_superuser: false,
  });
  const [venues, setVenues] = useState<Venue[]>([]);
  const [errors, setErrors] = useState<Record<string, string | undefined>>({});
  const [loading, setLoading] = useState(false);
  const [apiError, setApiError] = useState('');

  useEffect(() => {
    getVenues().then(res => setVenues(res.data));
  }, []);

  useEffect(() => {
    if (open && userId) {
      getUser(userId)
        .then(res => {
          setForm({ ...res.data, password: '' });
        })
        .catch(() => setApiError('Ошибка загрузки данных'));
    } else if (open) {
      setForm({
        email: '',
        password: '',
        role: 'admin',
        venue_id: null,
        is_active: true,
        is_superuser: false,
      });
    }
  }, [open, userId]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
    if (errors[name]) setErrors((prev) => ({ ...prev, [name]: undefined }));
  };

  const handleCheckbox = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.checked }));
  };

  const cleanForm = (data: UserFormValues): Record<string, unknown> => {
    const result: Record<string, unknown> = {};
    for (const key in data) {
      const value = data[key as keyof UserFormValues];
      if (value !== null && value !== '') {
        result[key] = value;
      }
    }
    // При редактировании не отправляем пароль, если он не был изменён
    if (userId && !data.password) {
      delete result.password;
    }
    return result;
  };

  const handleSubmit = async () => {
    try {
      await userSchema.validate(form, {
        abortEarly: false,
        context: { isNew: !userId },
      });
      setErrors({});

      setLoading(true);
      setApiError('');
      const payload = cleanForm(form);
      if (userId) {
        await updateUser(userId, payload);
      } else {
        // Для создания пароль обязателен и должен присутствовать
        if (!payload.password) {
          throw new Error('Пароль обязателен');
        }
        await createUser(payload as Parameters<typeof createUser>[0]); // Приведение типа
      }
      onSaved();
      onClose();
    } catch (err: unknown) {
      if (err && typeof err === 'object' && 'name' in err && err.name === 'ValidationError' && 'inner' in err) {
        const validationErrors: Record<string, string | undefined> = {};
        (err as { inner: { path?: string; message: string }[] }).inner.forEach((e) => {
          if (e.path) validationErrors[e.path] = e.message;
        });
        setErrors(validationErrors);
      } else if (err instanceof AxiosError) {
        setApiError(err.response?.data?.detail || 'Ошибка сохранения');
      } else {
        setApiError(err instanceof Error ? err.message : 'Ошибка сохранения');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>{userId ? 'Редактировать пользователя' : 'Новый пользователь'}</DialogTitle>
      <DialogContent>
        {apiError && <Alert severity="error" sx={{ mb: 2 }}>{apiError}</Alert>}
        <TextField
          margin="dense"
          name="email"
          label="Email"
          type="email"
          fullWidth
          value={form.email}
          onChange={handleChange}
          error={!!errors.email}
          helperText={errors.email}
          required
        />
        <TextField
          margin="dense"
          name="password"
          label="Пароль"
          type="password"
          fullWidth
          value={form.password}
          onChange={handleChange}
          error={!!errors.password}
          helperText={errors.password}
          required={!userId}
        />
        <TextField
          select
          margin="dense"
          name="role"
          label="Роль"
          fullWidth
          value={form.role}
          onChange={handleChange}
        >
          <MenuItem value="admin">Администратор</MenuItem>
          <MenuItem value="venue_owner">Владелец площадки</MenuItem>
          <MenuItem value="marketing">Маркетолог</MenuItem>
          <MenuItem value="support">Техподдержка</MenuItem>
        </TextField>
        {form.role === 'venue_owner' && (
          <TextField
            select
            margin="dense"
            name="venue_id"
            label="Площадка"
            fullWidth
            value={form.venue_id || ''}
            onChange={handleChange}
            error={!!errors.venue_id}
            helperText={errors.venue_id}
          >
            {venues.map(v => <MenuItem key={v.id} value={v.id}>{v.name}</MenuItem>)}
          </TextField>
        )}
        <FormControlLabel
          control={<Checkbox name="is_active" checked={form.is_active} onChange={handleCheckbox} />}
          label="Активен"
        />
        <FormControlLabel
          control={<Checkbox name="is_superuser" checked={form.is_superuser} onChange={handleCheckbox} />}
          label="Суперпользователь"
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