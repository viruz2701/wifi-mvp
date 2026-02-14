import { useState } from 'react';
import { Button, LinearProgress, Box, Typography, Alert } from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';

interface FileUploaderProps {
  uploadUrl: string;           // полный URL для загрузки (например, /api/v1/banners/1/upload)
  accept?: string;             // принимаемые типы файлов
  onSuccess?: (fileUrl: string) => void;
  onError?: (error: string) => void;
  buttonText?: string;
}

export default function FileUploader({ uploadUrl, accept = 'image/*', onSuccess, onError, buttonText = 'Загрузить файл' }: FileUploaderProps) {
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState('');

  const handleUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    setUploading(true);
    setProgress(0);
    setError('');

    try {
      const xhr = new XMLHttpRequest();
      xhr.open('POST', uploadUrl);
      xhr.setRequestHeader('Authorization', `Bearer ${localStorage.getItem('token')}`);

      xhr.upload.addEventListener('progress', (e) => {
        if (e.lengthComputable) {
          setProgress(Math.round((e.loaded / e.total) * 100));
        }
      });

      xhr.onload = () => {
        setUploading(false);
        if (xhr.status === 200) {
          const response = JSON.parse(xhr.responseText);
          onSuccess?.(response.image_url || response.path);
        } else {
          const err = 'Ошибка загрузки';
          setError(err);
          onError?.(err);
        }
      };

      xhr.onerror = () => {
        setUploading(false);
        const err = 'Сетевая ошибка';
        setError(err);
        onError?.(err);
      };

      xhr.send(formData);
    } catch (err) {
      setUploading(false);
      const errMsg = err instanceof Error ? err.message : 'Неизвестная ошибка';
      setError(errMsg);
      onError?.(errMsg);
    }
  };

  return (
    <Box>
      <Button variant="contained" component="label" startIcon={<CloudUploadIcon />} disabled={uploading}>
        {uploading ? 'Загрузка...' : buttonText}
        <input type="file" hidden accept={accept} onChange={handleUpload} />
      </Button>
      {uploading && (
        <Box sx={{ width: '100%', mt: 1 }}>
          <LinearProgress variant="determinate" value={progress} />
          <Typography variant="caption" color="textSecondary">{progress}%</Typography>
        </Box>
      )}
      {error && <Alert severity="error" sx={{ mt: 1 }}>{error}</Alert>}
    </Box>
  );
}