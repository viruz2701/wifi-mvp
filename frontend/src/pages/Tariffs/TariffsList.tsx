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
import { Tariff } from './types';

interface TariffsListProps {
  onEdit: (tariff: Tariff) => void;
  onAdd: () => void;
}

const TariffsList: React.FC<TariffsListProps> = ({ onEdit, onAdd }) => {
  const [tariffs, setTariffs] = useState<Tariff[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const { showSuccess, showError } = useSnackbar();

  const fetchTariffs = async () => {
    setLoading(true);
    try {
      const response = await api.get('/tariff-plans/'); // обратите внимание на слеш
      setTariffs(response.data);
    } catch (err: any) {
      setError(err.message || 'Ошибка загрузки');
      showError(err.message || 'Ошибка загрузки');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTariffs();
  }, []);

  const handleDelete = async (id: number) => {
    if (!window.confirm('Удалить тариф?')) return;
    try {
      await api.delete(`/tariff-plans/${id}`);
      showSuccess('Тариф удалён');
      fetchTariffs();
    } catch (err: any) {
      showError(err.message || 'Ошибка удаления');
    }
  };

  if (loading) return <CircularProgress />;
  if (error) return <Alert severity="error">{error}</Alert>;

  return (
    <div>
      <Stack direction="row" justifyContent="space-between" alignItems="center" mb={2}>
        <Typography variant="h5">Тарифные планы</Typography>
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
              <TableCell>Цена</TableCell>
              <TableCell>Валюта</TableCell>
              <TableCell>Длительность (ч)</TableCell>
              <TableCell>Скорость (Mbps)</TableCell>
              <TableCell>Статус</TableCell>
              <TableCell align="right">Действия</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {tariffs.map((t) => (
              <TableRow key={t.id}>
                <TableCell>{t.id}</TableCell>
                <TableCell>{t.name}</TableCell>
                <TableCell>{t.price}</TableCell>
                <TableCell>{t.currency}</TableCell>
                <TableCell>{t.duration_hours}</TableCell>
                <TableCell>
                  {t.speed_limit_down_kbps ? `${t.speed_limit_down_kbps / 1024} Mbps` : '—'}
                </TableCell>
                <TableCell>
                  <Chip
                    label={t.is_active ? 'Активен' : 'Неактивен'}
                    color={t.is_active ? 'success' : 'default'}
                    size="small"
                  />
                </TableCell>
                <TableCell align="right">
                  <IconButton size="small" onClick={() => onEdit(t)}>
                    <EditIcon />
                  </IconButton>
                  <IconButton size="small" onClick={() => handleDelete(t.id)}>
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

export default TariffsList;