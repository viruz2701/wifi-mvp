import React, { useEffect, useState } from 'react';
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
import { CrmProvider } from './types';

interface CrmProvidersListProps {
  onEdit: (provider: CrmProvider) => void;
  onAdd: () => void;
}

const CrmProvidersList: React.FC<CrmProvidersListProps> = ({ onEdit, onAdd }) => {
  const [providers, setProviders] = useState<CrmProvider[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const { showSuccess, showError } = useSnackbar();

  const fetchProviders = async () => {
    setLoading(true);
    try {
      const response = await api.get('/crm/providers');
      setProviders(response.data);
    } catch (err: any) {
      setError(err.message || 'Ошибка загрузки');
      showError(err.message || 'Ошибка загрузки');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProviders();
  }, []);

  const handleDelete = async (id: number) => {
    if (!window.confirm('Удалить CRM-провайдера?')) return;
    try {
      await api.delete(`/crm/providers/${id}`);
      showSuccess('Провайдер удалён');
      fetchProviders();
    } catch (err: any) {
      showError(err.message || 'Ошибка удаления');
    }
  };

  if (loading) return <CircularProgress />;
  if (error) return <Alert severity="error">{error}</Alert>;

  return (
    <div>
      <Stack direction="row" justifyContent="space-between" alignItems="center" mb={2}>
        <Typography variant="h5">CRM-провайдеры</Typography>
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
              <TableCell>Статус</TableCell>
              <TableCell>Приоритет</TableCell>
              <TableCell>Действия</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {providers.map((provider) => (
              <TableRow key={provider.id}>
                <TableCell>{provider.id}</TableCell>
                <TableCell>{provider.name}</TableCell>
                <TableCell>{provider.type}</TableCell>
                <TableCell>
                  <Chip
                    label={provider.is_active ? 'Активен' : 'Неактивен'}
                    color={provider.is_active ? 'success' : 'default'}
                    size="small"
                  />
                </TableCell>
                <TableCell>{provider.priority}</TableCell>
                <TableCell>
                  <IconButton size="small" onClick={() => onEdit(provider)}>
                    <EditIcon />
                  </IconButton>
                  <IconButton size="small" onClick={() => handleDelete(provider.id)}>
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
};

export default CrmProvidersList;