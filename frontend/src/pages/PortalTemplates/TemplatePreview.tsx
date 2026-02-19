import { useEffect, useState } from 'react';
import { Paper, CircularProgress, Alert } from '@mui/material';
import api from '@/api/axios';

interface TemplatePreviewProps {
  templateId?: number;
  venueId: number;
  htmlContent: string;
  files: {
    css_files: string[];
    js_files: string[];
    images: string[];
  };
}

export default function TemplatePreview({ templateId, venueId, htmlContent, files }: TemplatePreviewProps) {
  const [previewHtml, setPreviewHtml] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchPreview = async () => {
      if (!templateId) {
        // локальный предпросмотр с подстановкой макросов
        let html = htmlContent;
        const context = {
          venue_name: 'Тестовая площадка',
          mac: 'AA:BB:CC:DD:EE:FF',
          phone: '375291234567',  // исправлено на белорусский формат
          error: '',
          banner_url: files.images[0] || '/static/test_banner.jpg',
          code: '1234',
          dst: 'http://example.com',
          year: '2026',
        };
        html = html.replace(/\$\((\w+)\)/g, (_, key) => {
          const k = key as keyof typeof context;
          return context[k] || `$(${key})`;
        });
        setPreviewHtml(html);
        return;
      }

      setLoading(true);
      try {
        const params = new URLSearchParams({
          venue_id: venueId.toString(),
          mac: 'AA:BB:CC:DD:EE:FF',
          phone: '375291234567',  // исправлено
          banner_url: files.images[0] || '/static/test_banner.jpg',
        });
        const response = await api.get(`/portal/preview/${templateId}?${params}`, {
          responseType: 'text',
        });
        setPreviewHtml(response.data);
      } catch {
        setError('Не удалось загрузить предпросмотр');
      } finally {
        setLoading(false);
      }
    };

    fetchPreview();
  }, [templateId, venueId, htmlContent, files]);

  if (loading) return <CircularProgress />;
  if (error) return <Alert severity="error">{error}</Alert>;

  return (
    <Paper variant="outlined" sx={{ p: 2, mt: 2, maxHeight: 500, overflow: 'auto' }}>
      <div dangerouslySetInnerHTML={{ __html: previewHtml }} />
    </Paper>
  );
}