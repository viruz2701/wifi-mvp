import { useEffect, useState } from 'react';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import { Button, IconButton, Stack, Typography, Chip } from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import AddIcon from '@mui/icons-material/Add';
import api from '@/api/axios';
import { User } from '@/types';
import { useSnackbar } from '@/hooks/useSnackbar';
import { ConfirmDialog } from '@/components/ConfirmDialog';
import { LoadingScreen } from '@/components/LoadingScreen';

interface UsersListProps {
  onEdit: (id: number) => void;
  onAdd: () => void;
}

export default function UsersList({ onEdit, onAdd }: UsersListProps) {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(false);
  const [deleteId, setDeleteId] = useState<number | null>(null);
  const { showSuccess, showError } = useSnackbar();

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    setLoading(true);
    try {
      const response = await api.get('/users');
      setUsers(response.data);
    } catch {
      showError('Не удалось загрузить список пользователей');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteClick = (id: number) => setDeleteId(id);

  const handleConfirmDelete = async () => {
    if (!deleteId) return;
    try {
      await api.delete(`/users/${deleteId}`);
      showSuccess('Пользователь удалён');
      fetchUsers();
    } catch {
      showError('Ошибка при удалении');
    } finally {
      setDeleteId(null);
    }
  };

  const columns: GridColDef[] = [
    { field: 'id', headerName: 'ID', width: 70 },
    { field: 'email', headerName: 'Email', width: 200 },
    { field: 'role', headerName: 'Роль', width: 120 },
    { field: 'venue_id', headerName: 'Площадка', width: 100 },
    {
      field: 'is_active',
      headerName: 'Активен',
      width: 100,
      renderCell: (params) => (
        <Chip label={params.value ? 'Да' : 'Нет'} color={params.value ? 'success' : 'default'} size="small" />
      ),
    },
    {
      field: 'is_superuser',
      headerName: 'Суперпользователь',
      width: 150,
      renderCell: (params) => (
        <Chip label={params.value ? 'Да' : 'Нет'} color={params.value ? 'secondary' : 'default'} size="small" />
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

  if (loading && users.length === 0) return <LoadingScreen message="Загрузка пользователей..." />;

  return (
    <>
      <div style={{ height: 600, width: '100%' }}>
        <Stack direction="row" justifyContent="space-between" alignItems="center" mb={2}>
          <Typography variant="h5">Администраторы</Typography>
          <Button variant="contained" startIcon={<AddIcon />} onClick={onAdd}>
            Добавить
          </Button>
        </Stack>
        <DataGrid
          rows={users}
          columns={columns}
          loading={loading}
          pageSizeOptions={[10, 25, 50, 100]}
        />
      </div>
      <ConfirmDialog
        open={deleteId !== null}
        message="Вы уверены, что хотите удалить пользователя?"
        onConfirm={handleConfirmDelete}
        onCancel={() => setDeleteId(null)}
      />
    </>
  );
}