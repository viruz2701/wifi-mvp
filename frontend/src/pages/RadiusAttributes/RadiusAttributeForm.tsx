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
import { RadiusAttribute, RadiusAttributeFormData } from './types';

interface RadiusAttributeFormProps {
  open: boolean;
  onClose: () => void;
  onSaved: () => void;
  attribute?: RadiusAttribute | null;
}

const RadiusAttributeForm: React.FC<RadiusAttributeFormProps> = ({
  open,
  onClose,
  onSaved,
  attribute,
}) => {
  const [formData, setFormData] = useState<RadiusAttributeFormData>({
    name: '',
    vendor_id: null,
    is_proprietary: false,
    description: '',
    format_hint: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [validationErrors, setValidationErrors] = useState<Record<string, string>>({});

  useEffect(() => {
    if (attribute) {
      setFormData({
        name: attribute.name,
        vendor_id: attribute.vendor_id,
        is_proprietary: attribute.is_proprietary,
        description: attribute.description || '',
        format_hint: attribute.format_hint || '',
      });
    } else {
      setFormData({
        name: '',
        vendor_id: null,
        is_proprietary: false,
        description: '',
        format_hint: '',
      });
    }
    setValidationErrors({});
  }, [attribute]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, type, checked } = e.target;
    if (type === 'checkbox') {
      setFormData((prev) => ({ ...prev, [name]: checked }));
    } else {
      setFormData((prev) => ({ ...prev, [name]: value === '' ? null : value }));
    }
    if (validationErrors[name]) {
      setValidationErrors((prev) => ({ ...prev, [name]: '' }));
    }
  };

  const validate = (): boolean => {
    const errors: Record<string, string> = {};
    if (!formData.name.trim()) {
      errors.name = 'Название обязательно';
    }
    setValidationErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSubmit = async () => {
    if (!validate()) return;

    setLoading(true);
    setError('');
    try {
      const url = attribute ? `/radius-attributes/${attribute.id}` : '/radius-attributes/';
      if (attribute) {
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
      <DialogTitle>{attribute ? 'Редактировать атрибут' : 'Новый RADIUS-атрибут'}</DialogTitle>
      <DialogContent>
        {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

        <TextField
          fullWidth
          margin="dense"
          name="name"
          label="Имя атрибута"
          value={formData.name}
          onChange={handleChange}
          required
          error={!!validationErrors.name}
          helperText={validationErrors.name}
        />

        <TextField
          fullWidth
          margin="dense"
          name="vendor_id"
          label="Vendor ID (для VSA, оставьте пустым для стандартных)"
          type="number"
          value={formData.vendor_id ?? ''}
          onChange={handleChange}
          InputProps={{ inputProps: { min: 0 } }}
        />

        <FormControlLabel
          control={
            <Checkbox
              name="is_proprietary"
              checked={formData.is_proprietary}
              onChange={handleChange}
            />
          }
          label="Проприетарный (VSA)"
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
          name="format_hint"
          label="Подсказка по формату значения"
          value={formData.format_hint}
          onChange={handleChange}
          helperText="например: '1M/1M' для Mikrotik-Rate-Limit"
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

export default RadiusAttributeForm;