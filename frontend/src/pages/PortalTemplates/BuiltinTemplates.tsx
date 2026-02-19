// src/pages/PortalTemplates/BuiltinTemplates.tsx
import { useEffect, useState } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Card,
  CardMedia,
  CardContent,
  Typography,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Alert,
  Box,
} from '@mui/material';
import api from '@/api/axios';
import { AxiosError } from 'axios';

interface BuiltinTemplate {
  id: string;
  name: string;
  type: string;
  preview: string;
}

interface BuiltinTemplatesProps {
  open: boolean;
  onClose: () => void;
  onImported: () => void;
}

export const BuiltinTemplates: React.FC<BuiltinTemplatesProps> = ({ open, onClose, onImported }) => {
  const [templates, setTemplates] = useState<BuiltinTemplate[]>([]);
  const [venues, setVenues] = useState<{ id: number; name: string }[]>([]);
  const [selectedVenue, setSelectedVenue] = useState<number | ''>('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (open) {
      fetchTemplates();
      fetchVenues();
    }
  }, [open]);

  const fetchTemplates = async () => {
    try {
      const response = await api.get('/builtin-templates');
      setTemplates(response.data);
    } catch {
      setError('Не удалось загрузить список шаблонов');
    }
  };

  const fetchVenues = async () => {
    try {
      const response = await api.get('/venues');
      setVenues(response.data);
    } catch {
      setError('Не удалось загрузить список площадок');
    }
  };

  const handleImport = async (templateId: string) => {
    if (!selectedVenue) {
      setError('Выберите площадку');
      return;
    }
    setLoading(true);
    setError('');
    try {
      await api.post(`/builtin-templates/${templateId}/import?venue_id=${selectedVenue}`);
      onImported();
      onClose();
    } catch (err) {
      if (err instanceof AxiosError) {
        setError(err.response?.data?.detail || 'Ошибка импорта');
      } else {
        setError('Ошибка импорта');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      <DialogTitle>Выберите готовый шаблон</DialogTitle>
      <DialogContent>
        {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
        <FormControl fullWidth margin="dense">
          <InputLabel>Площадка</InputLabel>
          <Select
            value={selectedVenue}
            onChange={(e) => setSelectedVenue(e.target.value as number)}
          >
            {venues.map(v => <MenuItem key={v.id} value={v.id}>{v.name}</MenuItem>)}
          </Select>
        </FormControl>
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2, mt: 2 }}>
          {templates.map(tmpl => (
            <Card key={tmpl.id} sx={{ width: { xs: '100%', sm: 'calc(50% - 8px)', md: 'calc(33.333% - 16px)' } }}>
              {tmpl.preview && (
                <CardMedia
                  component="img"
                  height="140"
                  image={tmpl.preview}
                  alt={tmpl.name}
                />
              )}
              <CardContent>
                <Typography variant="h6">{tmpl.name}</Typography>
                <Typography variant="body2">Тип: {tmpl.type}</Typography>
                <Button
                  variant="contained"
                  size="small"
                  sx={{ mt: 1 }}
                  onClick={() => handleImport(tmpl.id)}
                  disabled={!selectedVenue || loading}
                >
                  {loading ? 'Импорт...' : 'Использовать'}
                </Button>
              </CardContent>
            </Card>
          ))}
        </Box>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Закрыть</Button>
      </DialogActions>
    </Dialog>
  );
};