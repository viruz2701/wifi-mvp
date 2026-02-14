import { useState } from 'react';
import { Box, Typography, List, ListItem, ListItemText, IconButton, Paper, Stack, Alert, LinearProgress } from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import FileUploader from './FileUploader';
import api from '@/api/axios';

interface TemplateFileManagerProps {
  templateId: number;
  files: string[];          // массив путей к файлам
  fileType: 'css' | 'js' | 'images';
  onFilesChanged: (newFiles: string[]) => void;
}

export default function TemplateFileManager({ templateId, files, fileType, onFilesChanged }: TemplateFileManagerProps) {
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState('');

  const handleUploadSuccess = (fileUrl: string) => {
    onFilesChanged([...files, fileUrl]);
    setUploading(false);
  };

  const handleDelete = async (filePath: string) => {
    if (!window.confirm('Удалить файл?')) return;
    try {
      await api.delete(`/portal-templates/${templateId}/files`, {
        params: { file_path: filePath },
      });
      onFilesChanged(files.filter(f => f !== filePath));
    } catch (err) {
      setError('Ошибка при удалении файла');
    }
  };

  return (
    <Paper variant="outlined" sx={{ p: 2, mt: 2 }}>
      <Typography variant="subtitle1" gutterBottom>
        {fileType === 'css' ? 'CSS' : fileType === 'js' ? 'JavaScript' : 'Изображения'}
      </Typography>
      <List dense>
        {files.map((file) => (
          <ListItem
            key={file}
            secondaryAction={
              <IconButton edge="end" onClick={() => handleDelete(file)}>
                <DeleteIcon />
              </IconButton>
            }
          >
            <ListItemText primary={file.split('/').pop()} />
          </ListItem>
        ))}
      </List>
      <Box sx={{ mt: 1 }}>
        <FileUploader
          uploadUrl={`/api/v1/portal-templates/${templateId}/upload?file_type=${fileType}`}
          accept={fileType === 'images' ? 'image/*' : fileType === 'css' ? '.css' : '.js'}
          onSuccess={handleUploadSuccess}
          onError={(msg) => setError(msg)}
        />
        {error && <Alert severity="error" sx={{ mt: 1 }}>{error}</Alert>}
      </Box>
    </Paper>
  );
}