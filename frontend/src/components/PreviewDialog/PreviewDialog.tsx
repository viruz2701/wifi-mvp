import { Dialog, DialogTitle, DialogContent, DialogActions, Button, Box, TextField } from '@mui/material';
import { useState } from 'react';
import api from '@/api/axios';

interface PreviewDialogProps {
  open: boolean;
  onClose: () => void;
  templateId: number;
  venueId: number;
}

export default function PreviewDialog({ open, onClose, templateId, venueId }: PreviewDialogProps) {
  const [mac, setMac] = useState('AA:BB:CC:DD:EE:FF');
  const [phone, setPhone] = useState('375291234567'); // исправлено
  const [errorMsg, setErrorMsg] = useState('');
  const [bannerUrl, setBannerUrl] = useState('/static/test_banner.jpg');
  const [previewHtml, setPreviewHtml] = useState('');

  const fetchPreview = async () => {
    try {
      const response = await api.get(`/portal/preview/${templateId}`, {
        params: { venue_id: venueId, mac, phone, error: errorMsg, banner_url: bannerUrl },
      });
      setPreviewHtml(response.data);
    } catch {
      alert('Ошибка загрузки предпросмотра');
    }
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="lg" fullWidth>
      <DialogTitle>Предпросмотр шаблона</DialogTitle>
      <DialogContent>
        <Box sx={{ display: 'flex', gap: 2, mb: 2, flexWrap: 'wrap' }}>
          <TextField label="MAC" value={mac} onChange={(e) => setMac(e.target.value)} size="small" />
          <TextField label="Телефон" value={phone} onChange={(e) => setPhone(e.target.value)} size="small" />
          <TextField label="Ошибка" value={errorMsg} onChange={(e) => setErrorMsg(e.target.value)} size="small" />
          <TextField label="URL баннера" value={bannerUrl} onChange={(e) => setBannerUrl(e.target.value)} size="small" fullWidth />
          <Button variant="contained" onClick={fetchPreview}>Обновить</Button>
        </Box>
        <Box sx={{ border: '1px solid #ccc', p: 2, maxHeight: '70vh', overflow: 'auto' }}>
          <div dangerouslySetInnerHTML={{ __html: previewHtml }} />
        </Box>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Закрыть</Button>
      </DialogActions>
    </Dialog>
  );
}