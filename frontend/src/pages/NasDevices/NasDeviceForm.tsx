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
  Box,
  Typography,
  Link,
} from '@mui/material';
import OpenInNewIcon from '@mui/icons-material/OpenInNew';
import { getNasDevice, createNasDevice, updateNasDevice } from '@/api/nasDevices';
import { getVenues } from '@/api/venues';
import { Venue } from '@/types';
import { nasDeviceSchema, NasDeviceFormValues } from '@/validation/nasDeviceSchema';
import { AxiosError } from 'axios';

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
    api_username: undefined,
    api_password: undefined,
    wireguard_pubkey: undefined,
    is_active: true,
    generate_wireguard_keys: false,
  });
  const [venues, setVenues] = useState<Venue[]>([]);
  const [errors, setErrors] = useState<Record<string, string | undefined>>({});
  const [loading, setLoading] = useState(false);
  const [apiError, setApiError] = useState('');

  // Маппинг типа устройства на файл документации
  const typeToDoc: Record<string, string> = {
    mikrotik: 'mikrotik_hotspot.md',
    openwrt: 'openwrt_opennds.md',
    ubiquiti: 'ubiquiti.md',
  };

  useEffect(() => {
    getVenues().then(res => setVenues(res.data));
  }, []);

  useEffect(() => {
    if (open && deviceId) {
      getNasDevice(deviceId)
        .then(res => {
          setForm({
            ...res.data,
            secret: '',
            generate_wireguard_keys: false,
          });
        })
        .catch(() => setApiError('Ошибка загрузки данных'));
    } else if (open) {
      setForm({
        venue_id: venues[0]?.id || 1,
        name: '',
        type: 'mikrotik',
        ip_address: '',
        secret: '',
        api_username: undefined,
        api_password: undefined,
        wireguard_pubkey: undefined,
        is_active: true,
        generate_wireguard_keys: false,
      });
    }
    setErrors({});
    setApiError('');
  }, [open, deviceId, venues]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value, type } = e.target;
    const checked = (e.target as HTMLInputElement).checked;
    setForm((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value === '' ? undefined : value,
    }));
    if (errors[name]) setErrors((prev) => ({ ...prev, [name]: undefined }));
  };

  const handleCheckbox = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm((prev) => ({ ...prev, is_active: e.target.checked }));
  };

  const cleanForm = (data: NasDeviceFormValues): Record<string, unknown> => {
    const result: Record<string, unknown> = {};
    for (const key in data) {
      const value = data[key as keyof NasDeviceFormValues];
      if (value !== undefined && value !== '' && key !== 'generate_wireguard_keys') {
        result[key] = value;
      }
    }
    if (data.generate_wireguard_keys) {
      result.generate_wireguard_keys = true;
      delete result.wireguard_pubkey;
    }
    if (deviceId && !data.secret) {
      delete result.secret;
    }
    return result;
  };

  const handleSubmit = async () => {
    try {
      await nasDeviceSchema.validate(form, { abortEarly: false, context: { isNew: !deviceId } });
      setErrors({});

      setLoading(true);
      setApiError('');
      const payload = cleanForm(form);
      if (deviceId) {
        await updateNasDevice(deviceId, payload);
      } else {
        await createNasDevice(payload);
      }
      onSaved();
    } catch (err: unknown) {
      // Validation error from yup
      if (err && typeof err === 'object' && 'name' in err && err.name === 'ValidationError' && 'inner' in err) {
        const validationErrors: Record<string, string | undefined> = {};
        (err as { inner: { path?: string; message: string }[] }).inner.forEach((e) => {
          if (e.path) validationErrors[e.path] = e.message;
        });
        setErrors(validationErrors);
      } else if (err instanceof AxiosError) {
        // HTTP errors
        if (err.response?.status === 409) {
          setApiError(err.response?.data?.detail || 'Устройство с таким IP уже существует');
        } else {
          setApiError(err.response?.data?.detail || 'Ошибка сохранения');
        }
      } else {
        setApiError('Ошибка сохранения');
      }
    } finally {
      setLoading(false);
    }
  };

  const isGenerating = form.generate_wireguard_keys;

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
          required={!deviceId}
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

        <Box sx={{ mt: 2, mb: 1 }}>
          <Typography variant="subtitle2">WireGuard</Typography>
          {!deviceId && (
            <FormControlLabel
              control={
                <Checkbox
                  name="generate_wireguard_keys"
                  checked={form.generate_wireguard_keys}
                  onChange={handleChange}
                />
              }
              label="Сгенерировать ключи автоматически"
            />
          )}
        </Box>

        <TextField
          margin="dense"
          name="wireguard_pubkey"
          label="WireGuard public key"
          fullWidth
          multiline
          rows={2}
          value={form.wireguard_pubkey || ''}
          onChange={handleChange}
          disabled={isGenerating}
          required={!deviceId && !isGenerating}
          helperText={
            isGenerating
              ? 'Ключи будут сгенерированы на сервере'
              : deviceId
              ? 'Оставьте пустым, если не хотите менять'
              : 'Введите публичный ключ или включите генерацию'
          }
        />

        <FormControlLabel
          control={<Checkbox checked={form.is_active} onChange={handleCheckbox} />}
          label="Активно"
        />

        {/* Ссылка на документацию */}
        {form.type && typeToDoc[form.type] && (
          <Box sx={{ mt: 2, display: 'flex', justifyContent: 'flex-end' }}>
            <Link
              href={`/docs/equipment/${typeToDoc[form.type]}`}
              target="_blank"
              rel="noopener"
              underline="hover"
              sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}
            >
              <OpenInNewIcon fontSize="small" />
              Инструкция по настройке {form.type}
            </Link>
          </Box>
        )}
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