import { useEffect, useState, useCallback } from 'react';
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
import { SmsProvider } from './types';
import api from '@/api/axios';
import { useSnackbar } from '@/hooks/useSnackbar';
import { AxiosError } from 'axios';

interface ProvidersListProps {
  onEdit: (provider: SmsProvider) => void;
  onAdd: () => void;
}

const ProvidersList: React.FC<ProvidersListProps> = ({ onEdit, onAdd }) => {
  const [providers, setProviders] = useState<SmsProvider[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const { showSuccess, showError } = useSnackbar();

  const fetchProviders = useCallback(async () => {
    setLoading(true);
    try {
      const response = await api.get('/sms-providers');
      setProviders(response.data);
      setError('');
    } catch (err) {
      const errorMessage = err instanceof AxiosError ? err.message : 'Ошибка загрузки';
      setError(errorMessage);
      showError(errorMessage);
    } finally {
      setLoading(false);
    }
  }, [showError]);

  useEffect(() => {
    fetchProviders();
  }, [fetchProviders]);

  const handleDelete = async (id: number) => {
    if (!window.confirm('Удалить провайдера?')) return;
    try {
      await api.delete(`/sms-providers/${id}`);
      showSuccess('Провайдер удалён');
      fetchProviders();
    } catch (err) {
      const errorMessage = err instanceof AxiosError ? err.message : 'Ошибка удаления';
      showError(errorMessage);
    }
  };

  const handleSetActive = async (id: number) => {
    try {
      await api.post(`/sms-providers/${id}/set-active`);
      showSuccess('Провайдер активирован');
      fetchProviders();
    } catch (err) {
      const errorMessage = err instanceof AxiosError ? err.message : 'Ошибка активации';
      showError(errorMessage);
    }
  };

  if (loading) return <CircularProgress />;
  if (error) return <Alert severity="error">{error}</Alert>;

  return (
    <div>
      <Stack direction="row" justifyContent="space-between" alignItems="center" mb={2}>
        <Typography variant="h5">SMS-провайдеры</Typography>
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
              <TableCell>Активный</TableCell>
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
                <TableCell>
                  {!provider.is_active && (
                    <Button 
                      size="small" 
                      variant="outlined"
                      onClick={() => handleSetActive(provider.id)}
                    >
                      Сделать активным
                    </Button>
                  )}
                </TableCell>
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

export default ProvidersList;