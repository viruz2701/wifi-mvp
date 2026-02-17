import { useEffect, useState } from 'react';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import { Button, IconButton, Stack, Typography, Chip } from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import AddIcon from '@mui/icons-material/Add';
import VisibilityIcon from '@mui/icons-material/Visibility';
import api from '@/api/axios';
import { PortalTemplate } from '@/types';
import { useSnackbar } from '@/hooks/useSnackbar';
import { ConfirmDialog } from '@/components/ConfirmDialog';
import { LoadingScreen } from '@/components/LoadingScreen';
import PreviewDialog from '@/components/PreviewDialog/PreviewDialog';

interface TemplatesListProps {
  onEdit: (id: number) => void;
  onAdd: () => void;
}

export default function TemplatesList({ onEdit, onAdd }: TemplatesListProps) {
  const [templates, setTemplates] = useState<PortalTemplate[]>([]);
  const [loading, setLoading] = useState(false);
  const [deleteId, setDeleteId] = useState<number | null>(null);
  const [previewOpen, setPreviewOpen] = useState(false);
  const [previewTemplateId, setPreviewTemplateId] = useState<number | null>(null);
  const [previewVenueId, setPreviewVenueId] = useState<number>(1);
  const { showSuccess, showError } = useSnackbar();

  useEffect(() => {
    fetchTemplates();
  }, []);

  const fetchTemplates = async () => {
    setLoading(true);
    try {
      const response = await api.get('/portal-templates');
      setTemplates(response.data);
    } catch (err) {
      showError('Не удалось загрузить шаблоны');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteClick = (id: number) => setDeleteId(id);

  const handleConfirmDelete = async () => {
    if (!deleteId) return;
    try {
      await api.delete(`/portal-templates/${deleteId}`);
      showSuccess('Шаблон удалён');
      fetchTemplates();
    } catch (err) {
      showError('Ошибка при удалении');
    } finally {
      setDeleteId(null);
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
          <IconButton size="small" onClick={() => handleDeleteClick(params.row.id)}>
            <DeleteIcon />
          </IconButton>
        </Stack>
      ),
    },
  ];

  if (loading && templates.length === 0) return <LoadingScreen message="Загрузка шаблонов..." />;

  return (
    <>
      <div style={{ height: 600, width: '100%' }}>
        <Stack direction="row" justifyContent="space-between" alignItems="center" mb={2}>
          <Typography variant="h5">Шаблоны портала</Typography>
          <Button variant="contained" startIcon={<AddIcon />} onClick={onAdd}>
            Добавить
          </Button>
        </Stack>
        <DataGrid
          rows={templates}
          columns={columns}
          loading={loading}
          pageSizeOptions={[10, 25, 50, 100]}
        />
      </div>
      {previewTemplateId && (
        <PreviewDialog
          open={previewOpen}
          onClose={() => setPreviewOpen(false)}
          templateId={previewTemplateId}
          venueId={previewVenueId}
        />
      )}
      <ConfirmDialog
        open={deleteId !== null}
        message="Вы уверены, что хотите удалить шаблон?"
        onConfirm={handleConfirmDelete}
        onCancel={() => setDeleteId(null)}
      />
    </>
  );
}