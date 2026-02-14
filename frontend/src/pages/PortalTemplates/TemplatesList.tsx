import { useEffect, useState } from 'react';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import { Button, IconButton, Stack, Typography, Chip } from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import AddIcon from '@mui/icons-material/Add';
import VisibilityIcon from '@mui/icons-material/Visibility';
import api from '@/api/axios';
import { PortalTemplate } from '@/types';
import PreviewDialog from '@/components/PreviewDialog/PreviewDialog';

interface TemplatesListProps {
  onEdit: (id: number) => void;
  onAdd: () => void;
}

export default function TemplatesList({ onEdit, onAdd }: TemplatesListProps) {
  const [templates, setTemplates] = useState<PortalTemplate[]>([]);
  const [loading, setLoading] = useState(false);
  const [previewOpen, setPreviewOpen] = useState(false);
  const [previewTemplateId, setPreviewTemplateId] = useState<number | null>(null);
  const [previewVenueId, setPreviewVenueId] = useState<number>(1);

  useEffect(() => {
    fetchTemplates();
  }, []);

  const fetchTemplates = async () => {
    setLoading(true);
    try {
      const response = await api.get('/portal-templates');
      setTemplates(response.data);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('Удалить шаблон?')) {
      await api.delete(`/portal-templates/${id}`);
      fetchTemplates();
    }
  };

  const columns: GridColDef[] = [
    { field: 'id', headerName: 'ID', width: 70 },
    { field: 'venue_id', headerName: 'Площадка', width: 100 },
    { field: 'type', headerName: 'Тип', width: 120 },
    {
      field: 'is_active',
      headerName: 'Активен',
      width: 100,
      renderCell: (params) => (
        <Chip label={params.value ? 'Да' : 'Нет'} color={params.value ? 'success' : 'default'} size="small" />
      ),
    },
    {
      field: 'actions',
      headerName: 'Действия',
      width: 150,
      renderCell: (params) => (
        <Stack direction="row" spacing={1}>
          <IconButton size="small" onClick={() => { setPreviewTemplateId(params.row.id); setPreviewVenueId(params.row.venue_id); setPreviewOpen(true); }}>
            <VisibilityIcon />
          </IconButton>
          <IconButton size="small" onClick={() => onEdit(params.row.id)}>
            <EditIcon />
          </IconButton>
          <IconButton size="small" onClick={() => handleDelete(params.row.id)}>
            <DeleteIcon />
          </IconButton>
        </Stack>
      ),
    },
  ];

  return (
    <div style={{ height: 600, width: '100%' }}>
      <Stack direction="row" justifyContent="space-between" alignItems="center" mb={2}>
        <Typography variant="h5">Шаблоны портала</Typography>
        <Button variant="contained" startIcon={<AddIcon />} onClick={onAdd}>
          Добавить
        </Button>
      </Stack>
      <DataGrid rows={templates} columns={columns} loading={loading} pageSizeOptions={[10, 25, 50]} />
      {previewTemplateId && (
        <PreviewDialog
          open={previewOpen}
          onClose={() => setPreviewOpen(false)}
          templateId={previewTemplateId}
          venueId={previewVenueId}
        />
      )}
    </div>
  );
}
