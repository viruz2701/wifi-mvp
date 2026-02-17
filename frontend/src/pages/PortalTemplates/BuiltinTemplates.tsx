import React, { useEffect, useState } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Grid,
  Card,
  CardMedia,
  CardContent,
  Typography,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Alert,
  CircularProgress
} from '@mui/material';
import api from '@/api/axios';

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
    } catch (err) {
      setError('Не удалось загрузить список шаблонов');
    }
  };

  const fetchVenues = async () => {
    try {
      const response = await api.get('/venues');
      setVenues(response.data);
    } catch (err) {
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
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Ошибка импорта');
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
        <Grid container spacing={2} sx={{ mt: 1 }}>
          {templates.map(tmpl => (
            <Grid item xs={12} sm={6} md={4} key={tmpl.id}>
              <Card>
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
            </Grid>
          ))}
        </Grid>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Закрыть</Button>
      </DialogActions>
    </Dialog>
  );
};