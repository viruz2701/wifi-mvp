import { useState, useEffect } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Checkbox,
  FormControlLabel,
  Alert,
} from '@mui/material';
import { getUserProfile, updateUserProfile } from '@/api/userProfiles';
import { userProfileSchema, UserProfileFormValues } from '@/validation/userProfileSchema';

interface ProfileEditDialogProps {
  open: boolean;
  onClose: () => void;
  onSaved: () => void;
  profileId: number;
  initialData?: UserProfileFormValues;
}

export default function ProfileEditDialog({ open, onClose, onSaved, profileId, initialData }: ProfileEditDialogProps) {
  const [form, setForm] = useState<UserProfileFormValues>({
    is_blocked: false,
    is_vip: false,
  });
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(false);
  const [apiError, setApiError] = useState('');

  useEffect(() => {
    if (open && profileId) {
      if (initialData) {
        setForm(initialData);
      } else {
        getUserProfile(profileId).then(res => {
          setForm({ is_blocked: res.data.is_blocked, is_vip: res.data.is_vip });
        }).catch(() => setApiError('Ошибка загрузки данных'));
      }
    }
  }, [open, profileId, initialData]);

  const handleCheckbox = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.checked }));
    if (errors[e.target.name]) setErrors((prev) => ({ ...prev, [e.target.name]: undefined }));
  };

  const handleSubmit = async () => {
    try {
      await userProfileSchema.validate(form, { abortEarly: false });
      setErrors({});

      setLoading(true);
      setApiError('');
      await updateUserProfile(profileId, form);
      onSaved();
      onClose();
    } catch (err: any) {
      if (err.name === 'ValidationError') {
        const validationErrors: Record<string, string> = {};
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
    <Dialog open={open} onClose={onClose} maxWidth="xs" fullWidth>
      <DialogTitle>Редактирование профиля</DialogTitle>
      <DialogContent>
        {apiError && <Alert severity="error" sx={{ mb: 2 }}>{apiError}</Alert>}
        <FormControlLabel
          control={<Checkbox name="is_blocked" checked={form.is_blocked} onChange={handleCheckbox} />}
          label="Заблокирован"
        />
        <FormControlLabel
          control={<Checkbox name="is_vip" checked={form.is_vip} onChange={handleCheckbox} />}
          label="VIP"
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