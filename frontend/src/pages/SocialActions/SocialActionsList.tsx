import { useEffect, useState } from 'react';
import {
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  IconButton,
  Chip,
  Button,
  Stack,
  Typography,
  Alert,
  CircularProgress,
} from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import AddIcon from '@mui/icons-material/Add';
import api from '@/api/axios';
import { useSnackbar } from '@/hooks/useSnackbar';
import { SocialAction } from './types';

interface SocialActionsListProps {
  onEdit: (action: SocialAction) => void;
  onAdd: () => void;
}

export default function SocialActionsList({ onEdit, onAdd }: SocialActionsListProps) {
  const [actions, setActions] = useState<SocialAction[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const { showSuccess, showError } = useSnackbar();

  const fetchActions = async () => {
    setLoading(true);
    try {
      const response = await api.get('/social/actions');
      setActions(response.data);
      setError('');
    } catch {
      setError('Ошибка загрузки');
      showError('Ошибка загрузки');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchActions();
  }, []);

  const handleDelete = async (id: number) => {
    if (!window.confirm('Удалить социальное действие?')) return;
    try {
      await api.delete(`/social/actions/${id}`);
      showSuccess('Действие удалено');
      fetchActions();
    } catch {
      showError('Ошибка удаления');
    }
  };

  if (loading) return <CircularProgress />;
  if (error) return <Alert severity="error">{error}</Alert>;

  return (
    <div>
      <Stack direction="row" justifyContent="space-between" alignItems="center" mb={2}>
        <Typography variant="h5">Социальные акции</Typography>
        <Button variant="contained" startIcon={<AddIcon />} onClick={onAdd}>
          Добавить
        </Button>
      </Stack>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>Название</TableCell>
              <TableCell>Тип</TableCell>
              <TableCell>Сеть</TableCell>
              <TableCell>Статус</TableCell>
              <TableCell>Действия</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {actions.map((action) => (
              <TableRow key={action.id}>
                <TableCell>{action.id}</TableCell>
                <TableCell>{action.name}</TableCell>
                <TableCell>{action.type}</TableCell>
                <TableCell>{action.network}</TableCell>
                <TableCell>
                  <Chip
                    label={action.is_active ? 'Активна' : 'Неактивна'}
                    color={action.is_active ? 'success' : 'default'}
                    size="small"
                  />
                </TableCell>
                <TableCell>
                  <IconButton size="small" onClick={() => onEdit(action)}>
                    <EditIcon />
                  </IconButton>
                  <IconButton size="small" onClick={() => handleDelete(action.id)}>
                    <DeleteIcon />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </div>
  );
}