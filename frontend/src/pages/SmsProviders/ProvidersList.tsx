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
import { SmsProvider } from './types';

interface ProvidersListProps {
  onEdit: (provider: SmsProvider) => void;
  onAdd: () => void;
}

const ProvidersList: React.FC<ProvidersListProps> = ({ onEdit, onAdd }) => {
  const [providers, setProviders] = useState<SmsProvider[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const fetchProviders = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/v1/sms-providers', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
      });
      if (!response.ok) throw new Error('Ошибка загрузки');
      const data = await response.json();
      setProviders(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProviders();
  }, []);

  const handleDelete = async (id: number) => {
    if (!window.confirm('Удалить провайдера?')) return;
    try {
      const response = await fetch(`/api/v1/sms-providers/${id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
      });
      if (!response.ok) throw new Error('Ошибка удаления');
      fetchProviders();
    } catch (err: any) {
      alert(err.message);
    }
  };

  const handleSetActive = async (id: number) => {
    try {
      const response = await fetch(`/api/v1/sms-providers/${id}/set-active`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
      });
      if (!response.ok) throw new Error('Ошибка активации');
      fetchProviders();
    } catch (err: any) {
      alert(err.message);
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