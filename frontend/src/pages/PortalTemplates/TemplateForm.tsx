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
  Tab,
  Tabs,
  Box,
} from '@mui/material';
import api from '@/api/axios';
import { portalTemplateSchema, PortalTemplateFormValues } from '@/validation/portalTemplateSchema';
import TemplateFileManager from '@/components/TemplateFileManager/TemplateFileManager';

interface TemplateFormProps {
  open: boolean;
  onClose: () => void;
  onSaved: () => void;
  templateId?: number;
}

export default function TemplateForm({ open, onClose, onSaved, templateId }: TemplateFormProps) {
  const [tab, setTab] = useState(0);
  const [form, setForm] = useState<PortalTemplateFormValues>({
    venue_id: 1,
    type: 'auth',
    html_content: '',
    css_files: [],
    js_files: [],
    images: [],
    is_active: true,
  });
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(false);
  const [apiError, setApiError] = useState('');

  useEffect(() => {
    if (open && templateId) {
      api.get(`/portal-templates/${templateId}`).then(res => {
        setForm(res.data);
      }).catch(() => setApiError('Ошибка загрузки данных'));
    } else if (open) {
      setForm({
        venue_id: 1,
        type: 'auth',
        html_content: '',
        css_files: [],
        js_files: [],
        images: [],
        is_active: true,
      });
    }
  }, [open, templateId]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
    if (errors[name]) setErrors((prev) => ({ ...prev, [name]: undefined }));
  };

  const handleCheckbox = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm((prev) => ({ ...prev, is_active: e.target.checked }));
  };

  const handleFilesUpdate = (css: string[], js: string[], images: string[]) => {
    setForm((prev) => ({ ...prev, css_files: css, js_files: js, images }));
  };

  const handleSubmit = async () => {
    try {
      await portalTemplateSchema.validate(form, { abortEarly: false });
      setErrors({});

      setLoading(true);
      setApiError('');
      if (templateId) {
        await api.put(`/portal-templates/${templateId}`, form);
      } else {
        await api.post('/portal-templates', form);
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
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      <DialogTitle>{templateId ? 'Редактировать шаблон' : 'Новый шаблон'}</DialogTitle>
      <DialogContent>
        {apiError && <Alert severity="error" sx={{ mb: 2 }}>{apiError}</Alert>}
        <Tabs value={tab} onChange={(_, v) => setTab(v)} sx={{ mb: 2 }}>
          <Tab label="Основное" />
          <Tab label="Файлы" />
        </Tabs>
        <Box hidden={tab !== 0}>
          <TextField
            margin="dense"
            name="venue_id"
            label="ID площадки"
            type="number"
            fullWidth
            value={form.venue_id}
            onChange={handleChange}
            error={!!errors.venue_id}
            helperText={errors.venue_id}
            required
          />
          <TextField
            margin="dense"
            name="type"
            label="Тип"
            select
            fullWidth
            value={form.type}
            onChange={handleChange}
            SelectProps={{ native: true }}
          >
            <option value="auth">Авторизация</option>
            <option value="welcome">Приветствие</option>
            <option value="error">Ошибка</option>
          </TextField>
          <TextField
            margin="dense"
            name="html_content"
            label="HTML-код"
            fullWidth
            multiline
            rows={10}
            value={form.html_content}
            onChange={handleChange}
            error={!!errors.html_content}
            helperText={errors.html_content}
            required
          />
          <FormControlLabel
            control={<Checkbox checked={form.is_active} onChange={handleCheckbox} />}
            label="Активен"
          />
        </Box>
        <Box hidden={tab !== 1}>
          {templateId ? (
            <TemplateFileManager
              templateId={templateId}
              venueId={form.venue_id}
              initialCss={form.css_files}
              initialJs={form.js_files}
              initialImages={form.images}
              onUpdate={handleFilesUpdate}
            />
          ) : (
            <Alert severity="info">Сначала сохраните шаблон, чтобы можно было загружать файлы</Alert>
          )}
        </Box>
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