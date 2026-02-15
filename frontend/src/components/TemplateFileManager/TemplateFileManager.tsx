import { useState } from 'react';
import {
  List,
  ListItem,
  ListItemText,
  IconButton,
  Typography,
  Box,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button
} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import VisibilityIcon from '@mui/icons-material/Visibility';
import FileUploader from '@/components/FileUploader/FileUploader';
import api from '@/api/axios';

interface TemplateFileManagerProps {
  templateId: number;
  initialCss?: string[];
  initialJs?: string[];
  initialImages?: string[];
  onUpdate: (css: string[], js: string[], images: string[]) => void;
}

export default function TemplateFileManager({
  templateId,
  initialCss = [],
  initialJs = [],
  initialImages = [],
  onUpdate,
}: TemplateFileManagerProps) {
  const [cssFiles, setCssFiles] = useState(initialCss);
  const [jsFiles, setJsFiles] = useState(initialJs);
  const [images, setImages] = useState(initialImages);
  const [previewOpen, setPreviewOpen] = useState(false);
  const [previewUrl, setPreviewUrl] = useState('');

  const handleUploadSuccess = (type: 'css' | 'js' | 'image', fileUrl: string) => {
    let updatedCss = cssFiles;
    let updatedJs = jsFiles;
    let updatedImages = images;

    if (type === 'css') updatedCss = [...cssFiles, fileUrl];
    if (type === 'js') updatedJs = [...jsFiles, fileUrl];
    if (type === 'image') updatedImages = [...images, fileUrl];

    setCssFiles(updatedCss);
    setJsFiles(updatedJs);
    setImages(updatedImages);
    onUpdate(updatedCss, updatedJs, updatedImages);
  };

  const handleDelete = async (type: 'css' | 'js' | 'image', filePath: string) => {
    if (!window.confirm('Удалить файл?')) return;
    try {
      await api.delete(`/portal-templates/${templateId}/files`, {
        params: { file_path: filePath },
      });

      if (type === 'css') setCssFiles(cssFiles.filter(f => f !== filePath));
      if (type === 'js') setJsFiles(jsFiles.filter(f => f !== filePath));
      if (type === 'image') setImages(images.filter(f => f !== filePath));

      onUpdate(cssFiles, jsFiles, images);
    } catch (err) {
      alert('Ошибка удаления файла');
    }
  };

  const renderFileList = (files: string[], type: 'css' | 'js' | 'image', label: string) => (
    <Box sx={{ mb: 2 }}>
      <Typography variant="subtitle1">{label}</Typography>
      <FileUploader
        uploadUrl={`/api/v1/portal-templates/${templateId}/upload?file_type=${type}`}
        accept={type === 'image' ? 'image/*' : type === 'css' ? '.css' : '.js'}
        onSuccess={(url) => handleUploadSuccess(type, url)}
        buttonText={`Загрузить ${type}`}
      />
      <List dense>
        {files.map((file) => (
          <ListItem
            key={file}
            secondaryAction={
              <>
                <IconButton edge="end" onClick={() => { setPreviewUrl(file); setPreviewOpen(true); }}>
                  <VisibilityIcon />
                </IconButton>
                <IconButton edge="end" onClick={() => handleDelete(type, file)}>
                  <DeleteIcon />
                </IconButton>
              </>
            }
          >
            <ListItemText primary={file.split('/').pop()} />
          </ListItem>
        ))}
      </List>
    </Box>
  );

  return (
    <Box>
      {renderFileList(cssFiles, 'css', 'CSS файлы')}
      {renderFileList(jsFiles, 'js', 'JavaScript файлы')}
      {renderFileList(images, 'image', 'Изображения')}

      <Dialog open={previewOpen} onClose={() => setPreviewOpen(false)} maxWidth="md" fullWidth>
        <DialogTitle>Предпросмотр</DialogTitle>
        <DialogContent>
          {previewUrl.match(/\.(jpg|jpeg|png|gif|svg)$/i) ? (
            <img src={previewUrl} alt="preview" style={{ maxWidth: '100%' }} />
          ) : (
            <iframe src={previewUrl} title="preview" style={{ width: '100%', height: '400px' }} />
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setPreviewOpen(false)}>Закрыть</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}