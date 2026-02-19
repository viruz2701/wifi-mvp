import { useEffect, useState } from 'react';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import { Button, IconButton, Stack, Typography, Chip } from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import AddIcon from '@mui/icons-material/Add';
import api from '@/api/axios';
import { Venue } from '@/types';
import { useSnackbar } from '@/hooks/useSnackbar';
import { ConfirmDialog } from '@/components/ConfirmDialog';
import { LoadingScreen } from '@/components/LoadingScreen';

interface VenuesListProps {
  onEdit: (id: number) => void;
  onAdd: () => void;
}

export default function VenuesList({ onEdit, onAdd }: VenuesListProps) {
  const [venues, setVenues] = useState<Venue[]>([]);
  const [loading, setLoading] = useState(false);
  const [deleteId, setDeleteId] = useState<number | null>(null);
  const { showSuccess, showError } = useSnackbar();

  useEffect(() => {
    fetchVenues();
  }, []);

  const fetchVenues = async () => {
    setLoading(true);
    try {
      const response = await api.get('/venues');
      setVenues(response.data);
    } catch {
      showError('Не удалось загрузить список площадок');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteClick = (id: number) => setDeleteId(id);

  const handleConfirmDelete = async () => {
    if (!deleteId) return;
    try {
      await api.delete(`/venues/${deleteId}`);
      showSuccess('Площадка удалена');
      fetchVenues();
    } catch {
      showError('Ошибка при удалении');
    } finally {
      setDeleteId(null);
    }
  };

  const columns: GridColDef[] = [
    { field: 'id', headerName: 'ID', width: 70 },
    { field: 'name', headerName: 'Название', width: 200 },
    { field: 'domain', headerName: 'Домен', width: 150 },
    { field: 'contact_phone', headerName: 'Телефон', width: 150 },
    {
      field: 'is_active',
      headerName: 'Статус',
      width: 100,
      renderCell: (params) => (
        <Chip label={params.value ? 'Активна' : 'Неактивна'} color={params.value ? 'success' : 'default'} size="small" />
      ),
    },
    {
      field: 'actions',
      headerName: 'Действия',
      width: 120,
      renderCell: (params) => (
        <Stack direction="row" spacing={1}>
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

  if (loading && venues.length === 0) return <LoadingScreen message="Загрузка площадок..." />;

  return (
    <>
      <div style={{ height: 600, width: '100%' }}>
        <Stack direction="row" justifyContent="space-between" alignItems="center" mb={2}>
          <Typography variant="h5">Площадки</Typography>
          <Button variant="contained" startIcon={<AddIcon />} onClick={onAdd}>
            Добавить
          </Button>
        </Stack>
        <DataGrid
          rows={venues}
          columns={columns}
          loading={loading}
          pageSizeOptions={[10, 25, 50, 100]}
        />
      </div>
      <ConfirmDialog
        open={deleteId !== null}
        message="Вы уверены, что хотите удалить площадку?"
        onConfirm={handleConfirmDelete}
        onCancel={() => setDeleteId(null)}
      />
    </>
  );
}