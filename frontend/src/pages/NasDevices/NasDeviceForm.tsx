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
import { getNasDevice, createNasDevice, updateNasDevice } from '@/api/nasDevices';
import { getVenues } from '@/api/venues';
import { Venue } from '@/types';
import { nasDeviceSchema, NasDeviceFormValues } from '@/validation/nasDeviceSchema';

interface NasDeviceFormProps {
  open: boolean;
  onClose: () => void;
  onSaved: () => void;
  deviceId?: number;
}

export default function NasDeviceForm({ open, onClose, onSaved, deviceId }: NasDeviceFormProps) {
  const [form, setForm] = useState<NasDeviceFormValues>({
    venue_id: 1,
    name: '',
    type: 'mikrotik',
    ip_address: '',
    secret: '',
    api_username: null,
    api_password: null,
    wireguard_pubkey: null,
    wireguard_ip: null,
    is_active: true,
  });
  const [venues, setVenues] = useState<Venue[]>([]);
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(false);
  const [apiError, setApiError] = useState('');

  useEffect(() => {
    getVenues().then(res => setVenues(res.data));
  }, []);

  useEffect(() => {
    if (open && deviceId) {
      getNasDevice(deviceId).then(res => {
        setForm(res.data);
      }).catch(() => setApiError('Ошибка загрузки данных'));
    } else if (open) {
      setForm({
        venue_id: venues[0]?.id || 1,
        name: '',
        type: 'mikrotik',
        ip_address: '',
        secret: '',
        api_username: null,
        api_password: null,
        wireguard_pubkey: null,
        wireguard_ip: null,
        is_active: true,
      });
    }
  }, [open, deviceId, venues]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value === '' ? null : value }));
    if (errors[name]) setErrors((prev) => ({ ...prev, [name]: undefined }));
  };

  const handleCheckbox = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm((prev) => ({ ...prev, is_active: e.target.checked }));
  };

  const handleSubmit = async () => {
    try {
      await nasDeviceSchema.validate(form, { abortEarly: false });
      setErrors({});

      setLoading(true);
      setApiError('');
      if (deviceId) {
        await updateNasDevice(deviceId, form);
      } else {
        await createNasDevice(form);
      }
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
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>{deviceId ? 'Редактировать устройство' : 'Новое устройство'}</DialogTitle>
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
          select
          margin="dense"
          name="type"
          label="Тип"
          fullWidth
          value={form.type}
          onChange={handleChange}
        >
          <MenuItem value="mikrotik">MikroTik</MenuItem>
          <MenuItem value="openwrt">OpenWRT</MenuItem>
          <MenuItem value="ubiquiti">Ubiquiti</MenuItem>
        </TextField>
        <TextField
          margin="dense"
          name="ip_address"
          label="IP адрес"
          fullWidth
          value={form.ip_address}
          onChange={handleChange}
          error={!!errors.ip_address}
          helperText={errors.ip_address}
          required
        />
        <TextField
          margin="dense"
          name="secret"
          label="RADIUS secret"
          type="password"
          fullWidth
          value={form.secret}
          onChange={handleChange}
          error={!!errors.secret}
          helperText={errors.secret}
          required
        />
        <TextField
          margin="dense"
          name="api_username"
          label="API username"
          fullWidth
          value={form.api_username || ''}
          onChange={handleChange}
        />
        <TextField
          margin="dense"
          name="api_password"
          label="API password"
          type="password"
          fullWidth
          value={form.api_password || ''}
          onChange={handleChange}
        />
        <TextField
          margin="dense"
          name="wireguard_pubkey"
          label="WireGuard public key"
          fullWidth
          multiline
          rows={2}
          value={form.wireguard_pubkey || ''}
          onChange={handleChange}
        />
        <TextField
          margin="dense"
          name="wireguard_ip"
          label="WireGuard IP"
          fullWidth
          value={form.wireguard_ip || ''}
          onChange={handleChange}
        />
        <FormControlLabel
          control={<Checkbox checked={form.is_active} onChange={handleCheckbox} />}
          label="Активно"
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